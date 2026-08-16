# Browser Workflow Spec

> 规范性需求单一事实源（Normative Requirements SSOT）
> 版本：v0.8
> 核心问题：我们为什么建立 `matt-browser-workflow`，它长期必须满足什么规范性要求？

---

## 1. 目标与定位 (Purpose & Mission)

`matt-browser-workflow` 旨在构建一套人机协同的高效工程工作流：
让位于网页端的 **Browser Lead**（如 ChatGPT / Claude Web）通过人类用户作为高信任中继，统筹指导本地端 **IDE Agent**（如 Antigravity / Cursor / Claude Code / Codex），并与代码托管平台及追踪器（如 GitHub Issues/PRs）协同完成复杂软件工程研发。

Matt 原生工程 Skills 的典型关系模型为 `Human ↔ Agent in working directory ↔ Repo / Runtime / Tracker`。本项目面临的实际关系模型是 `User ↔ Browser Agent ↔ IDE Agent ↔ Repo / Tracker`。Browser 与 IDE 拥有不同的 context、工具能力、事实位置和 feedback loop。

因此本项目存在的核心价值，不是再造一套 Matt workflow，而是：

> 在 User / Browser / IDE 分离的协作关系中，保护 Matt 的 decision ownership、primary-source continuity、feedback locality 与 durable artifacts。

---

## 2. 用户操作与交互原则 (User Operating Principles)

1. **服务非专业开发者**：面向普通用户时，输出应聚焦于"现在到哪、为什么、下一步是什么"，先给明确推荐和理由，少堆无意义缩写。
2. **就绪中继指令 (Copy-Ready Work Orders)**：当需要用户操作 IDE 时，Browser 必须提供易于一键复制、结构完整的独立工单（Work Order），避免用户拼凑散落指令。Work Order 在已有 self-contained Issue / Spec 时采用 pointer-first（传递 Issue/Spec 指针与 execution delta，而非复制完整上下文作为第二份 Spec SSOT）。
3. **消除双方信息差**：IDE 向 Browser 反馈时必须提供充分的执行证据（Evidence）；Browser 则在必要时向 IDE 提供充足的上下文边界。
4. **事实独立验证 (Evidence-Based Gate)**：Browser 严禁将 IDE Agent 的口头"完成"声明直接当作既定事实，必须区分 `Verified`、`Reported` 与 `Inferred`。
5. **Semantic vs Mechanical Human Relay**：
   - **应保留的 Semantic relay**：User decision、explicit authorization、user-invoked slash Skill、真正需要 Human participation 的 HITL exchange；
   - **应尽量减少的 Mechanical relay**：Agent 可自行取得的 SHA / Issue 内容 / tracker state / remote facts / logs / 可直接读取的 canonical artifacts；
   - 核心原则：**Preserve semantic human relay; minimize mechanical human relay.** Human 是 decision / trust boundary，不是首选 machine-to-machine transport layer。
6. **Feedback Locality（反馈就近原则）**：Fact / execution 应尽量靠近事实产生的位置处理：
   - remote / tracker / external facts → Browser 倾向自行取得；
   - working tree / runtime / local tests → IDE 倾向自行取得；
   - product / domain / risk / preference decision → User。
   若 Browser 需要 local fact，应向 IDE 发出**窄范围 Fact Probe**，而不是让 User 自己回答工程事实。这是 routing heuristic，不要建立 Fact Ownership Registry。
7. **极简演进与防过度设计 (Avoid Overdesign)**：
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
   - **Handoff（Matt `/handoff`）**：仅当真正需要 portability 时使用，例如：切换到新工具/harness、移动到新目录或仓库、将工作交接给同事、在阶段中途分叉侧任务且不打断当前主会话。普通 Browser → IDE Work Order relay **本身不是** Handoff 触发条件。
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
   以上默认映射是 session / work-unit 的参考基准，不构成固定的 Skill → Host mapping；实际 execution placement 仍依据 Relationship-First 判断（见 §10）。

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
   - 在对本 workflow 自身进行维护与迭代时，必须以**最后一个已接受并冻结的版本/引用（Last Accepted Ref，如 `v0.7`）**作为维护基准；
   - 正在编辑的工作区规则在未获 Review 与合并前，不得反向支配维护过程。

