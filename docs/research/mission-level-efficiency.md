# Research Dossier: Mission-Level Efficiency, Configuration Layering & Long-Term Regression Guards

> **状态**：非规范性研究底册（Non-Normative Research Ledger / Design Rationale）  
> **关联议题**：Part of #32, Implementation of #33, Follow-up to #14 & #17  
> **权威声明**：本文件记录研究背景、一手信源依据、推导逻辑、事实状态、被否定方案、研究前沿与演进触发点，**不构成 Workflow Authority，亦非第四 SSOT**。规范性需求与不变式归属于 `browser-workflow-spec.md`，操作指引归属于 `browser-agent-playbook.md`。

---

## 1. 背景与问题溯源 (Problem Statement & Empirical Failures)

在 Browser Workflow 演进至 v0.12 后，跨端协作在正确性、证据链（Evidence-Based Verification）、门禁保真度（Skill Gate Fidelity）、发布接受边界（Release Acceptance Boundary）和权限划分（Default Split）上建立了严格的规范。然而，在真实工程实践中，大模型频繁表现出**过度注重局部步骤周全性、忽视整体任务交付效率（Ceremony-Heavy Local Optimization）**的系统性退化。

### 真实典型失败模式与事实归属

1. **小而明确的任务过度打磨 (100→110 Polishing)** `[Verified]`：
   - 面对已明确界定范围的小型任务（例如修复单行配置、增补已确定的术语词条、执行针对性测试），Agent 在达成既定完成门禁（Completion Gate）后，仍自发发起多余的深度拓展调研、全量文档重构、多轮无新信息的自我审查或冗长汇报，导致流程成本远超问题本身的工程价值（`process cost >> problem value`）。
2. **独立并行候选被人为串行化 (Artificial Serialization)** `[Verified]`：
   - 面对多个在逻辑上互不阻塞、共同服务于下游单一决策的独立实验或调研分支（如 A/B/C 三种技术方案的独立探针），Agent 习惯性采用 `A 执行 → A 独立总结汇报 → 用户/Browser 确认 → B 执行 → B 独立总结汇报 → ...` 的串行流水线，引入大量的空等与人工中继损耗。
3. **已知 IDE 并行能力闲置 (Unused Harness Leverage)** `[Verified]`：
   - 在已明确知道当前 IDE Harness 原生支持子代理（Subagents）、后台任务（Background Tasks）或多会话（Multi-Session）并发执行时，Browser 在派发 Mission Contract 时仍默认以单线思维组织任务，未主动释放并行的执行杠杆。
4. **对“IDE 拥有拓扑权属”的消极误读 (Misinterpreting Topology Ownership)** `[Verified]`：
   - 规则明确规定“IDE 拥有内部任务分解与执行拓扑权属，Browser 不做微观调度”。部分模型将其机械反向误读为“Browser 应该对明显的并行杠杆与独立分支保持沉默”，放弃了在目标和契约层面识别依赖关系与并行候选（Parallel Candidates）的统筹职责。

---

## 2. 一手信源、先验事实与理论依据 (Primary Sources & Provenance)

### A. 锁定的 Matt 上游一手源 (Locked Matt Primary Sources)
基准引用：`mattpocock/skills @ 8b78b531ab965735c5dc74f6f7a219e1e37326df`
- **`skills/engineering/ask-matt/SKILL.md`** `[Verified]`：路由器 SSOT。明确限定 `/wayfinder` 仅适用于 huge / foggy / multi-session 任务（强调“slower and denser, never a well-scoped feature”）；明确 `/research` 是后台并发代理调研。
- **`.agents/invocation.md`** `[Verified]`：调用权限唯一事实源。严格规定 `user-invoked` 技能只能由人类用户显式输入名称触发（human typing its name），模型不得自主触达；模型内部调用仅限于 `model-invoked` 技能。
- **`skills/engineering/ask-matt/PHASE-BOUNDARIES.md`** `[Verified]`：阶段边界决策树。确立 `Continue → Clear → Handoff → Subagent → Compact` 优先级，强调以最低摩擦和保护一手源连续性（Primary-Source Continuity）为准绳。
- **`skills/engineering/to-tickets/SKILL.md`** `[Verified]`：工单依赖模型。生成自包含 tickets 并通过 issue dependencies 显式声明阻塞边（blocking edges）；无 blocker 的 ticket 可独立/并发推进。
- **`skills/engineering/research/SKILL.md`** `[Verified]`：调研制品契约。定义把 reading legwork 派发给 background agent、主线继续工作，并输出包含引用的 Markdown durable artifact。

