"""Readability-baseline checks in component_lint (justify + body font-size/line-height)."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from component_lint import body_typography_issue, lint_file, lint_text


def block(html):
    return '### 组件\n\n```html\n' + html + '\n```\n'


def errors(html):
    return [msg for level, msg in lint_text(block(html)) if level == 'ERROR']


BODY = '<p style="margin:0;font-size:{fs}px;line-height:{lh};color:#333;text-align:left;"><span leaf="">正文</span></p>'


class BaselineLintTests(unittest.TestCase):
    def test_justify_is_error(self):
        html = '<p style="font-size:15px;line-height:1.9;text-align:justify;"><span leaf="">正文</span></p>'
        self.assertTrue(any('justify' in m for m in errors(html)))

    def test_small_or_tight_body_is_error(self):
        self.assertTrue(errors(BODY.format(fs=14, lh=1.9)))
        self.assertTrue(errors(BODY.format(fs=15, lh=1.8)))
        self.assertTrue(errors(BODY.format(fs=16, lh=2.2)))

    def test_baseline_body_is_clean(self):
        for fs, lh in ((15, 1.85), (15, 1.95), (16, 2.0)):
            self.assertEqual(errors(BODY.format(fs=fs, lh=lh)), [], (fs, lh))

    def test_code_labels_and_centered_text_are_exempt(self):
        exempt = (
            "margin:0;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:13px;line-height:1.6;",
            'font-size:14px;font-weight:700;line-height:1.6;',
            'font-size:14px;line-height:1.7;text-align:center;',
            'font-size:12px;letter-spacing:1px;line-height:1.5;',
            'font-size:15px;line-height:1.6;text-decoration:line-through;',
            'display:inline-block;font-size:14px;line-height:1.8;',
        )
        for style in exempt:
            self.assertIsNone(body_typography_issue(style), style)

    def test_root_without_text_align_inherits_wechat_justify(self):
        card = '<section style="margin:0 0 24px;{align}"><p style="margin:0;font-size:15px;line-height:1.85;">' \
               '<span leaf="">卡片正文</span></p></section>'
        self.assertTrue(any('text-align' in m for m in errors(card.format(align=''))))
        self.assertEqual(errors(card.format(align='text-align:left;')), [])
        self.assertEqual(errors(card.format(align='text-align:center;')), [])
        # inline snippets (行内代码、高亮) sit inside a component that owns the alignment
        self.assertEqual(errors('<span style="font-size:14px;"><span leaf="">code</span></span>'), [])

    def test_line_owner_without_px_size_falls_back_to_wechat_17px(self):
        label = '<section style="text-align:left;{size}"><p style="margin:0 0 8px;">' \
                '<span style="display:inline-block;font-size:11px;"><span leaf="">标签</span></span></p></section>'
        self.assertTrue(any('17px' in m for m in errors(label.format(size=''))))
        self.assertEqual(errors(label.format(size='font-size:16px;')), [])
        relative = '<p style="font-size:1.1em;text-align:left;"><span leaf="">相对字号</span></p>'
        self.assertTrue(any('17px' in m for m in errors(relative)))
        svg = '<section style="text-align:left;"><svg><text font-size="9"><tspan leaf="">节点</tspan></text></svg></section>'
        self.assertEqual(errors(svg), [])

    def test_global_container_declares_alignment_and_base_size(self):
        shell = '<section style="max-width:677px;margin:0 auto;{extra}">\n  <!-- 所有组件放在这里 -->\n</section>'
        self.assertTrue(errors(shell.format(extra='')))
        self.assertTrue(errors(shell.format(extra='text-align:left;')))
        self.assertEqual(errors(shell.format(extra='text-align:left;font-size:16px;')), [])

    def test_shipped_libraries_have_no_errors(self):
        for path in sorted((ROOT / 'references').glob('*.md')):
            name, found = lint_file(path)
            self.assertEqual([m for level, m in found if level == 'ERROR'], [], name)


if __name__ == '__main__':
    unittest.main()