---

## 7. 项目绑定与权威层级 (Project Binding & Authority Layers)

1. **持久仓库绑定 (Project Repository Binding)**：
   - 每个 ChatGPT Project 默认绑定一个主代码仓库（Primary `PROJECT_REPO`），作为定位该 Project 权威事实的稳定实体标识指针（Project Identity Pointer）；
   - `PROJECT_DEFAULT_BRANCH`、`PROJECT_ACTIVE_REF` 与当前 Issue 属于动态易变的现场事实（Live State），严禁作为静态绑定参数持久写死。
2. **三层权威分立 (Three Authority Layers)**：
   - **Workflow Authority**：由 Project Sources 中的 `browser-agent-playbook.md` 与 `browser-workflow-spec.md` 定义跨端协作契约；
   - **Matt Process Authority**：由 Project Instructions 中的 `Release Dependency Lock`（`MAT_REPO @ MAT_REF : MAT_ROUTER_PATH`）定义技能原生行为规范。所有关键负载 Matt 源码检索必须经过 Ref 约束（Ref-Qualified），禁止使用浮动的 `main` 分支内容作为权威；冲突处理见下方 MAT_REF 权威边界规则；
   - **Project Authority**：由 `PROJECT_REPO` 坐标所指向的 live repo、tracker 与 `AGENTS.md` / `docs/agents/*` 定义项目自身事实与规则。
3. **MAT_REF 权威边界 (MAT Authority Precedence)**：
   区分两种情形：
   - **Accidental / undeclared divergence（无意漂移）**：若 IDE 本地 Skill 行为与 Release Dependency Lock 不一致，但目标项目的权威文档（`AGENTS.md` / `docs/agents/*`）没有明确声明这是有意定制，视为版本漂移（version drift）；Browser Review 以 locked `MAT_REF` 为准。
   - **Explicit project-local adaptation（明确适配）**：若目标项目的权威文档明确声明了某个 Matt 行为是有意覆盖/适配，则该**具体声明点**由 Project Authority 优先；但仅覆盖声明的具体行为，绝对不得静默替换整个工作流 Release 的 `MAT_REF`。若目标项目确实需要另一个完全不同的 Matt ref，将其归类为依赖分歧/兼容性决策并显式处理，严禁静默重定义 Matt Process Authority。
   **不使用**笼统的 `Project Authority > Matt Authority`；不引入 MAT_MODE、override registry 或额外配置体系。
4. **历史版本可复现性 (Old Release Reproducibility)**：
   - 后续 Matt 上游演进绝对不得修改已经发布的 `matt-browser-workflow` 版本的语义；
   - 历史 release 持续使用其不可变的发布锁定 `MAT_REF`；新工作流版本仅通过显式、经过完整 Review 的 Release 流程采纳新的 `MAT_REF`；严禁重写历史 tag 或 release。
5. **单项目优先**：当前工作流专注于单仓库主权绑定，暂不针对多仓库（Multi-repo）图谱做前置复杂抽象，待出现真实需求再行演进。

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

---

## 10. Relationship-First 协作关系感知 (Relationship-First Routing)

在设计工作路由或做出协作决策前，先判断当前协作关系的实际状态：

1. **User** 在当前工作中的角色是什么（decision maker / trust boundary / relay / observer）；
2. **Browser** 当前持有什么 reasoning / remote authority；
3. **IDE** 当前持有什么 working-tree / runtime facts；
4. **authoritative artifact** 在哪里（Issue / CONTEXT.md / branch / test evidence）；
5. 下一阶段需要保留哪个 context 作为 primary source。

不得为了机械保持 Browser → IDE 的固定流程而无意义地切断连续认知链条。**Canonical artifacts**（Issue / Map / Spec / CONTEXT.md / ADR / branch / diff / test evidence）是 Browser 与 IDE 跨 context 的稳定共享状态，跨 Agent 通信优先传递 pointer 与 execution delta，而不是复制另一份可能漂移的内容。

### Skill 执行位置启发规则

