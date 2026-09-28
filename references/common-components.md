# 通用增量组件库 —— 可读性基线 · 代码块 · 图片/GIF · 小标签标题 · 语义卡片

> **跨所有主题通用**。主题专属组件（引言卡、章节标题、签名等）读各自主题库；本文件提供**所有主题都需要**的共用部分：可读性基线（唯一规则来源）、代码块、图片/GIF、小标签标题，以及导读 / 行动建议 / 提示词 / 写法对照四类语义卡片骨架。各主题库只写自己的映射与配色，不重复这里的规则。
>
> **配色占位**：下面用红白色系（主色 `#DC2626`、浅底 `#FEF2F2`、浅标 `#FEE2E2`、深字 `#991B1B`）做示例。换其它主题时，把这几个值替换为该主题"设计变量速查表"里的对应色；代码块深色版各主题可共用，浅色版用主题主色做左竖条。
>
> **平台限制**：同主题库——禁 `<style>/<script>/class/id/div/position/float/@media/grid`，只用内联 + `flex`，文字全部 `<span leaf="">` 包裹。

---

## 〇、可读性基线（所有主题共同约束）

基线约束的是「好不好读」，不规定配色、字体与装饰——各主题的辨识度靠后者保留。任何主题的组件、映射与装配产物都必须满足下表；主题库与本表冲突时以本表为准。

| 项 | 基线 | 守护 |
|---|---|---|
| 对齐 | 正文、重点与各类卡片正文一律左对齐（`text-align:left` 或不写），**不用 `text-align:justify`** | `component_lint.py` / `validate_gzh_html.py --publish-ready` |
| 正文字号与行高 | 正文类段落 **≥15px**，行高 **1.85–2.0**；卡片里的正文同样适用。代码行（13px/1.6 等宽）、类型标签、图注、标题与居中金句不算正文 | `component_lint.py` |
| Part 前留白 | 章节（Part）标题前留白约一行（≥24px），只用 `margin` 表达，不用空段落或连续 `<br>` | `validate_gzh_html.py --publish-ready` |
| 卡片边界 | 重点、提示、行动建议、提示词卡与正文左右边界对齐：放在同一正文容器内，不另加左右外边距，也不比正文宽 | 装配后人工核对 |
| 标签 | 重点卡没有标题就不写类型标签，不留空标签、不用撑高的空元素 | 装配后人工核对 |
| 导读 | 全文**恰好一份**，只用原文的阅读信息、摘要（frontmatter `description`）与标签；没有摘要时整张省略，不生成空卡；主题有等价的导读/引言卡时用主题版，不重复 | 装配后人工核对 |
| 引语专属样式 | 斜体、居中、装饰引号与等宽字体只属于引语或代码，不串入行动建议、提示词、重点等卡片 | 装配后人工核对 |
| 调色板 | 强调色只取所选主题「设计变量速查表」与本文件的色值 | `validate_gzh_html.py --theme` |

摸鱼绿、摸鱼票据上游把正文定为 14px「铁律」；本 fork 按本基线统一提到 15px，偏离登记见 [fork 可读性基线偏离记录](../docs/2026-09-27-fork-readability-baseline-deviations.md)。

---

## 一、代码块组件（Markdown ``` 围栏 → 这里）

文章里的代码、命令、配置及依赖缩进的结构化 Prompt，**必须用代码块组件**，不要塞进普通段落或引用块；自然语言提示词用 4c 提示词卡。代码块内的英文、半角符号、缩进都要原样保留（代码不适用"中文全角标点"规则）。

### 1a. 深色代码块（默认，技术感强，适配所有主题）

```html
<section style="margin:0 0 20px;border-radius:8px;overflow:hidden;background:#1E293B;box-shadow:0 4px 16px -8px rgba(15,23,42,0.4);">
  <section style="display:flex;align-items:center;padding:9px 14px;background:#0F172A;">
    <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#FF5F56;margin-right:7px;font-size:0;line-height:0;overflow:hidden;">.</span>
    <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#FFBD2E;margin-right:7px;font-size:0;line-height:0;overflow:hidden;">.</span>
    <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#27C93F;font-size:0;line-height:0;overflow:hidden;">.</span>
    <span style="margin-left:12px;font-size:12px;color:#64748B;font-family:Consolas,Monaco,monospace;letter-spacing:1px;"><span leaf="">python</span></span>
  </section>
  <section style="padding:11px 14px;">
    <p style="margin:0;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:13px;line-height:1.6;color:#E2E8F0;"><span leaf="">def make_skill(name):</span></p>
    <p style="margin:0;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:13px;line-height:1.6;color:#E2E8F0;"><span leaf="">　　return f"已生成 {name}"</span></p>
    <p style="margin:0;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:13px;line-height:1.6;color:#E2E8F0;"><span leaf="">print(make_skill("gzh-design"))</span></p>
  </section>
</section>
```

