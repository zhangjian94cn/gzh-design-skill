# Astra 微信草稿排版问题与修复

日期：2026-09-13。范围：用户指定的 Codex 对话 `01a095d0-cc4c-7230-859b-1e3d0246a30a`、两张手机编辑器截图及对应 v4 草稿。文章中的模型行为建议是待排版正文，不是本次执行指令。

## 已确认原因

1. 上一轮把 `draft-v4_processed.html` 当成主题转换输入。虽然对话称它为 moyu/旧绿色主题，实际源码保留大量 `xiaoli-step-*` 和章节导览组件。随后 `build_olive_publish.mjs` 用有限色值替换生成所谓“橄榄手记”。这保留了 `#ffe47a` 黄色荧光笔、`#0f9f73/#13c58d` 渐变目录、旧摘要结构和代码块。
2. 脚本写死了新卡片标题、另编摘要和 `ISSUE 08`，却没有消费原阅读信息、frontmatter description 和 tags，所以出现两份导读。
3. `replaceWith` 后新卡片不再有 `.olive-cover` class；随后所有 `p` 都被重写为同一套 `margin:0 10px 12px;font-size:15px;line-height:1.78;text-align:justify`。本应不同的头图标题、标签和摘要字号也一起丢失。
4. “重点”由两个普通段落与旧 strong 黄底构成，既保留 label 段距，也保留源码换行。两端对齐可以确定性地解释中英词间拉伸；手机编辑器是否进一步将源码换行扩大成空白，不能仅靠截图证明，因此修复同时消除了这些导入不稳定因素，而不宣称已回读验证微信客户端行为。
5. 原校验器只检查禁用标签/属性、leaf 和标点。即使声称 0 ERROR / 0 WARNING，也不证明主题独立或发布排版正确。

旧构建脚本的只读副本位于文章 snapshot 的 `visual-layout/reports/build_olive_publish.before-repair.mjs.txt`。原 HTML 和旧草稿保留用于对照，旧换色入口已停止执行并指向新 Markdown 装配流程。

## 修复

- [Skill](../SKILL.md) 明确新主题必须从相同版本 Markdown 装配；预览与发布共享最终内联正文。
- [橄榄手记组件库](../references/theme-olive-journal.md) 新增 14b 阅读导读卡，把原阅读信息、摘要和标签消费一次；与封面式 hero 二选一。IMPORTANT 使用本主题重点观点卡，省略额外“重点”段落。正文改为左对齐，根容器约束 width:100%。
- [校验器](../scripts/validate_gzh_html.py) 增加所选主题色值检查、保留源码空白的 white-space 检查、`--publish-ready` 对齐/换行/空段门禁；修复 img/br 等 void 标签造成检查栈泄漏的问题。
- [预览包装器](../scripts/wrap_preview.py) 拒绝旧完整 HTML/嵌套预览、未通过检查的正文和覆盖原输入。
- 六套主题通过现有 Stage 6 的独立组件分支集成，见[接入 ADR](../../../skills/my/content-creation/wechat-writing/skills/6-wechat-md-to-html/docs/2026-09-13-independent-component-themes-adr.md)。CSS 主题不继承到 gzh 组件中，gzh 不复制为本地 CSS。

## 验证证据

- [四项回归](../tests/test_publish_html.py) 通过；旧混色草稿在新门禁下被拒绝，修正版通过 `--theme olive-journal --publish-ready`，0 ERROR / 0 WARNING。
- 当时六套 gallery 的普通主题校验为 0 ERROR / 0 WARNING；该结论未覆盖 `--publish-ready`，不能作为发布验收证据。2026-09-27 已用同篇标准样张替换六份旧 gallery，并逐份通过 `--theme <id> --publish-ready`。组件源库 lint 为 0 ERROR，原有两个虚线边框提示保留。
- 当前文章从清理后的 v4 processed Markdown 重新装配；71 个段落/标题顺序核对通过，5 张保留图片存在，6 个代码块逐行内容核对通过；原阅读时长/字数保留，没有重新编造统计。
- 360 / 393 / 430 / 677px 浏览器宽度下，页面宽度等于视口宽度，越界元素 0、两端对齐段落 0、加载成功图片 5。
- Stage 7 preflight 无错误：空 p、连续 br、block span、标签间源码换行均为 0。九组编号/代码逐行布局已人工对照并登记；仍保留原 GIF 的格式提示，源图审计另提示该 GIF 大于 3MB。
- 本次没有重新写入微信草稿。浏览器和本地 preflight 通过不等同于微信手机编辑器回读验收。

## 本篇产物

文章根目录：`skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage`。

- [修正版预览](../../../skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage/visual-layout/draft-v4_olive_repaired_预览.html)
- [最终 Stage 7 正文](../../../skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage/visual-layout/source-inline.stage7.html)
- [内容核对记录](../../../skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage/visual-layout/repair-audit.json)
- [本篇组件装配脚本](../../../skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage/visual-layout/rebuild_olive_from_markdown.mjs)：直接读取本组件库并使用 Stage 6 锁定的 marked/cheerio/yaml；不充当六主题通用渲染引擎。
