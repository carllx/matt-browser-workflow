# 文件规模与 Agent 可维护性：诊断底册

**Status: Research / Diagnostic Note — Non-normative**

本文记录研究结论、诊断方法和未来重新评估条件；不修改 v0.15 的任何规范、门禁或 600-Line Soft Guard。不构成第四权威、强制检查表或新的日志流程。

**Current disposition: KEEP v0.15.** 日期：2026-09-12。

## 1. 研究来源与证据边界

用户报告 Agent 持续向代码或 Markdown 追加内容，文件逐渐达到 600、800、1000 行以上。本轮从是否采用 fixed LOC threshold、Pre/Post/Stop Hook、CI、跨 Agent policy 和 complexity budget 出发，转向区分维护摩擦的原因。这些候选没有自动成为方案；用户描述是 Reported 症状，不是已复现的统一根因。

本记录承接[此前用户问题研究](user-problem-research-direction-2026-09-10.md)的文件结构、单次读取与 Session 分轨判断，聚焦 v0.15 下的文件规模和可维护性裁决，不替代旧底册的历史调查。引用资料在本轮咨询中已读取；论文结果仅为作者报告，未在本项目复现。

语义分类：发布内容与锁定源码为 Verified facts；文献结论为 source-reported evidence；诊断建议与反例为分析推论；KEEP 为本轮 Decision。下列建议均非新 Invariant。

## 2. 当前发布基线

本轮核实 remote main 与 v0.15 tag 均指向 `cddb5690829a825a2619345d6689b114d3a00ea7`；GitHub Release 为已发布、非 draft、非 prerelease。维护权威为 v0.15，`MAT_REF` 保持 `8b78b531ab965735c5dc74f6f7a219e1e37326df`。