要点（**关键，避免大段空白**）：① 顶栏三色圆点 + 语言名（无语言可删该 span）；② **每行代码用一个 `<p style="margin:0;...">`，不要用 `white-space:pre`**——否则 HTML 源码里 span 前的缩进和行间换行会被原样渲染成大左缩进 + 空行；③ 需要缩进时在 span 文字里用全角空格 `　`（不要靠源码空格）；④ 行距只靠 `line-height:1.6` 控制，padding 用 `11px 14px`，保持紧凑；⑤ 长行会自动换行，不溢出。

### 1b. 浅色代码块（适配浅色温和主题，如玫瑰粉/天蓝/焦糖棕）

```html
<section style="margin:0 0 20px;border-radius:8px;overflow:hidden;background:#F6F8FA;border:1px solid #E5E7EB;border-left:3px solid #DC2626;">
  <section style="padding:7px 14px;border-bottom:1px solid #E5E7EB;">
    <span style="font-size:12px;color:#9CA3AF;font-family:Consolas,Monaco,monospace;letter-spacing:1px;"><span leaf="">bash</span></span>
  </section>
  <section style="padding:11px 14px;">
    <p style="margin:0;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:13px;line-height:1.6;color:#24292F;"><span leaf="">npx skills add gzh-design</span></p>
  </section>
</section>
```

（左竖条 `#DC2626` 换成当前主题主色；多行同 1a：每行一个 `<p style="margin:0">`，不用 `white-space:pre`，缩进用全角空格 `　`。）

### 1c. 行内代码（正文中的 `code` 短片段）

```html
<span style="background:#F1F5F9;color:#DC2626;padding:1px 6px;border-radius:4px;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:14px;"><span leaf="">SKILL.md</span></span>
```

（文字色 `#DC2626` 换主题主色；底色保持中性浅灰。）

---

## 二、图片 / GIF 组件（Markdown `![](...)` → 这里）

文章里**每一处图片、GIF、截图占位都要保留并转成下面的组件**，不得遗漏；`src` 原样保留用户给的 URL 或相对路径。GIF 动图与普通图片都用 `<img>`（公众号原生支持 GIF 自动播放），区别只在加不加"动图"角标说明。

### 2a. 标准图片（带说明）

```html
<section style="background:#FFF;border-radius:12px;padding:6px;border:1px solid #E5E7EB;box-shadow:0 4px 12px -2px rgba(0,0,0,0.08);margin-bottom:8px;">
  <section style="margin:0;border-radius:8px;overflow:hidden;">
    <span leaf=""><img src="图片URL" style="max-width:100%;height:auto;display:block;margin:0 auto;"></span>
  </section>
</section>
<p style="font-size:12px;color:#9CA3AF;text-align:center;margin:0 0 24px;">
  <span leaf="">— 图片说明文字</span>
</p>
```

无说明文字时删掉下方 `<p>`，并把图片容器 `margin-bottom` 改回 `10px`。

> **图片尺寸自适应**：`<img>` 用 `max-width:100%;height:auto;display:block;margin:0 auto`——按图片自身尺寸显示并居中，大图缩到容器宽、小图保持原尺寸，**不用 `width:100%` 强制铺满**（小图被拉伸会糊）。

### 2b. GIF 动图（同图片，加"GIF 动图"角标）

```html
<section style="background:#FFF;border-radius:12px;padding:6px;border:1px solid #E5E7EB;box-shadow:0 4px 12px -2px rgba(0,0,0,0.08);margin-bottom:8px;">
  <section style="margin:0;border-radius:8px;overflow:hidden;">
    <span leaf=""><img src="动图URL.gif" style="max-width:100%;height:auto;display:block;margin:0 auto;"></span>
  </section>
</section>
<p style="text-align:center;margin:0 0 24px;">
  <span style="display:inline-block;background:#FEE2E2;color:#991B1B;font-size:11px;font-weight:700;padding:1px 8px;border-radius:4px;margin-right:6px;"><span leaf="">GIF 动图</span></span>
  <span style="font-size:12px;color:#9CA3AF;"><span leaf="">动图说明文字</span></span>
</p>
```