### B. 仓库历史演进与工程事实 (Repository Historical Evidence)
- **GitHub Issue #14** `[Verified]`：IDE Harness Capability 与并行执行调研，确立了 Dependency-First 与环境能力感知原则；
- **GitHub Issue #17** `[Verified]`：确立 Mission Contract 语义与 IDE 内部执行拓扑自治权；
- **GitHub Issue #32** `[Verified]`：根本原因溯源：分析为何已有 Proportionality 仍无法阻止 100→110 形式主义，推导关键路径与边际价值公理；
- **GitHub Issue #33** `[Verified]`：本项实现工单：落实 Mission-Level Efficiency 默认值、配置分层与长期回归守护。

### C. 外部理论与工程方法依据（咨询性参考，非规范权威）
- **关键路径法 (Critical Path Method, CPM)** `[Reported]`：在拓扑图的所有合法路径中，总工期由关键路径决定；非关键路径上的局部过度优化无法缩短整体交付周期。
- **阿姆达尔定律与并发加速 (Amdahl's Law)** `[Reported]`：系统整体加速比受限于无法并行的串行部分；应将串行范围严格收敛至真实因果依赖与共享可变状态。
- **边际价值定理与有限理性元推理 (Marginal Value Theorem & Metareasoning)** `[Reported]`：理性智能体在信息搜集与中间处理中，当额外步骤的预期边际效用低于时间/注意力/协调开销时，应立即停止（Sufficiency Stop）。

---

## 3. 第一性原理推导与认知状态 (First-Principles Derivation & Epistemic Status)

针对上述问题与信源，推导出以下核心语义与自然推论：

### A. 核心语义

1. **使命级效率 (Mission-Level Efficiency)** `[Inferred]`：
   - 在所有满足权威性（Authority）、证据链（Evidence）、必要门禁（Required Gates）及安全边界的合法路径中，**优先选择具备更短关键路径（Critical Path）、更少无价值等待、更少人机协调开销的执行路径**。
2. **边际价值纪律与充分即止 (Marginal-Value Discipline & Sufficiency Stop)** `[Inferred]`：
   - 任何额外的研究、检查、报告、流程或修饰，只有在预期能**实质改变结果、降低真实风险、满足必要门禁或补足关键证据**时才被允许执行；
   - **完成门禁达成即停止（Completion Gate Satisfied → Stop）**，严禁在缺乏实质增量价值的情况下自发扩展工作。

### B. 自然推论 (Operational Corollaries)

- **推论 1（独立项批量/并行）** `[Inferred]`：无阻塞依赖且工作区/状态隔离的独立工作项，应作为批量（Batching）或并行（Parallelism）的默认候选；
- **推论 2（串行依赖而非串行习惯）** `[Inferred]`：*Serialize dependencies, not habits.* 仅在存在共享可变状态（Shared Mutable State）、有序门禁（Ordered Gates）或真实因果依赖时保持串行；
- **推论 3（兄弟分支共享闭环）** `[Inferred]`：服务于同一后置决策的并行兄弟分支（Parallel Siblings），应共享同一闭环边界与完成门禁；
- **推论 4（单整合汇报）** `[Inferred]`：分流内部仅返回最小结果，由父级汇聚（Join）后向 Browser/User 提交单一整合证据包（One Consolidated Evidence Bundle）；
- **推论 5（人机注意力极度节约）** `[Inferred]`：将人类注意力视为最稀缺资源，内部可自治推进的任务坚持 Run-to-Gate，杜绝无意义的中间局部确认；
- **推论 6（充分即止）** `[Inferred]`：达成契约门禁且无实质边际收益时立即停止，不做 100→110 式的过度交付。

---

## 4. 锁定 Matt 流程权威兼容性证据 (Matt Process Authority Compatibility)

本研究严格以锁定 Matt 流程权威（`mattpocock/skills @ 8b78b531ab965735c5dc74f6f7a219e1e37326df`）为基准，逐项核实兼容性：

| Matt 原生机制 / 权威信源 | Matt 原生语义与哲学 | Mission-Level Efficiency 兼容性分析 | 事实状态 |
|---|---|---|---|
| **`ask-matt` 路由器** (`skills/engineering/ask-matt/SKILL.md`) | 明确规定 `/wayfinder` 仅适用于 huge / foggy / multi-session 任务，强调其“slower and denser”，明令禁止 well-scoped 任务走 Wayfinder。 | **完全一致**。Mission-level efficiency 反对对小任务施加重型流程，主张小任务直接走轻量流。 | `[Verified]` |
| **`/to-tickets` 与依赖模型** (`skills/engineering/to-tickets/SKILL.md`) | 生成自包含 tickets 并通过 issue dependencies 声明阻塞边（blocking edges）；无 blocker 的 ticket 可独立/并发推进。 | **完全一致**。强调“从依赖关系出发”，未阻塞的分支天然可并发。 | `[Verified]` |
| **`/research` 技能** (`skills/engineering/research/SKILL.md`) | 语义为“把 reading legwork 交给 background agent，主线继续工作，并留下 cited durable artifact”。 | **完全一致**。原生支持后台并发阅读与主线推进，且强调持久化研究资产。 | `[Verified]` |
| **`PHASE-BOUNDARIES.md` 决策树** (`skills/engineering/ask-matt/PHASE-BOUNDARIES.md`) | 阶段边界评估顺序为 `Continue → Clear → Handoff → Subagent → Compact`，优先采用最廉价、保护 primary-source continuity 的方案。 | **完全一致**。反对无收益的上下文切换与过重 ceremony，坚持最小充分代价。 | `[Verified]` |
| **调用权限与调用边界** (`.agents/invocation.md`) | 严格区分 `user-invoked` 技能（必须人类显式输入名称触发）与模型自治边界。 | **完全一致**。并行与拓扑自治仅限于内部实现，绝不绕过人类显式授权边界与必要技能门禁。 | `[Verified]` |

**结论**：Mission-level efficiency 与 Marginal-value discipline 是 Matt 原生工程哲学的自然延伸，不仅未弱化 Matt 门禁，反而清除了偏离 Matt 极简主张的形式主义冗余。

---

## 5. 被否定方案与反例分析 (Rejected Alternatives & Negative Patterns)

在推导过程中，以下 5 种设计方向被明确评估并否定：

1. **否定方案 A：建立 Browser 端细粒度调度器（Browser-Side Micro-Scheduler）**
   - *理由*：违背 Default Split 与 IDE 执行拓扑自治权。Browser 介入具体子代理派发与步骤编排会导致跨端中继爆炸、上下文拥挤，并丧失对不同 IDE Harness 原生特性的适应力。
2. **否定方案 B：引入显式并行/效率状态机（Parallelism State Machine）**
   - *理由*：增加死板状态转换规则（如 PENDING_PARALLEL → RUNNING_LANES → JOINING），大幅消耗指令上下文（Context Bloat），并在遇到非典型场景时迅速失效。
3. **否定方案 C：维护静态 IDE Harness 能力矩阵（Harness Capability Matrix / Registry）**
   - *理由*：外部环境与工具演进极快，静态矩阵必然迅速过时且维护成本高昂。改为采用“运行时对承重能力的按需轻量感知”与“依赖优先通用推导”。
4. **否定方案 D：强制所有任务必须并行 / 固定 Subagent 数量**
   - *理由*：机械要求并行会在单线小任务上引入额外的进程创建、工作区隔离与汇聚开销，反而降低整体效率。
5. **否定方案 E：将 Project Memory / Personality 作为效率规范的主要承载层**
   - *理由*：Memory 与模型 Personality 不具备版本可追溯性与规范权威性，无法提供可审计的回归保障。

---

## 6. 配置分层落地矩阵 (Configuration Layering Matrix)

为防止出现平行 SSOT，本研究将相关结论精确晋升（Promote）至最窄正确宿主：

```text
┌────────────────────────────────────────────────────────────────────────┐
│               browser-workflow-spec.md (Normative SSOT)               │
│  - 核心定义：Mission-Level Efficiency 原则                              │
│  - 不变式：Marginal-Value Discipline & Sufficiency Stop                │
│  - 并发与汇聚不变式：Dependency-First, Workspace Isolation, Single Join│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ guides
┌───────────────────────────────────▼────────────────────────────────────┐
│              browser-agent-playbook.md (Operational Manual)            │
│  - Browser 规划操作：轻量依赖与并行机会扫描（Dependency/Leverage Scan） │
│  - 工单派发姿态：指出明显并行候选，不微观编排拓扑                        │
│  - 停止纪律：门禁满足即止，杜绝 100→110 汇报与打磨                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ activates
┌───────────────────────────────────▼────────────────────────────────────┐
│            project-instructions.md (Minimal Runtime Trigger)           │
│  - 极简触发词：在 Mission Contract 与相称性中嵌入关键路径与边际价值思维  │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                      AGENTS.md (Maintainer Layer)                      │
│  - 仓库维护者行为：自治推进至门禁、相称证据输出、杜绝形式化过度工程      │
├────────────────────────────────────────────────────────────────────────┤
│                      CONTEXT.md (Domain Glossary)                      │
│  - 稳定术语沉淀：使命级效率、边际价值纪律、充分即止、关键路径优先        │
├────────────────────────────────────────────────────────────────────────┤
│          docs/evals/behavioral-regression-evals.md (Eval Suite)         │
│  - 长期行为回归套件：R1 独立实验、R2 极小任务、R3 真实依赖、R4 注意力开销 │
├────────────────────────────────────────────────────────────────────────┤
│           docs/research/mission-level-efficiency.md (This File)        │
│  - 非规范性研究底册：背景、信源、事实状态、推导、反例、未决前沿与触发点   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 7. 未决问题与研究前沿 (Unresolved Questions & Research Frontier)

本研究在当前阶段明确保留以下开放问题（Open Questions / Frontier），作为未来继续调研的线索：

1. **子代理创建门槛与延迟权衡 (Subagent Spawning Thresholds)** `[Inferred]`：
   - 在任务颗粒度多小的时候，创建子代理进程、工作区隔离与跨 Agent 汇聚的固定时间/上下文开销，会超过其并发带来的关键路径收益？
2. **人类认知带宽与分支因子平衡 (Cognitive Branching Factor in Fresh Sessions)** `[Reported]`：
   - 当 Browser 在 Work Order 中识别出多个并行候选时，单次向人类呈现的最优分支数量上限是多少？过度分支是否会导致用户在中继与审查时发生上下文认知过载？
3. **被动式回归感知机制 (Passive Anti-Regression Monitoring)** `[Inferred]`：
   - 是否存在一种无需在每次会话提示词中消耗大量 Token 的轻量方式，仅通过会话后日志分析或离线评测自动检测 Agent 是否发生 100→110 或低效串行退化？
4. **多样化 IDE Harness 原生能力对齐 (Cross-Harness Native Alignment)** `[Reported]`：
   - 随着 Claude Code、Cursor、Antigravity、Codex 持续迭代其原生子代理、Background Tasks 与 Worktree 接口，如何在保持 Mission Contract 供应商中立（Provider-Neutral）的前提下，最大化利用各环境的原生并发能力？

---

## 8. 长期生命周期与演进触发点 (Lifecycle, Promotion & Revisit Triggers)

本底册作为可扩展的研究资产长期维护。当出现以下事件时，触发有界重新评估（Bounded Re-evaluation）：

1. **工作流发布变更**：新的 Workflow Release 修改了 Mission Contract、Planning、Review 或 Context 规则；
2. **底座大模型或 Harness 发生质变**：新模型具备更强自主规划能力，或 Harness 原生支持全新的并发编排原语；
3. **Matt 上游正式发布**：Matt 出现 formal non-prerelease Release 并进入 Upgrade Review；
4. **真实项目出现形式主义退化**：在实际工程中再次观察到串行化或过度打磨回归现象；
5. **前沿 Agent 编排研究出现实质突破**：出现更优的延迟感知（Latency-Aware）或元推理（Metareasoning）方法论。

### 重新评估流程

1. 按照 `docs/evals/behavioral-regression-evals.md` 中的 Runtime Eval Protocol 执行真实 Browser 评测；
2. 查阅本文件中的未决前沿与被否定方案，避免重复试错；
3. 遵循 Subtraction Check 进行 `KEEP / MODIFY / DELETE / ADD` 决策；
4. 若新模型已原生具备某项能力，主动精简提示词中的冗余规则；
5. 任何新理念必须经由真实回归证据验证后，方可通过 Durable Insight Promotion 升格为生产规范。