[v0.15 Spec §4](https://github.com/carllx/matt-browser-workflow/blob/v0.15/chatgpt-project/browser-workflow-spec.md)明确将约 600 行作为人工编写代码及面向 Agent 文档的 soft warning，要求评估自然职责分离点，禁止机械碎片化；列有 generated、lockfiles、vendor、fixtures/snapshots 例外；超出 Issue 范围只报告，不顺手重构。Playbook §14 与 AGENTS §3.5 有对应表述。

因此，现行行为是软警示／针对性评估，不是 hard maximum 或 automatic split threshold。本轮另行判断：600 不能被当作 Agent capability boundary 或 architectural verdict；这不是声称发布原文逐字写出了本轮全部解释。例外也不能扩张为“凡 Agent 生成的业务代码均豁免”。

## 3. 支持的发现与保留的不确定性

| 主题 | 本轮判断 | 证据边界 |
| --- | --- | --- |
| File size | 廉价、低精度的风险信号，不能单独证明设计错误 | 定性定位；未测定本项目告警精度或最佳阈值 |
| Session degradation | 没有充分证据建立 `file > 600 lines → session degradation` | 文件组织、实际读取范围、累积上下文不是同一变量 |
| Depth | deep module 不等于 large file，反之亦然；内部可由多个文件组成 | 锁定 Matt 明确允许内部小模块；不是当前模型最优架构的实证结论 |
| Locality | 关注修改所需知识和验证是否合理局部化 | 跨文件修改和重读可能必要，不能只数次数 |
| Feedback availability | tests、type checking、build、runtime 与 acceptance evidence 的可得性影响维护难度 | “结构漂亮但反馈差，可能更难维护”是竞争解释，不是本项目已完成的对照实验 |

[SWE-agent 的 ACI 研究](https://arxiv.org/html/2405.15793v3)表明读取窗口和交互反馈可改变任务结果；读取窗口不是文件尺寸，不能据此规定 100 或 600 行文件上限。[RepoCoder](https://arxiv.org/abs/2303.12570)支持改进跨文件检索，不提供模块深度的对照结论。[Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)支持按需读取与持续筛选上下文，不提供统一文件行数断崖。

[Code for Machines, Not Just Humans](https://arxiv.org/abs/2601.02200)在竞争编程 Python 文件中研究可维护性指标与 AI 重构语义保持的关联，不能直接外推到长期多模块项目。[SWE-CI](https://arxiv.org/html/2603.03823v4)研究多轮维护与测试回归，仍非多年真实 Agent 维护的观察，也没有证明 deep modules 优于 small modules。

## 4. 目标与干预层级

更准确的问题是：**在保留必要行为、证据和授权边界的前提下，一次可信修改需要多少定位、读取、修改、验证、返工与人工纠偏？** 这不是新评分公式。必要读取、必要验证与合法跨层修改不属于浪费；先解释动作为何发生，再判断是否值得减少。

| 层级 | 所拥有的问题 |
| --- | --- |
| Workflow | 谁决定、谁执行、授权、证据、验证时机、stop/gate、Browser/IDE relationship |
| Target Repository | 领域职责、依赖、module design、测试、文档组织、项目特有 architecture contracts |
| Agent Host / Tool | search、retrieval、read window、output limits、cache、Hook protocol、context restoration、宿主执行能力 |

单项目维护困难不自动证明通用 Workflow 缺规则。Session Health、Repository Structure 描述问题；lint、CI、Hook、architecture tests 属于干预机制，不能据此建立三个平行治理子系统。检索与反馈工具也可能解释表面上的结构摩擦。

## 5. 可选诊断顺序

以下问题供出现真实摩擦时选择使用，不要求每次任务逐项回答：

1. 当前任务、目标、验收和有效状态是否清楚？
2. Agent 能否找到真正需要的信息？
3. 读取困难来自结构、搜索、截断、权限，还是上下文累积？
4. 修改为什么传播到这些文件／模块？
5. 传播是必要变化还是异常耦合？
6. 能否快速获得可信反馈，反馈是否覆盖真正验收？
7. 问题属于 Workflow、Repository、Host/Tool，还是多层或尚未知？
8. 最小有效干预是什么，包括“不改代码，只改善读取／反馈”？
9. 是否确实需要 executable enforcement，还是一次局部修复已经充分？

## 6. Matt 原文与本项目推论

锁定 [improve-codebase-architecture](https://github.com/mattpocock/skills/blob/8b78b531ab965735c5dc74f6f7a219e1e37326df/skills/engineering/improve-codebase-architecture/SKILL.md)明确支持 scope before scan、YAGNI、近期 hot spots、实际 friction 与避免 rigid heuristics。锁定 [codebase-design](https://github.com/mattpocock/skills/blob/8b78b531ab965735c5dc74f6f7a219e1e37326df/skills/engineering/codebase-design/SKILL.md)提供 Depth、Locality、Seam、Interface、Leverage、Deletion Test；Depth 关注调用者通过少量 interface 获得多少能力，而非 implementation LOC/interface LOC 比率。

“因此应取消 600”“因此应改名 Repository Legibility”“因此 deep module 最适合 AI”均为本项目可能提出的推论，不是 Matt 原文直接结论，本轮也不接受这些必然推导。读取源码是证据核对，不代表实际调用了其中 user-invoked 工作流。

Matt 方法论是分析镜头，不是对当前 Agent 最佳 architecture 的实证证明。Deletion Test 说明抽象是否承担复杂性，不保证它承担得正确；错误共享抽象也可能需要解开。[Sandi Metz 的反论](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction)支持在抽象错误时恢复局部重复，而非无条件集中实现。

## 7. 反例与 600 的地位

以下是诊断用假设场景，不是新执行过的 regression tests：

| 场景 | 有边界的判断 |
| --- | --- |
| 720 行、内聚、interface 稳定、locality 强、可靠测试、无自然 seam | 不能仅因超 600 自动拆；允许检查内部组织后保持完整 |
| 若干 150–250 行文件，共享隐藏状态、隐式顺序、频繁共同修改、难导航、弱测试 | 都低于 600 也可能有结构摩擦；不因此自动合并 |
| 合法 API migration 同时修改多个层 | change spread 本身不证明 architecture failure |

600 保持 v0.15 现有地位：用于提醒针对性检查的 soft warning。本轮不进一步降级、删除、硬化，也不改名为更宽的 Guard。[OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)确实包含 file-size limits，但不能证明普适阈值或本项目应采用硬门禁。

## 8. Code 与研究／Prose

二者共享 versioning、provenance、navigation、responsibility、verification，不共享统一拆分逻辑。source、concept、synthesis、teaching 是用途与关系，不必成为互斥文件箱；一篇完整论证合理地包含引文、分析与参考文献。

哲学原典、学术研究和备课优先分清版本／页码来源、quotation 与 paraphrase、解释归属、不确定性及教学简化；按真实 reuse/navigation 需要逐步抽取。固定 LOC、H2 数量、section count 或 atomic notes 不能替代这些判断。连续论证有时应保持完整。

[Red Hat Modular Documentation](https://redhat-documentation.github.io/modular-docs/)反对将旧文档切成无意义碎片；[Diátaxis](https://www.diataxis.fr/start-here/)区分读者需要，但不是全部学术知识的分类。TEI 的[异文处理](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/TC.html)及[不确定性与责任](https://tei-c.org/release/doc/tei-p5-doc/en/html/CE.html)提供来源治理视角；本轮不引入 XML 工具链或知识图谱。

## 9. Hook、CI 与增量基线

本轮不建设 Hook 或 CI enforcement。Hook 按实际宿主能力可以提供 early feedback、pause、evidence request、authorization gate 或 remediation guidance，不只有 ALLOW/DENY；这些角色不等于所有宿主协议兼容或本机已启用。Post 不自动回滚副作用；CI 的合入保障依赖实际 required checks、检查范围与候选绑定。能确定执行规则，不等于规则值得阻塞。

[Clean as You Code](https://docs.sonarsource.com/sonarqube-server/10.3/user-guide/clean-as-you-code)的增量治理值得借鉴，但不证明任意 LOC ratchet 有效：`850→852` 小修通常不启动架构工程；`0→730` 新文件值得检查；`420→900` 应关注新增职责与验证范围。持续小增量、移动与重命名也可能扭曲基线。

历史基线帮助选择何时检查，不能回答什么设计正确；不建立“只许变短”的规则。风险是否值得阻塞，还取决于真实后果、检测稳定性、误报成本、修复与例外路径及长期维护成本。

## 10. 未来案例记录与重新评估

可选最小记录提示如下，已有 output/commit/issue 可用链接代替重复抄写。Agent 可从现有上下文整理，用户不需填写模板；缺失项写 unknown，区分 Reported、Verified 和 Inferred，不补猜用户意图：

`Task | Symptom | Necessary reads | Change spread | Feedback availability | Rework/retries | Human correction | Root layer (Workflow/Repository/Host/multiple/unknown) | Intervention | Result`

该提示用于未来真实案例，不要求新增日志、Issue、监控或预先造实验。重新评估线索包括：同类维护失败反复出现；可观察的返工、漏改、验证失败或人工纠偏；能区分结构、读取、反馈与状态原因；最小干预的收益可能超过治理成本。

不同升格目标所需证据不同，不把线索变成全部必须满足的统一 Gate：

- 项目局部修复可由单项目直接事实支持，不必等待跨仓库复发。
- 通用 Workflow 修改需说明为何现有 v0.15 无法容纳正确处理；跨 repository 重复可增强普适性依据。
- executable enforcement 另需明确检测范围、稳定性、误报和合法例外，不能只凭“大文件”表象。

正式升格仍按既有 Durable Insight Promotion 判断，落到最窄正确位置；本记录不新增升格权限或程序。

## 11. 未得出的结论与最终处置

本轮没有确定 Agent 最佳文件长度、universal LOC threshold、最佳 AI-first architecture；没有实证证明 deep modules 优于 small modules，没有证明长文件导致上下文退化。没有认定 Hook 是通用解法、应建立 Complexity Score，或 Workflow 应承担所有 repository maintainability 问题。

**Decision: KEEP v0.15.** 不启动 v0.16，不新增 Hook、CI hard gate、Policy Engine、Complexity Score 或 Repository Legibility Guard。本轮价值是增加诊断能力，而不是增加规范。未来只有真实证据达到既有 Durable Insight Promotion 要求，才考虑将适用内容升格到 Spec、Playbook、AGENTS、eval 或 ADR；否则继续 KEEP。
