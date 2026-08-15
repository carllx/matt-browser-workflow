# PROJECT-SPEC.md

> 规范性需求单一事实源（Normative Requirements SSOT）
> 版本：v0.4
> 核心问题：我们为什么建立 `matt-browser-workflow`，它长期必须满足什么规范性要求？

---

## 1. 目标与定位 (Purpose & Mission)

`matt-browser-workflow` 旨在构建一套人机协同的高效工程工作流：
让位于网页端的 **Browser Lead**（如 ChatGPT / Claude Web）通过人类用户作为高信任中继，统筹指导本地端 **IDE Agent**（如 Antigravity / Cursor / Claude Code），并与代码托管平台及追踪器（如 GitHub Issues/PRs）协同完成复杂软件工程研发。

---

## 2. 用户操作与交互原则 (User Operating Principles)

1. **服务非专业开发者**：面向普通用户时，输出应聚焦于“现在到哪、为什么、下一步是什么”，先给明确推荐和理由，少堆无意义缩写。
2. **就绪中继指令 (Copy-Ready Work Orders)**：当需要用户操作 IDE 时，Browser 必须提供易于一键复制、结构完整的独立工单（Work Order），避免用户拼凑散落指令。
3. **消除双方信息差**：IDE 向 Browser 反馈时必须提供充分的执行证据（Evidence）；Browser 则在必要时向 IDE 提供充足的上下文边界。
4. **事实独立验证 (Evidence-Based Gate)**：Browser 严禁将 IDE Agent 的口头“完成”声明直接当作既定事实，必须区分 `Verified`、`Reported` 与 `Inferred`。
5. **极简演进与防过度设计 (Avoid Overdesign)**：
   - 坚持“先正确，再通用；先验证，再扩展；先解决当前阻塞”；
   - 严禁为尚未发生的场景预先引入复杂的代理抽象、多余文件或重型流程。

---

## 3. 上下文治理要求 (Context Requirements)

1. **双会话独立治理 (Dual-Session Context Stewardship)**：
   - Browser Session 与 IDE Session 是物理隔离的独立上下文空间；
   - 两端各自独立监控并评估其上下文健康度（Session Health），一端的切换/清理不应机械引发另一端的变动。
2. **阶段边界优先 (Phase Boundary Over Token Count)**：
   - 上下文的重置（Clear）、压缩（Compact）、交接（Handoff）或开启新会话（Fresh Session）应发生在明确的阶段边界（Phase Boundary）；
   - 严禁仅因对话长度增加而在阶段中途（Mid-Phase）随意切换。
3. **退化信号感知 (Context Degradation Signals)**：
   - 当观察到退化信号（如重复询问已知信息、推翻已定决策、遗忘活跃工作项、丢失验收标准、前后陈述矛盾、范围漂移、回复空洞泛化等）时，应在最近的合理阶段边界执行治理。
4. **独立工单新会话**：对于完全独立的 Issue、Ticket 或大型新阶段，推荐在阶段边界使用 Fresh Context / Fresh Session 启动。

---

## 4. 文件长度软警示 (File Context Guard)

1. **预警阈值非绝对上限**：约 **600 行**是人工编写代码及面向 Agent 文档的软性预警阈值（Soft Warning Threshold），而非不可逾越的硬性限制。
2. **评估拆分而非机械割裂**：当文件超过约 600 行时，应评估是否存在清晰自然的职责分离点；严禁为了单纯满足行数指标而破坏文档完整性进行机械碎片化拆分。
3. **合理例外**：自动生成文件、锁文件（lockfiles）、第三方代码（vendor code）、测试夹具（fixtures/snapshots）等不受此软限制约束。
4. **范围约束**：若拆分重构不属于当前 Issue 的明确范围，Agent 仅作报告，不顺手发起未经授权的重构。

---

## 5. 语言契约 (Language Contract)

1. **人类可读物料默认中文**：
   - GitHub Issue、PR 标题与描述、执行计划（Plan）、阶段报告（Report）、交接文档（Handoff）、IDE 运行反馈（Feedback）等人类可读材料，一律默认使用清晰流畅的简体中文。
2. **技术标识符保持规范英文**：
   - 代码标识符（变量名、函数名等）、文件路径、Shell 命令、API 接口、Git 引用及原始日志输出保持规范英文。

---

## 6. 记忆与自维护边界 (Memory & Self-Maintenance Boundaries)

1. **记忆边界 (Memory Boundary)**：
   - ChatGPT Project Memory 或聊天摘要是辅助性的检索参考（Useful Context），**不具备规范性权威（Normative SSOT）**；
   - 长期约束和工程事实必须沉淀在仓库文档（Repository Docs）及 Project Instructions 中，以仓库权威为准。
2. **自维护基线 (Self-Maintenance Boundary)**：
   - 在对本 workflow 自身进行维护与迭代时，必须以**最后一个已接受并冻结的版本/引用（Last Accepted Ref）**作为维护基准；
   - 正在编辑的工作区规则在未获 Review 与合并前，不得反向支配维护过程。