Browser 是 Workflow Steward，但**不是所有 Matt reasoning 的强制 Host**。Skill 的实际执行位置应根据以下因素就近判断，不建立固定 Skill → Host 静态 registry：

- **primary-source continuity**：若当前 primary reasoning 在 Browser 且下一阶段仍需要该推理链，优先 Continue；
- **feedback locality**：working-tree / runtime / test 反馈密集的工作倾向 IDE context 连续运行；remote / tracker / decision 密集的工作倾向 Browser-hosted cognition；
- **authoritative artifact locality**：Artifact 的位置用于判断 reading / reasoning 就近、feedback loop 充满度以及 Skill 执行放置；它本身 **不授予 mutation authority**。任何 mutation 仍必须遵循既有的 Browser / IDE Default Split、user authorization 和 Browser narrow/auditable mutation exceptions。
  > `Location informs placement; it does not grant authority.`
- **信息损耗成本**：不必要的跨端传递会引入漂移和误差，应最小化。

以下为参考性启发（非硬编码规则）：
- Small / well-scoped / local-feedback-heavy work → 倾向让相关 Matt flow 在 IDE context 连续运行；
- Huge / foggy / tracker-native / decision-heavy work → 倾向 Browser-hosted cognition。

### 演进审查的 Relationship-First 不变量 (Relationship-First Invariant)

所有未来的 Matt 依赖更新与工作流版本迭代，必须持续评估其对以下三端关系维度的影响：
- 用户决策与信任边界（User decision / trust boundary）
- Browser 工作流统筹与认知角色（Browser workflow / cognitive role）
- IDE 执行与运行时角色（IDE execution / runtime role）
- 调用所有权（Invocation Ownership）
- 权威一手源连续性（Primary-Source Continuity）
- 反馈局部性（Feedback Locality）
- 规范产物共享状态（Canonical Artifacts）
- 跨 Agent 语义与机械中继（Cross-Agent Semantic vs Mechanical Relay）
- 变更权限与位置分离（Mutation Authority vs Locality）
- 会话与上下文边界（Session & Context Stewardship）

该关系维度是永久性的架构审查轴线，而非单版本特性。

---

## 11. 上游演进治理规范 (Upstream Evolution Governance)

### 1. 上游漂移感知 (Upstream Detection)
在涉及 Matt 技能的完整启动导向期间，Browser 执行轻量级检测：
- 验证锁定 `MAT_REF` 与 `MAT_ROUTER_PATH` 可用性；
- 获取上游最新默认分支 `UPSTREAM_HEAD` 并比对 `MAT_REF...UPSTREAM_HEAD`；
- **核心原则**：检测仅用于感知漂移，**绝对不得自动修改或升级 `MAT_REF`**。目标项目工作采用有界相关性（Bounded Relevance），禁止会话间盲目重扫所有技能。

### 2. 候选版本冻结 (Candidate Freeze)
当上游漂移需要深入分析时，必须冻结不可变候选 SHA：
- `CURRENT_MAT_REF` = 当前发布锁定 SHA；
- `CANDIDATE_MAT_REF` = 观察到的上游候选 SHA。
一旦进入评审，禁止继续基于浮动的 `main` 分支分析，所有语义比对均严格在两者之间展开。

### 3. 技能清单差异与 10 维动态评审透镜
升级分析必须区分：**Added / Removed / Renamed / Changed / Unchanged**。重命名/移动检测结合标识符与语义防机械判定。
对受影响的技能，通过 10 维关系透镜进行评审：
1. **Identity**：旧/新名称与路径，增/删/改/移状态；
2. **Matt Flow Role**：router / main-flow / on-ramp / standalone / vocabulary layer / precondition；
3. **Invocation Authority**：user-invoked vs model-invoked、工具/内部调用、显式 slash 要求；
4. **Decision Ownership**：Agent 自行查证的事实 vs 需 User 裁决的决策；
5. **Primary-Source Continuity**：Continue / Fresh / Handoff / 上下文继承要求；
6. **Feedback Locality**：Browser/远程/Tracker 倾向 vs IDE/工作区/运行时/测试 倾向；
7. **Artifact Contract**：权威输入、持久输出、临时产物；变更权限与位置分离；
8. **Cross-Agent Relay**：保留语义中继，消除机械搬运；
9. **Skill Dependencies**：上下游依赖影响、调用边界变更；
10. **Workflow Adaptation Result**：`KEEP` / `MODIFY` / `DELETE` / `ADD`。

