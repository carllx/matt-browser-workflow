# Browser Workflow Spec

> 规范性需求单一事实源（Normative Requirements SSOT）
> 版本：v0.6
> 核心问题：我们为什么建立 `matt-browser-workflow`，它长期必须满足什么规范性要求？

---

## 1. 目标与定位 (Purpose & Mission)

`matt-browser-workflow` 旨在构建一套人机协同的高效工程工作流：
让位于网页端的 **Browser Lead**（如 ChatGPT / Claude Web）通过人类用户作为高信任中继，统筹指导本地端 **IDE Agent**（如 Antigravity / Cursor / Claude Code / Codex），并与代码托管平台及追踪器（如 GitHub Issues/PRs）协同完成复杂软件工程研发。

---

## 2. 用户操作与交互原则 (User Operating Principles)

1. **服务非专业开发者**：面向普通用户时，输出应聚焦于"现在到哪、为什么、下一步是什么"，先给明确推荐和理由，少堆无意义缩写。
2. **就绪中继指令 (Copy-Ready Work Orders)**：当需要用户操作 IDE 时，Browser 必须提供易于一键复制、结构完整的独立工单（Work Order），避免用户拼凑散落指令。
3. **消除双方信息差**：IDE 向 Browser 反馈时必须提供充分的执行证据（Evidence）；Browser 则在必要时向 IDE 提供充足的上下文边界。
4. **事实独立验证 (Evidence-Based Gate)**：Browser 严禁将 IDE Agent 的口头"完成"声明直接当作既定事实，必须区分 `Verified`、`Reported` 与 `Inferred`。
5. **极简演进与防过度设计 (Avoid Overdesign)**：
   - 坚持"先正确，再通用；先验证，再扩展；先解决当前阻塞"；
   - 严禁为尚未发生的场景预先引入复杂的代理抽象、多余文件或重型流程。

---

## 3. 上下文治理要求 (Context Requirements)

1. **双会话独立治理 (Dual-Session Context Stewardship)**：
   - Browser Session 与 IDE Session 是物理隔离的独立上下文空间；
   - 两端各自独立监控并评估其上下文健康度（Session Health），一端的切换/清理不应机械引发另一端的变动。
2. **阶段边界优先 (Phase Boundary Over Token Count)**：
   - 上下文治理应在明确的阶段边界（Phase Boundary）发生；
   - 严禁仅因对话长度增加而在阶段中途（Mid-Phase）随意切换。
3. **有序阶段边界策略 (Ordered Phase Boundary Operations)**：
   上下文切换遵循以下有序决策逻辑，依次评估：
   - **Continue**：若下一阶段仍需要当前深度推理链条，优先继续；
   - **Clear**：若当前上下文对下一阶段确实无价值，则清空；
   - **Handoff**：若需要跨端、跨工具、跨仓库或将工作交接给同事，才生成便携交接包；
   - **Subagent**：若任务独立且可 AFK 并行，才派遣子代理；
   - **Compact**：其他需要保留相关 context 但需要新空间的情况。
   Compact 不是首选项；Handoff 不是所有跨会话操作的默认选项。
4. **退化信号感知 (Context Degradation Signals)**：
   - 当观察到退化信号（如重复询问已知信息、推翻已定决策、遗忘活跃工作项、丢失验收标准、前后陈述矛盾、范围漂移、回复空洞泛化等）时，应在最近的合理阶段边界执行治理。
5. **Work-Unit ↔ Session 对齐 (Work-Unit to Session Alignment)**：
   Fresh Context 跟随自包含的认知/执行单元，而非机械跟随 tracker 对象。
   默认映射参考：
   - **Wayfinder decision ticket**：默认一个 ticket 对应一个 Fresh Browser Session；
   - **可独立执行的 implementation Issue**（由 `/to-tickets` 产生）：默认一个 Issue 对应一个 Fresh IDE Session；完成后该 IDE context 通常 disposable；
   - **Browser orchestration context**：可以跨多个 implementation Issues 继续，只要当前 context 仍是有价值的 primary source 且健康；
   - **grilling → spec / tickets 等依赖当前 primary reasoning 的连续阶段**：优先 Continue，不因 tracker object 边界机械 Clear；
   - **triage / discovery 等可批量处理多 Issue 的 flow**：不强制 Issue:Session 1:1；
   - **Browser Session 与 IDE Session 生命周期独立**：一端 Clear/Fresh 不机械触发另一端。

---

## 4. 文件长度软警示 (File Context Guard)

1. **预警阈值非绝对上限**：约 **600 行**是人工编写代码及面向 Agent 文档的软性预警阈值（Soft Warning Threshold），而非不可逾越的硬性限制。
2. **评估拆分而非机械割裂**：当文件超过约 600 行时，应评估是否存在清晰自然的职责分离点；严禁为了单纯满足行数指标而破坏文档完整性进行机械碎片化拆分。
3. **合理例外**：自动生成文件、锁文件（lockfiles）、第三方代码（vendor code）、测试夹具（fixtures/snapshots）等不受此软限制约束。
4. **范围约束**：若拆分重构不属于当前 Issue 的明确范围，Agent 仅作报告，不顺手发起未经授权的重构。

