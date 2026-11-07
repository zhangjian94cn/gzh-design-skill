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
  - 线上继承（微信正文默认两端对齐、17px）→ ERROR：组件顶层块缺 text-align；
    承载文字的块自身和组件内祖先都没有 px 字号；全局容器缺 text-align 或 px 字号。

用法：
    component_lint.py [skill-dir]   # 默认当前目录
退出码：1 = 有 ERROR，0 = 通过。
"""

import glob
import os
import re
import sys
from html.parser import HTMLParser

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

# 线上继承检查：微信文章页正文容器 .rich_media_content 默认 text-align:justify、
# font-size:17px。组件里没有写明的对齐与字号，发布后都会落到这两个默认值。
INLINE_TAGS = {"span", "strong", "b", "em", "i", "u", "a", "code", "sub", "sup",
               "mark", "del", "s", "small", "font", "label", "br", "img"}
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "col"}
ABSOLUTE_SIZE = re.compile(r"^(?:[\d.]+px|0)$", re.I)


class _Node:
    __slots__ = ("tag", "style", "children", "parent")

    def __init__(self, tag, style, parent):
        self.tag, self.style, self.children, self.parent = tag, style, [], parent


def _declarations(attrs):
    attrs = dict(attrs)
    out = {}
    for part in (attrs.get("style") or "").split(";"):
        if ":" in part:
            key, value = part.split(":", 1)
            out[key.strip().lower()] = value.strip()
    size = (attrs.get("font-size") or "").strip()  # SVG 文字的字号写在属性上，单位为用户坐标
    if size and "font-size" not in out:
        out["font-size"] = size + "px" if re.fullmatch(r"[\d.]+", size) else size
    return out


class _Fragment(HTMLParser):
    """把组件 HTML 片段解析成节点树（只保留标签、style 与文本）。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = _Node("#root", {}, None)
        self.current = self.root

    def handle_starttag(self, tag, attrs):
        node = _Node(tag, _declarations(attrs), self.current)
        self.current.children.append(node)
        if tag not in VOID:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.current.children.append(_Node(tag, _declarations(attrs), self.current))

    def handle_endtag(self, tag):
        node = self.current
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self.current = node.parent

    def handle_data(self, data):
        if data.strip():
            self.current.children.append(data)


def _display(node):
    return node.style.get("display", "inline" if node.tag in INLINE_TAGS else "block").lower()


def _has_text(node):
    return any(isinstance(c, str) or _has_text(c) for c in node.children)


def _sized(node):
    """该节点的字号是否由组件内某个 px 声明决定（em/% 仍相对微信默认值）。"""
    while node is not None and node.tag != "#root":
        value = node.style.get("font-size")
        if value and ABSOLUTE_SIZE.match(value):
            return True
        node = node.parent
    return False


def _line_owners(node):
    """文字所在的行盒拥有者：块级元素、flex 子项和 inline-block 自身及其所在行。"""
    owners = []
    while node is not None and node.tag != "#root":
        display = _display(node)
        parent_flex = node.parent is not None and "flex" in _display(node.parent)
        if display == "inline" and not parent_flex:
            node = node.parent
            continue
        owners.append(node)
        if display.startswith("inline") and not parent_flex:  # inline-block 也坐在父元素的行里
            node = node.parent
            continue
        break
    return owners


def inheritance_issues(html, line):
    """返回会在微信线上继承正文默认对齐/字号的组件位置说明。"""
    tree = _Fragment()
    tree.feed(html)
    tree.close()
    issues = []
    for root in tree.root.children:
        if not isinstance(root, _Node) or _display(root) == "inline":
            continue
        if "max-width" in root.style:  # 全局容器：其余组件都放在它里面
            if "text-align" not in root.style or not _sized(root):
                issues.append(f"第 {line} 行全局容器未同时声明 text-align 与 px 字号：未写明的组件会落到"
                              "微信正文默认的两端对齐与 17px；写 text-align:left;font-size:16px")
        elif _has_text(root) and "text-align" not in root.style:
            issues.append(f"第 {line} 行组件顶层 <{root.tag}> 未声明 text-align：线上会继承微信正文默认的"
                          "两端对齐；顶层写 text-align:left（居中组件写 center）")
    flagged = set()

    def walk(node):
        for child in node.children:
            if isinstance(child, str):
                for owner in _line_owners(node):
                    if id(owner) not in flagged and not _sized(owner):
                        flagged.add(id(owner))
                        issues.append(f"第 {line} 行 <{owner.tag}> 未声明 px 字号且组件内无字号可继承："
                                      "线上会落到微信正文默认 17px，行高随之变大；写明设计字号")
            else:
                walk(child)

    walk(tree.root)
    return issues


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
        line = text.count("\n", 0, m.start(1)) + 1
        for msg in inheritance_issues(html, line):
            add("ERROR", msg)
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
