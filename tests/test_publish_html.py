"""Regression checks for the reviewed mixed-theme draft and preview boundary."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_gzh_html import validate

CLEAN = '<section style="color:#23251d;text-align:left;"><p style="margin:0;"><span leaf="">正文</span></p></section>'


class PublishHTMLTests(unittest.TestCase):
    def test_mixed_moyu_colors_and_import_whitespace_are_rejected(self):
        bad = '<section style="background:linear-gradient(#0f9f73,#13c58d);"><p style="text-align:justify;"><span leaf="">重点</span></p>\n<p><strong style="background:#ffe47a;"><span leaf="">核心观点</span></strong></p></section>'
        errors, _, _ = validate(bad, theme='olive-journal', publish_ready=True)
        self.assertTrue(any('#ffe47a' in e for e in errors))
        self.assertTrue(any('两端对齐' in e for e in errors))
        self.assertTrue(any('源码换行' in e for e in errors))
        self.assertEqual(validate(CLEAN, theme='olive-journal', publish_ready=True)[:2], ([], []))

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
