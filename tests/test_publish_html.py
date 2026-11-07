"""Regression checks for the reviewed mixed-theme draft and preview boundary."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_gzh_html import validate

CLEAN = '<section style="color:#23251d;text-align:left;font-size:16px;"><p style="margin:0;"><span leaf="">正文</span></p></section>'


class PublishHTMLTests(unittest.TestCase):
    def test_mixed_moyu_colors_and_import_whitespace_are_rejected(self):
        bad = '<section style="background:linear-gradient(#0f9f73,#13c58d);"><p style="text-align:justify;"><span leaf="">重点</span></p>\n<p><strong style="background:#ffe47a;"><span leaf="">核心观点</span></strong></p></section>'
        errors, _, _ = validate(bad, theme='olive-journal', publish_ready=True)
        self.assertTrue(any('#ffe47a' in e for e in errors))
        self.assertTrue(any('两端对齐' in e for e in errors))
        self.assertTrue(any('源码换行' in e for e in errors))
        self.assertEqual(validate(CLEAN, theme='olive-journal', publish_ready=True)[:2], ([], []))

    def test_wechat_body_defaults_cannot_leak_into_published_text(self):
        # WeChat's .rich_media_content defaults to justify/17px; anything not declared inherits them.
        container = '<section style="max-width:677px;color:#23251d;{root}">{body}</section>'
        label = ('<section style="margin:0 0 24px;{card}"><p style="margin:0 0 8px;"><span style="display:inline-block;'
                 'font-size:11px;"><span leaf="">提示词</span></span></p><p style="margin:0;font-size:15px;line-height:1.85;">'
                 '<span leaf="">正文</span></p></section>')
        bare = validate(container.format(root='', body=label.format(card='')), publish_ready=True)[0]
        self.assertTrue(any('text-align' in e for e in bare))
        self.assertTrue(any('17px' in e and '提示词' in e for e in bare))
        # Declared on the container: every component inherits left/16px instead of the WeChat defaults.
        root = 'text-align:left;font-size:16px;'
        self.assertEqual(validate(container.format(root=root, body=label.format(card='')), publish_ready=True)[:2], ([], []))
        # A sized component does not excuse the container: it must still carry the base size for future components.
        only_card = validate(container.format(root='text-align:left;', body=label.format(card='text-align:left;font-size:16px;')),
                             publish_ready=True)[0]
        self.assertTrue(any('17px' in e for e in only_card))
        # Relative sizes resolve against WeChat's 17px, so they do not count.
        relative = '<section style="text-align:left;font-size:1em;"><p style="margin:0;"><span leaf="">正文</span></p></section>'
        self.assertTrue(any('17px' in e for e in validate(relative, publish_ready=True)[0]))
        # The check belongs to --publish-ready only.
        self.assertEqual(validate(container.format(root='', body=label.format(card='')))[:2], ([], []))

    def test_pre_source_whitespace_is_not_allowed(self):
        for value in ('pre', 'pre-wrap', 'pre-line', 'break-spaces'):
            self.assertTrue(validate(CLEAN.replace('text-align:left', 'white-space:'+value))[0])

    def test_void_image_does_not_leak_code_exemption(self):
        html = '<section><img style="font-family:monospace;"><p><span leaf="">中文"引号"</span></p></section>'
        self.assertTrue(validate(html)[1])
        # Actual inline code is still exempt from punctuation checks.
        code = '<section><span style="font-family:monospace;"><span leaf="">中文"代码"</span></span></section>'
        self.assertEqual(validate(code)[:2], ([], []))

    def test_preview_only_wraps_valid_body_and_cannot_overwrite_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dest = Path(tmp)/'正文.html', Path(tmp)/'预览.html'
            src.write_text(CLEAN)
            command = [sys.executable, str(ROOT/'scripts/wrap_preview.py')]
            self.assertEqual(subprocess.run(command+[str(src),str(dest)], capture_output=True).returncode, 0)
            self.assertIn(CLEAN, dest.read_text())
            self.assertNotEqual(subprocess.run(command+[str(src),str(src)], capture_output=True).returncode, 0)
            self.assertEqual(src.read_text(), CLEAN)
            src.write_text('<html><body>'+CLEAN+'</body></html>')
            before = dest.read_text()
            self.assertNotEqual(subprocess.run(command+[str(src),str(dest)], capture_output=True).returncode, 0)
            self.assertEqual(dest.read_text(), before)


if __name__ == '__main__':
    unittest.main()
