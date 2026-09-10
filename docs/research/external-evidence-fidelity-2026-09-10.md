# #31：跨 Agent 证据保真有界调查

日期：2026-09-10。非规范研究材料；本轮仅 investigation，不进入 implementation。
维护基线：v0.14 / `5b01c5f5e5a730598cc0d545b673b8f93bd0a99c`。本轮只读比较确认生产文件与该基线无差异（Verified）。
来源：[Issue #31 正文](https://github.com/carllx/matt-browser-workflow/issues/31)、[历史回归评论](https://github.com/carllx/matt-browser-workflow/issues/31#issuecomment-5493982577)、[锁定 Spec](https://github.com/carllx/matt-browser-workflow/blob/5b01c5f5e5a730598cc0d545b673b8f93bd0a99c/chatgpt-project/browser-workflow-spec.md)、[锁定 Playbook](https://github.com/carllx/matt-browser-workflow/blob/5b01c5f5e5a730598cc0d545b673b8f93bd0a99c/chatgpt-project/browser-agent-playbook.md)。

## 证据边界

正文及评论内容存在已直接读取（Verified）；NotebookLM 日期、结构、概念及纠正后复犯属于历史用户报告（Reported）。未取得原始 synthesis、IDE 轨迹、source pages 或具体消费范围误写样本，相关成因 unknown/deferred，不能自行把全部错误成因或当前 v0.14 复发标 Verified。
主 Agent 本轮实际执行 `gh api repos/carllx/matt-browser-workflow/commits/{SHA}` 并整合输出，以下仅为2026-09-10时的解析结果（Verified），不证明历史生成错误的内部原因：

| 评论中的角色 | 原样标识符 | 本轮结果 |
| --- | --- | --- |
| 错误 head | `97363ce73663a825f75e24cb11649988b48624be` | HTTP 422、exit 1，No commit found |
| 错误 base | `707164536780dc964d4b17f54c9a81389bc7289f` | HTTP 422、exit 1，No commit found |
| 历史正确 head | `97363cedbd0f2cf34b152b3b7f66f74e83f15140` | exit 0，返回相同SHA |
| 历史正确 base | `70716452d14d6bf9e00f13a644214c71406dcacb` | exit 0，返回相同SHA |

本轮 `gh pr view 34` 返回已MERGED，head 为 `7effe658f0397a572290791a7267de6f3e4a2d6d`、base 为表中历史正确base（Verified）。历史 head 可解析不等于当前 PR head；不能用本轮解析结果证明当时只有一个 commit 或复原当时完整执行过程。复制机器值之后仍要核对其角色、时间与制品覆盖范围。

## 七项覆盖判断

| 调查点 | v0.14 已有覆盖（文本 Verified） | 调查结论（Inferred） |
| --- | --- | --- |
| 1. Reported 是否足够 | Spec 外部能力条款、Playbook §8/§12：合成保持 Reported，采纳后持久化 | 语义已足够禁止升级；缺的是该链路的具体失败示例，而非已证实的新 invariant 缺口。 |
| 2. claim promotion gate | Playbook §8：Verified 需独立核实；Spec 不允许合成自动提升 | `SOURCE-DIRECT` 等同义标签不能绕开既有判据；可用例子解释标签语义，不建立另一套 claim 状态机。 |
| 3. direct claim 最低证据 | 原始来源的独立核实与适用 provenance 已明确 | 重要 claim 应能定位实际来源内容、核对该内容支持的精确命题，并区分原文与现代术语解释；仅有 citation/page 字段不够。页面号不适用于所有来源，不要求通用固定 schema。 |
| 4. 纠正后同类错误与 Fresh | Playbook §13 已含混淆 Reported/Verified、无法保留结论等退化信号，并按阶段边界选择最轻操作 | 重犯可作为加强警示的例子；无法据报告诊断上下文退化，更不能自动要求 Fresh。还需排除纠正未传达、原始证据缺失等原因。 |
| 5. CONTINUE/NEW compact pattern | Spec Session Targeting 不变式及 Playbook §12 已要求明确会话目标与事实理由 | KEEP 现有模式；例子使用现有 `Continue current IDE session` / `Fresh IDE session`，不再增加另一组状态名称。 |
| 6. immutable IDs machine-copy | Spec pointer/delta、Playbook §12 审查引用绑定和远端核实 | 可增加研究示例说明直接复制机器输出并由接收端解析/核对角色；复制仅保护传输，不保证引用选对或仍是当前 head。当前证据支持示例，不足以要求全局新 invariant。 |
| 7. 消费关系与知识 scope ownership | Spec 项目能力声明归仓库，但仅声明项目用途/适用范围；位置不授予权限，外部能力非第四权威 | 项目可定义自己的消费子集，不能由该声明推导外部知识库只包含此范围，或项目拥有其内容/变更权限。适宜在示例区分消费范围、来源覆盖、修改授权。 |

## 最小处理与停止结论

**DOCS / EXAMPLE ONLY 是当前最小范围判断；没有新增生产 invariant 的充分依据。** “已有规则”不证明落实成功，历史违例也不自动证明规则语义缺失；本结论不表示根因已证或 #31 已全部完成。
- KEEP：证据三级、适用 provenance、会话独立判断、引用绑定、项目声明及外部权限边界。
- MODIFY 候选：后续若获实施授权，仅在现有说明附近解释合成经 IDE 重组/落盘后仍保持来源等级；不复制到多层规则。
- ADD 候选：最多两个示例——合成/现代术语被误标直接原文；机器引用在传递时损坏或历史 head 被当当前 head。重复纠正、消费范围作为前者的观察分支即可，无需新增系统。
- DELETE：候选中的强制 Fresh、新 session 状态名、全量 claim schema，以及“机器复制就足以 Verified”的推断。

示例验收应看最终标签、支持命题的来源核对、引用角色/时间及相称会话判断；不是看是否填满字段。本轮没有测试 NotebookLM、修改生产/Evals 或运行新回归；若要宣称 v0.14 当前失败，仍需绑定实际部署版本及原始动作证据。
