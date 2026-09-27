# 语义排版、Part留白与图片锚点优化

日期：2026-09-13。用户反馈截图中的“引用”标签不适合行动建议/提示词、Part过密、行距偏紧、Stop hook配图位置不合适。

## 根因与处理

- [旧装配器](../../../skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage/visual-layout/rebuild_olive_from_markdown.mjs) 把所有非IMPORTANT的blockquote一律交给编者按且标题固定“引用”。现由Agent阅读后在 [本篇语义决定](../../../skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage/visual-layout/semantic-layout-review.json) 指定7块用途：使用者反馈、重点、写法对照、替换句式、写法对照、行动建议、提示词；源SHA变化即要求重新审阅，不用关键词分类器猜用途。
- [Skill](../SKILL.md) 与 [语义规则](../references/semantic-layout.md) 增加模型按内容决策的步骤。自然语言Prompt用可读提示词卡，代码/配置仍为逐行等宽代码；取消提示词整段斜体。已有CTA保持原文，无新增互动文案。
- [橄榄模板](../references/theme-olive-journal.md)：组件14c轻量行动卡、14d提示词卡；正文15px/1.95，Part顶部44px。原文章正文为15px/1.8、Part紧凑margin16px，新增28px约一行留白；不造空p/br。生成后不再覆盖正文的字号/行距，代码仍line-height1.6。
- 图片01实际为AGENTS加载链/32KiB截断，移至截断机制段后。
- 图片03实际为旧刹车与新交付规则对照，并非原图注所说的渐进披露目录；修正图注并移至Part01“拆旧刹车”结论后。
- 图片04实际为Stop hook运行流程，图中没有独立Verifier；修正图注，移至Part03 STEP02机制说明后、配置示例前。

## 结果与验证

[新预览](../../../skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage/visual-layout/draft-v4_olive_refined_预览.html)由Stage6验收后的新正文生成，发布与预览不混入旧CSS。

- builder内容断言：71段文字按原顺序，6段代码逐行保留，5图保留。图位/图注变动先落地新派生_processed.md，再针对它做Stage6 hash/图片序验收。
- gzh发布HTML检查0error/0warning；组件库lint0error、2项既有虚线框warning；上游4个与Stage6集成5个回归均通过。
- [手机实测](../../../skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage/visual-layout/reports/olive-refined-mobile-layout.json)：360/393/430/677无整页溢出，5图加载；3处Part间距44px，正文line-height1.95，通用“引用”标签0个。
- [行动/提示词截图](../../../skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage/visual-layout/reports/olive-refined-action-prompt-393.png)、[Stop hook图位截图](../../../skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage/visual-layout/reports/olive-refined-stop-hook-393.png)。

## 版本边界

模板优化阶段仅生成本地候选，未修改已经创建的微信草稿。旧olive_repaired HTML、冻结source-inline.stage7.html和平台回读证据保持原样；新候选以olive_refined命名。新图序不复用旧源文manifest。该阶段未消费上次已执行的草稿授权。

沿用[既有Spec](../../../specs/006-independent-wechat-themes/spec.md)的FR-010～FR-013/SC-005及T015～T018；没有新的架构边界变化，模型判断/脚本执行仍遵循既有ADR。


## 用户确认后的平台验收

用户随后明确回复“发布吧”。按既有草稿发布范围，新建 refined 版草稿，旧稿保留，未正式群发。新冻结输入直接采用已验收的 Stage6 正文，未覆盖旧冻结文件。平台回读确认5图、正文文字、图片锚点与样式一致，0错误0警告。

- 新 media_id：`rZQh871tux6JtPRQsjDlYksJZCYQlEpVfY44wss4beGpAputKy_bn_cRsUCBN2D8`
- [发布与回读证据](../../../skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage/reports/wechat-edge-draft-20260913T013727Z-6685df03e766.validation.md)
- [执行状态](../../../skills/my/content-creation/wechat-writing/snapshots/GeekZ知行录/20260912-gpt6-astra-usage/reports/olive-refined-edge.state.json)
