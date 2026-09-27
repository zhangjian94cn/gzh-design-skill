#!/usr/bin/env python3
"""组件库源头检查器 —— 可验证循环的第一道关。

扫描 references/ 下所有组件库 .md 里的 ```html 代码块，检测会导致
排版问题的反模式。只看真实组件 HTML，不被说明文字干扰（grep 做不到）。

与 validate_gzh_html.py 配合构成闭环：
  改组件库 → component_lint.py 扫源头 → 生成产物 → validate_gzh_html.py 扫产物 → 修 → 重复

可读性基线（common-components.md「可读性基线」为唯一规则来源）的源头检查：
  - 任何 text-align:justify → ERROR（正文与重点不两端对齐）。
  - 正文类 <p>：字号 13–14px 且行高 ≥1.6（多行正文意图）→ ERROR，应提到 15px；
    字号 15–17px 且写了行高但不在 1.85–2.0 → ERROR。
    豁免（不是正文）：等宽代码行、inline-block 标签、加粗（bold/≥600）标题与卡片标题、
    居中说明/金句、删除线旧写法、letter-spacing ≥1px 的英文标签、字号 <13px 或 >17px、
    未写字号（继承容器）的 <p>。

用法：
    component_lint.py [skill-dir]   # 默认当前目录
退出码：1 = 有 ERROR，0 = 通过。
"""

import glob
import os
import re
import sys

CJK = re.compile(r"[一-鿿㐀-䶿]")

# (正则, 级别, 说明) —— 在每个 ```html 组件块内检查
CHECKS = [
    (re.compile(r"white-space\s*:\s*pre", re.I), "ERROR",
     "用了 white-space:pre —— 会把 HTML 源码缩进/换行渲染成大左缩进+空行；"
     "代码块改成每行一个 <p style=\"margin:0\">，缩进用全角空格"),
    (re.compile(r"</?div[\s>]", re.I), "ERROR", "出现 <div>，应用 <section>"),
    (re.compile(r"\sclass\s*=", re.I), "ERROR", "出现 class 属性（会被公众号剥离）"),
    (re.compile(r"\sid\s*=", re.I), "ERROR", "出现 id 属性"),
    (re.compile(r"<style[\s>]", re.I), "ERROR", "出现 <style> 标签"),
    (re.compile(r"position\s*:\s*(fixed|absolute|sticky)", re.I), "ERROR",
     "position fixed/absolute/sticky 不被支持"),
    (re.compile(r"display\s*:\s*grid", re.I), "ERROR", "display:grid 不被支持"),
    (re.compile(r"var\s*\(\s*--", re.I), "ERROR", "用了 CSS 变量 var(--x)"),
    (re.compile(r"@(media|keyframes|import)", re.I), "ERROR", "@media/@keyframes/@import 不被支持"),
    (re.compile(r"text-align\s*:\s*justify", re.I), "ERROR",
     "用了 text-align:justify —— 违反可读性基线（中英混排会被拉开字距），改为 left"),
]

P_STYLE = re.compile(r"<p\b[^>]*?\bstyle\s*=\s*\"([^\"]*)\"", re.I)
BODY_EXEMPT = re.compile(
    r"monospace|consolas|sf mono|courier|display\s*:\s*inline-block|"
    r"font-weight\s*:\s*(bold|[6-9]00)|text-align\s*:\s*center|"
    r"text-decoration\s*:\s*line-through", re.I)
FONT_SIZE = re.compile(r"font-size\s*:\s*([\d.]+)px", re.I)
LINE_HEIGHT = re.compile(r"line-height\s*:\s*([\d.]+)\s*(?:;|$)", re.I)
LETTER_SPACING = re.compile(r"letter-spacing\s*:\s*([\d.]+)px", re.I)


def body_typography_issue(style):
    """返回正文类 <p> 的基线违规说明；非正文或合规返回 None。"""
    if BODY_EXEMPT.search(style):
        return None
    ls = LETTER_SPACING.search(style)
    if ls and float(ls.group(1)) >= 1:
        return None
    fs = FONT_SIZE.search(style)
    if not fs:
        return None
    size = float(fs.group(1))
    lh_m = LINE_HEIGHT.search(style)
    lh = float(lh_m.group(1)) if lh_m else None
    if 13 <= size < 15 and lh is not None and lh >= 1.6:
        return (f"正文段落 {size:g}px/{lh:g} 低于可读性基线（正文 ≥15px、行高 1.85–2.0）")
    if 15 <= size <= 17 and lh is not None and not 1.85 <= lh <= 2.0:
        return (f"正文段落 {size:g}px 行高 {lh:g} 不在可读性基线 1.85–2.0 内")
    return None


# 四周虚线框：border: ... dashed（不含方向，如 border-left dashed 不算）
FOURSIDE_DASHED = re.compile(r"border\s*:\s*[^;{}]*dashed", re.I)
CENTERED = re.compile(r"text-align\s*:\s*center", re.I)


def lint_text(text):
    """检查一份组件库 Markdown 文本，返回 [(level, msg)]（按说明去重）。"""
    found = []  # (level, msg)
    seen = set()

    def add(level, msg):
        if msg not in seen:
            seen.add(msg)
            found.append((level, msg))

    for m in re.finditer(r"```html\s*\n(.*?)```", text, re.S):
        html = m.group(1)
        for rx, level, msg in CHECKS:
            if rx.search(html):
                add(level, msg)
        # 四周虚线框：正文强调勿用；居中块视为"占位/素材"组件，豁免
        if FOURSIDE_DASHED.search(html) and not CENTERED.search(html):
            add("WARN", "四周虚线框 border:…dashed（正文强调请用左竖条；"
                        "仅居中的素材占位块可用 dashed）")
        for pm in P_STYLE.finditer(html):
            issue = body_typography_issue(pm.group(1))
            if issue:
                add("ERROR", issue)
    return found


def lint_file(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    name = os.path.basename(path).replace("公众号排版组件库 —— ", "").replace(".md", "")
    return name, lint_text(text)


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    refs = sorted(glob.glob(os.path.join(root, "references", "*.md")))
    if not refs:
        print(f"未找到 {root}/references/*.md")
        sys.exit(1)

    total_err = total_warn = clean = 0
    print(f"📐 组件库源头检查：{len(refs)} 个库\n")
    for path in refs:
        name, found = lint_file(path)
        if not found:
            clean += 1
            continue
        errs = [m for lv, m in found if lv == "ERROR"]
        warns = [m for lv, m in found if lv == "WARN"]
        total_err += len(errs)
        total_warn += len(warns)
        print(f"── {name} ──")
        for m in errs:
            print(f"   ❌ {m}")
        for m in warns:
            print(f"   ⚠️  {m}")

    print(f"\n汇总：{clean}/{len(refs)} 个库干净，ERROR×{total_err}，WARN×{total_warn}")
    if total_err == 0 and total_warn == 0:
        print("✅ 全部组件库源头无反模式")
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()