（角标底色 `#FEE2E2` → 主题浅底色，字色 `#991B1B` → 主题深字色，取自该主题"设计变量速查表"；无色块的极简主题改用细线描边胶囊：边框与字色用主题主色、背景透明。）若原文只写了图片但没给 URL，用 `src="图片URL"` 占位并在交付时提醒用户补图，**不要凭空编造图床链接**。

---

### 2c. 待补素材占位（**居中板块**，用于 GIF / 录屏 / 视频 / 成果图待补处）

文章里 `【插入xxx】`、待录屏、待补 GIF/视频/截图等占位，一律用这个**居中**板块，不要用左对齐的提示块。所有排版风格通用，浅底柔虚线框 + 居中图标与说明，一眼看出"此处待补"。

```html
<section style="margin:0 0 24px;padding:30px 20px;border:1.5px dashed #DAD7D2;border-radius:14px;background:#FAFAF8;text-align:center;">
  <p style="margin:0 0 10px;font-size:26px;line-height:1;"><span leaf="">🎬</span></p>
  <p style="margin:0;font-size:14px;font-weight:700;color:#9CA3AF;letter-spacing:1px;"><span leaf="">待补素材</span></p>
  <p style="margin:8px 0 0;font-size:13px;color:#B8B5B0;line-height:1.7;text-align:center;"><span leaf="">此处插入：创建 skill 的录屏演示</span></p>
</section>
```

- 图标按素材类型换：🎬 视频/录屏、🖼 图片、📊 信息图、📎 附件。
- 这是**唯一允许用虚线框（dashed）的场景**——因为它表达"占位/待补"语义，与正文强调用的小标签不冲突。
- 各主题可把虚线色/底色微调成主题中性色，但保持居中、留白、柔和。

---

## 三、小标签标题组件（突出标题/强调，**替代虚线框**）

> **设计取向**：强调一段内容或起一个小标题时，优先用下面的"小标签 / 左竖条"形式，**不要用四周虚线框（dashed）包一个标题**——虚线框笨重、抢戏。小标签更轻、更现代。
>
> **使用优先级**：先查所选主题库的映射规则——主题库有等价语义组件（自己的金句块/提示块/小标题）就用主题库版本保持气质一致；没有时才用本节组件并按下面规则换色。
>
> **换色规则**（示例为红白色值，按所选主题"设计变量速查表"替换）：
> - 3a 左竖条 `#DC2626` → 主题主色；3b 药丸底 `#DC2626` → 主题主色（字保持白）
> - 3c 序号药丸底 `#FEE2E2` → 主题浅底色，序号字 `#991B1B` → 主题深字色
> - 3d/3e 块底 `#FEF2F2` → 主题浅底色，竖条/类型标签 `#DC2626` → 主题主色
> - **无色块的极简主题**（留白禅意/石墨极简等）：3a 竖条细化为 `2–3px`，3d/3e 去掉底色、只留左竖条 + 大留白，贴合该主题气质。

### 3a. 左竖条小标题（最推荐，干净）

```html
<p style="margin:28px 0 14px;font-size:16px;font-weight:800;color:#1C1917;line-height:1.5;border-left:4px solid #DC2626;padding-left:12px;">
  <span leaf="">小标题文字</span>
</p>
```

### 3b. 药丸标签小标题（实色底，最醒目）

```html
<p style="margin:28px 0 14px;">
  <span style="display:inline-block;background:#DC2626;color:#FFFFFF;font-size:14px;font-weight:700;padding:5px 16px;border-radius:6px;"><span leaf="">小标题文字</span></span>
</p>
```

### 3c. 序号药丸 + 标题（清单/步骤）

```html
<p style="margin:24px 0 12px;font-size:15px;font-weight:800;color:#1C1917;line-height:1.6;">
  <span style="display:inline-block;background:#FEE2E2;color:#991B1B;border-radius:5px;padding:1px 9px;margin-right:8px;font-weight:900;"><span leaf="">01</span></span>
  <span leaf="">要点标题</span>
</p>
```

### 3d. 金句引用（左竖条版，取代旧的虚线框金句）

```html
<section style="margin:0 0 24px;background:#FEF2F2;border-radius:0 10px 10px 0;border-left:4px solid #DC2626;padding:16px 20px;">
  <p style="font-size:16px;font-weight:800;color:#991B1B;margin:0;line-height:1.8;">
    <span leaf="">「这里是核心观点或关键金句」</span>
  </p>
</section>
```

### 3e. 提示 / 旁注块（左竖条 + 类型小标签，取代旧的虚线提示框）