> **横切性语义影响 (Cross-Cutting Semantic Impact)**：
> 单个 Skill 即使自身 `SKILL.md` 无直接 diff，若候选版本变更了全局横切规范（调用模型、user/model-invoked 边界、内部调用约定、phase 边界/上下文规则、handoff 语义、setup 契约、tracker 契约、共享词汇等），该 Skill 仍须纳入重新评估。评估范围严格限定在受影响的技能上（candidate-scoped），严禁建立静态 Skill 映射表或永久兼容性数据库。

### 4. 适配精简与减法原则 (Adaptation Subtraction)
升级评审必须审查“可以删除什么适配”。若 Matt 上游已原生支持了此前工作流在本地适配的行为，应优先评估精简或删除本地规则。Matt 上游拥有 Matt 规范语义，本项目保持尽可能轻量。

### 5. 本地 IDE 对齐探测 (Local IDE Alignment Probe)
Browser 端的 `MAT_REF` 不能直接保证本地 IDE 执行完全相同的版本。在关键技能执行前且对齐状态未知时，Browser 发起窄范围 Fact Probe，探测安装来源、版本、关键技能可用性与对齐状态。
状态分类：`ALIGNED` / `UNKNOWN / FLOATING` / `DRIFTED NON-MATERIAL` / `DRIFTED MATERIAL`。仅当实质性漂移影响当前流程时才阻断。禁止要求用户手动搬运 IDE 自查事实；禁止建立 Fact Ownership Registry。

### 6. 冲突裁决规则 (Conflict Resolution)
- **A. Published MAT_REF vs Newer Upstream**：当前发布的 `MAT_REF` 保持绝对权威，上游仅作为候选参考。
- **B. MAT_REF vs IDE Local Matt**：非实质漂移报告证据不改权威；实质漂移严禁静默执行本地差异语义，必须显式对齐或升级。
- **C. Pinned Matt vs Project Authority**：延续既有规则，仅在项目明确声明的具体点由项目优先；未声明的差异仍视作漂移，以 Pinned Matt 为准。
- **D. New Matt Semantics vs Relationship-First Adaptation**：优先保全 Matt 语义意图并适配到三端拓扑。若存在真冲突，向用户呈现权衡决策（保持当前 vs 采纳升级并调整适配）。
- **E. Last Accepted Workflow vs In-Progress New Workflow**：以最后接受的冻结 release（如 `v0.7`）作为自维护基准；正在开发的分支不能反向支配当前开发。
- **F. Workflow Adaptation vs Upstream-Native Solution**：优先精简/移除冗余的本地适配，避免累积影子规范。

### 7. 用户分级通知与升级决策协议 (User Notification & Update Decision)
- **核心原则**：`Update notification != Upgrade decision.`（更新感知通知 ≠ 升级权衡决策）。工作流应主动探测并合理呈现 Matt 演进状态，但人类决策权严格保留给真正的权衡问题。无需引入复杂状态机。
- **非实质性上游漂移 (Non-Material Drift)**：检测到上游变动但判定无实质影响时，Browser 仅需简要提示上游存在新 commit 且当前锁定版本有效；**严禁**打断正常工作，**严禁**向用户索要升级决策。
- **实质性更新候选 (Material Update Candidate)**：发现实质价值或影响的候选时，Browser 必须先产出基于证据的升级简报（Upgrade Brief，包含当前/候选坐标、commit 与技能清单变动、实质语义与关系影响、适配调整建议及 `NO UPGRADE` / `DEFER` / `UPGRADE CANDIDATE` 分类），主动呈现给用户，由用户决定是否进入升级排期。
- **运行时完整性问题 (Runtime Integrity Problem)**：发现锁定源不可用、当前关键技能缺失或本地存在影响流程的 `DRIFTED MATERIAL` 时，Browser 必须将其作为**阻塞性兼容问题**立即呈现，提供具体事实与恢复方案。
