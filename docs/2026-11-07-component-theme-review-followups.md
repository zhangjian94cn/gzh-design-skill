# 组件主题审视后续：提示层级、表格列宽与无序列表

主仓主题对比页「微信阅读模拟」375px 下发现四个组件问题，本次在组件库源头修复，并按组件模板重写 [gallery](gallery/sample-article.md) 中受影响的块，同步更新相邻 `*.review.json` 指纹（`librarySha256`、`htmlSha256`）。

## 改动

- **红白提示层级**（[theme-red-white.md](../references/theme-red-white.md) 组件 9）：NOTE（8c 灰竖条）< TIP（新 9c 中性浅灰 + 「💡 提示」）< WARNING（9b 改为白底浅红描边 + 红竖条 + 实色「注意」标签，正文常规字重）< IMPORTANT（9a 不变）。红色只留给 WARNING / IMPORTANT 和结构。
- **石墨提示标签**（[theme-graphite-minimal.md](../references/theme-graphite-minimal.md) 组件 9）：9a 加 `KEY POINT`，9c 标签由错误的 `NOTE` 改为 `WARNING`，新增 9d 细竖条 `NOTE` / `TIP`；TIP 不再与 IMPORTANT 同为整段粗体。
- **表格**（红白、石墨、摸鱼绿 `<table>`，橄榄 22 号 flex 表）：表头 `word-break:keep-all`，列宽写在表头上按内容分配；数据单元格顶对齐、左右内边距 8px，不加 keep-all。
- **无序列表**（红白 11b、石墨 11b、摸鱼绿 11a）：pill-list 改为 bullet-list，主题色圆点 + 正文字号字重，条目间距 8px；有小标题时行首 `<strong>` 接说明，不做胶囊。

## 列宽取值

样张三列表在 375px 下逐一试了 24/46/30、22/46/32、22/44/34、24/42/34、23/43/34、22/42/36、24/44/32。只有 **23% / 43% / 34%** 能让四套主题同时满足：表头一行，单元格最多两行，行尾不剩单个汉字，英文单词不被拆开（摸鱼绿正文区最窄，为 303px）。模板说明写的是分配原则和 375px 检查项，不是固定比例。

## 验证

- `component_lint.py .`：0 ERROR（摸鱼绿、橄榄两条 dashed WARN 在 main 上已存在）。
- `validate_gzh_html.py --publish-ready`：五套在役样张全部通过；本仓 tests：16 passed。
- 集成仓 `gallery-review.mjs`：五套在役主题均通过原生部位与内容保真检查。
- 375px 微信阅读模拟截图：改前和改后的提示块、列表、表格都已逐项比对。

未验证：iPhone / 安卓微信真机渲染，以及编辑器保存后重开的效果。已退役的 `moyu-ticket` 样张在 main 上已经是过期状态，本次没有处理。