```html
<section style="margin:0 0 24px;background:#FEF2F2;border-radius:0 8px 8px 0;border-left:4px solid #DC2626;padding:14px 18px;">
  <p style="margin:0 0 6px;">
    <span style="display:inline-block;background:#DC2626;color:#FFFFFF;font-size:11px;font-weight:700;padding:2px 10px;border-radius:4px;letter-spacing:1px;"><span leaf="">提示</span></span>
  </p>
  <p style="font-size:15px;color:#374151;margin:0;line-height:1.85;">
    <span leaf="">提示或旁注的正文内容</span>
  </p>
</section>
```

类型小标签文字可换：`提示` / `注意` / `重点` / `旁注` 等（自然语言提示词用 4c）。整块**没有任何 dashed 边框**，靠左竖条 + 浅底 + 小标签区分层次。

---

## 四、语义卡片骨架（导读 · 行动建议 · 提示词 · 写法对照）

> 与第三节同一套形态：左竖条 + 浅底 + 类型小标签，正文走基线字号行高，全部 `<span leaf="">`。**使用优先级同第三节**：主题库映射表指定了等价组件就用主题版；没有才用下面骨架换主题色。
>
> **换色规则**沿用第三节：块底 `#FEF2F2` → 主题浅底色，竖条与实色标签 `#DC2626` → 主题主色，浅标签 `#FEE2E2`/`#991B1B` → 主题浅标色/深字色；正文 `#374151`、深字 `#1C1917`、弱化 `#9CA3AF` → 主题正文色/标题色/辅助色。4c 的中性浅底 `#F6F8FA`、描边 `#E5E7EB` 同 1b，各主题可共用。无色块的极简主题同样去掉块底、只留竖条。

### 4a. 导读卡（frontmatter 阅读时长 / `description` / `tags` → 这里）

```html
<section style="margin:0 0 32px;background:#FEF2F2;border-radius:0 8px 8px 0;border-left:4px solid #DC2626;padding:16px 18px;">
  <p style="margin:0 0 8px;font-size:12px;color:#9CA3AF;letter-spacing:1px;line-height:1.5;">
    <span leaf="">导读 · 约 6 分钟</span>
  </p>
  <p style="margin:0;font-size:15px;color:#374151;line-height:1.85;">
    <span leaf="">原文摘要（frontmatter description 原样，不另编）</span>
  </p>
  <p style="margin:10px 0 0;">
    <span style="display:inline-block;background:#FEE2E2;color:#991B1B;font-size:12px;padding:1px 8px;border-radius:4px;margin:0 6px 4px 0;"><span leaf="">标签一</span></span>
    <span style="display:inline-block;background:#FEE2E2;color:#991B1B;font-size:12px;padding:1px 8px;border-radius:4px;margin:0 6px 4px 0;"><span leaf="">标签二</span></span>
  </p>
</section>
```

放在正文第一段之前，全文一份。原文没有阅读时长就只写「导读」；没有标签删掉标签行；**没有摘要时整张卡省略**。

### 4b. 行动建议卡（`> [!行动]` / `> [!ACTION]` → 这里）

```html
<section style="margin:0 0 24px;background:#FEF2F2;border-radius:0 8px 8px 0;border-left:4px solid #DC2626;padding:14px 18px;">
  <p style="margin:0 0 8px;">
    <span style="display:inline-block;background:#DC2626;color:#FFFFFF;font-size:11px;font-weight:700;padding:2px 10px;border-radius:4px;letter-spacing:1px;"><span leaf="">行动建议</span></span>
  </p>
  <p style="margin:0 0 6px;font-size:15px;color:#374151;line-height:1.85;">
    <strong style="color:#DC2626;"><span leaf="">1　</span></strong><span leaf="">第一步做什么</span>
  </p>
  <p style="margin:0;font-size:15px;color:#374151;line-height:1.85;">
    <strong style="color:#DC2626;"><span leaf="">2　</span></strong><span leaf="">第二步做什么</span>
  </p>
</section>
```

原文是有序列表就逐条编号，只有一句就去掉序号直接写正文。

### 4c. 提示词卡（`> [!提示词]` / `> [!PROMPT]` → 这里）

```html
<section style="margin:0 0 24px;background:#F6F8FA;border:1px solid #E5E7EB;border-left:3px solid #DC2626;border-radius:0 8px 8px 0;padding:14px 18px;">
  <p style="margin:0 0 8px;">
    <span style="display:inline-block;background:#FEE2E2;color:#991B1B;font-size:11px;font-weight:700;padding:2px 10px;border-radius:4px;letter-spacing:1px;"><span leaf="">提示词</span></span>
  </p>
  <p style="margin:0;font-size:15px;color:#1C1917;line-height:1.85;">
    <span leaf="">自然语言提示词原文，整段可直接复制</span>
  </p>
</section>
```