---

## 5. 语言契约 (Language Contract)

1. **人类可读物料默认中文**：
   - GitHub Issue、PR 标题与描述、执行计划（Plan）、阶段报告（Report）、Session Checkpoint / Snapshot、IDE 运行反馈（Feedback）等人类可读材料，一律默认使用清晰流畅的简体中文。
2. **技术标识符保持规范英文**：
   - 代码标识符（变量名、函数名等）、文件路径、Shell 命令、API 接口、Git 引用及原始日志输出保持规范英文。

---

## 6. 记忆与自维护边界 (Memory & Self-Maintenance Boundaries)

1. **记忆边界 (Memory Boundary)**：
   - ChatGPT Project Memory 或聊天摘要是辅助性的检索参考（Useful Context），**不具备规范性权威（Normative SSOT）**；
   - 长期约束和工程事实必须沉淀在仓库文档（Repository Docs）及 Project Instructions 中，以仓库权威为准。
2. **自维护基线 (Self-Maintenance Boundary)**：
   - 在对本 workflow 自身进行维护与迭代时，必须以**最后一个已接受并冻结的版本/引用（Last Accepted Ref，如 `v0.5`）**作为维护基准；
   - 正在编辑的工作区规则在未获 Review 与合并前，不得反向支配维护过程。

---

## 7. 项目绑定与权威层级 (Project Binding & Authority Layers)

1. **持久仓库绑定 (Project Repository Binding)**：
   - 每个 ChatGPT Project 默认绑定一个主代码仓库（Primary `PROJECT_REPO`），作为定位该 Project 权威事实的稳定实体标识指针（Project Identity Pointer）；
   - `PROJECT_DEFAULT_BRANCH`、`PROJECT_ACTIVE_REF` 与当前 Issue 属于动态易变的现场事实（Live State），严禁作为静态绑定参数持久写死。
2. **三层权威分立 (Three Authority Layers)**：
   - **Workflow Authority**：由 Project Sources 中的 `browser-agent-playbook.md` 与 `browser-workflow-spec.md` 定义跨端协作契约；
   - **Matt Process Authority**：由 `MAT_REPO @ MAT_REF`（Release 默认锚定 `MAT_REF=8b78b531ab965735c5dc74f6f7a219e1e37326df`）定义技能原生行为规范。不得隐式假定本地 IDE 安装版本完全一致，冲突时以 Pinned 原文为准；
   - **Project Authority**：由 `PROJECT_REPO` 坐标所指向的 live repo、tracker 与 `AGENTS.md` / `docs/agents/*` 定义项目自身事实与规则。
3. **MAT_REF 权威边界 (MAT Authority Precedence)**：
   区分两种情形：
   - **Accidental / undeclared divergence（无意漂移）**：若 IDE 本地 Skill 行为与 pinned `MAT_REF` 不一致，但目标项目的权威文档（`AGENTS.md` / `docs/agents/*`）没有明确声明这是有意定制，视为版本漂移（version drift）；Browser Review 以 pinned `MAT_REF` 为准。
   - **Explicit project-local adaptation（明确适配）**：若目标项目的权威文档明确声明了某个 Matt 行为是有意覆盖/适配，则该**具体声明点**由 Project Authority 优先；其他未声明的 Matt 行为仍遵循 pinned `MAT_REF`。
   **不使用**笼统的 `Project Authority > Matt Authority`；不引入 MAT_MODE、override registry 或额外配置体系。
4. **单项目优先**：当前工作流专注于单仓库主权绑定，暂不针对多仓库（Multi-repo）图谱做前置复杂抽象，待出现真实需求再行演进。

---

## 8. Domain Modeling 成果持久化 (Domain-Modeling Persistence)

1. **不得仅留在 Browser conversation**：Browser-hosted grilling / decision work 若产生了真正的 domain-modeling 成果（术语定义、命名共识、关键架构决策），不得仅停留在 Browser 会话中。
2. **及时建立 repository persistence**：
   - 若 Browser 拥有明确的用户授权及适当的 remote write capability，可进行窄范围、可审计的写入；
   - 否则 Browser 应立即向 IDE 下发最小 persistence Work Order（如更新 `CONTEXT.md` glossary 或创建 ADR）；
   - 不得把所有 `CONTEXT.md` / ADR 更新机械积压到阶段末尾。
3. **文档职责边界**：
   - `CONTEXT.md` 只承担 glossary / domain language；
   - ADR 只用于真正符合条件的重大、难逆、具有 trade-off 的决定；
   - 普通讨论记录不得强行写成 ADR。

---

## 9. 仓库级前置条件 (Repository-Level Prerequisites)

Matt engineering workflow 的仓库级配置前置条件（如 `/setup-matt-pocock-skills` 所生成的 `docs/agents/*` 及 `AGENTS.md` 规则块）应严格遵循 pinned `MAT_REF` 的官方 Skill 原生规范，而非由本项目另行复制一套实现。此类必要的工程配置不计入核心交付文件，亦不属于过度设计。