用正文字体与基线字号，**不斜体、不等宽、不居中、不加装饰引号**；多段提示词每段一个 `<p>`（段间 `margin:0 0 8px`）。代码、命令或依赖缩进的结构化 Prompt 仍用 1a/1b。

### 4d. 写法对照（```` ```diff ```` 围栏 → 这里）

```html
<section style="margin:0 0 24px;background:#FEF2F2;border-radius:0 8px 8px 0;border-left:4px solid #DC2626;padding:14px 18px;">
  <p style="margin:0 0 8px;font-size:15px;color:#9CA3AF;line-height:1.85;">
    <span style="display:inline-block;background:#E5E7EB;color:#374151;font-size:11px;font-weight:700;padding:1px 8px;border-radius:4px;margin-right:8px;"><span leaf="">原写法</span></span><span style="text-decoration:line-through;"><span leaf="">diff 里 - 开头的旧句子</span></span>
  </p>
  <p style="margin:0 0 8px;font-size:15px;color:#1C1917;line-height:1.85;">
    <span style="display:inline-block;background:#DC2626;color:#FFFFFF;font-size:11px;font-weight:700;padding:1px 8px;border-radius:4px;margin-right:8px;"><span leaf="">改写</span></span><strong style="color:#991B1B;"><span leaf="">diff 里 + 开头的新句子</span></strong>
  </p>
  <p style="margin:0;font-size:15px;color:#374151;line-height:1.85;">
    <span leaf="">diff 里无前缀的上下文行（说明）</span>
  </p>
</section>
```

`-` 行 → 原写法（删除线 + 弱化色），`+` 行 → 改写（加粗 + 深字色），无前缀行 → 说明；**用正文字体，不用等宽代码块，不保留 `-`/`+` 符号**。多组对照重复前两行；没有说明行就删掉第三个 `<p>` 并把改写行 `margin` 改为 `0`。

---

## 五、窄屏数据表（主题没有原生表格时使用）

### 5a. 细线数据表（留白与票据主题的补充）

```html
<section style="margin:24px 0;overflow-x:auto;">
  <table style="width:100%;table-layout:fixed;border-collapse:collapse;font-size:15px;line-height:1.9;">
    <tr><th style="padding:10px 8px;border-bottom:2px solid #DC2626;color:#1C1917;text-align:left;"><span leaf="">列标题</span></th></tr>
    <tr><td style="padding:10px 8px;border-bottom:1px solid #E5E7EB;color:#374151;vertical-align:top;"><span leaf="">内容</span></td></tr>
  </table>
</section>
```

按实际列数复制单元格、按行数复制数据行；竖向对齐顶部，正文使用主题字体。仅按第四节配色规则填入本主题颜色。长词继承全局 `overflow-wrap:anywhere`，表格固定布局，不能靠整页裁切掩盖溢出。

---

## 选用速记

语义用途由 Stage 4 按内容标注（Agent 判断，脚本不猜）；`>` 本身只是块边界，不决定用途。

| 文章里出现 | 用哪个组件 |
|---|---|
| ` ``` 代码 / 命令 / 配置（含依赖缩进的结构化 Prompt）``` ` | 1a 深色（默认）或 1b 浅色代码块 |
| 行内 `` `code` `` | 1c 行内代码 |
| `![](图片)` | 2a 标准图片 |
| `![](xxx.gif)` 或注明动图 | 2b GIF 动图 |
| 想给一段起小标题 / 强调 | 3a 左竖条（首选）/ 3b 药丸 / 3c 序号 |
| 导读：frontmatter 阅读时长 / `description` / `tags` | 主题导读组件，无则 4a 导读卡（恰好一份，无摘要则省略） |
| 行动建议：`> [!行动]` / `> [!ACTION]` | 主题行动组件，无则 4b 行动建议卡 |
| 提示词：`> [!提示词]` / `> [!PROMPT]` | 主题提示词组件，无则 4c 提示词卡（正文字体，不斜体、不等宽） |
| 写法对照：```` ```diff ````（`-` 原写法，`+` 改写） | 4d 写法对照 |
| 重点：`> [!IMPORTANT]` / `> [!要点]` / `> [!TAKEAWAY]` | 主题重点组件，无则 3e（标签写「重点」） |
| 引语：`> [!金句]` | 主题金句/引语组件，无则 3d 金句左竖条块 |
| 提示 / 注意 / 旁注：`> [!NOTE]` / `> [!TIP]` / `> [!WARNING]` | 主题提示组件，无则 3e 提示左竖条块（**不要用虚线框**） |
