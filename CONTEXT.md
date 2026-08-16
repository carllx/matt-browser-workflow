# Domain Vocabulary & Workflow Glossary

> 核心定位：`matt-browser-workflow` 体系的稳定领域语言与标准术语词汇表（Canonical Glossary）。  
> 规范性需求与操作流程分别参见 [`browser-workflow-spec.md`](./chatgpt-project/browser-workflow-spec.md) 与 [`browser-agent-playbook.md`](./chatgpt-project/browser-agent-playbook.md)。

---

## 核心术语 (Glossary)

### 1. Relationship-First（关系优先原则）
在决定流程（Flow）或技能（Skill）由哪一端承载之前，优先从真实的人机拓扑关系出发进行理性推导——综合评估 **User / Browser / IDE** 三端的认知分工、现场事实位置、决策归属、关键制品（Artifacts）、一手推理源（Primary Source）以及反馈循环（Feedback Loop），而非套用机械固定的“角色-宿主”映射表。详见 `browser-workflow-spec.md` → Relationship-First 协作关系感知。

### 2. Workflow Steward（工作流管家）
Browser Lead 在人机协作中承担的核心统筹角色。负责全局目标对齐（Destination）、证据门禁（Evidence Gate）、技能路由（Routing）、跨会话上下文治理与多端协作，而非所有 Matt 认知逻辑的排他性强制宿主。详见 `browser-agent-playbook.md` → 角色定位。

### 3. Default Split（默认协作分工）
Browser 与 IDE 之间的默认职责与变更边界划分（Browser 默认 `READ / INSPECT / VERIFY`，IDE 默认 `EXECUTE / MUTATE`）。默认分工明确了双方的层次与权限，但不直接锁定 Skill 的实际执行位置。详见 `browser-workflow-spec.md` → 用户操作与交互原则、`browser-agent-playbook.md` → 角色定位 → 默认分工 与 `AGENTS.md` → 默认协作分工。

### 4. Skill Routing（技能路由）
分析理解当前阻塞并挑选/推荐最合适 Matt Skill 或流程的过程。与技能的实际执行调用在语义上是两个独立的事件。

### 5. Skill Invocation（技能调用）
在具体的运行环境中实际触发/执行某个 Skill 的过程。向用户推荐 Skill（Routing）与在本地环境执行 Skill（Invocation）具有不同的语义生命周期。

### 6. User-Invoked Skill（用户调用技能）
依据 Matt 原生技能语义，其执行必须由人类用户显式发出指令（如 Slash Command）进行授权与触发的 Skill。

### 7. Semantic Human Relay（语义级人工中继）
承载真实决策意图、高信任授权、User-Invoked 技能触发或关键人机交互（HITL exchange）的人工参与环节。这是工作流中必须予以尊重和保留的核心控制边界。详见 `browser-workflow-spec.md` → 用户操作与交互原则。

### 8. Mechanical Human Relay（机械式人工搬运）
仅负责在不同 Agent 或环境之间搬运 Commit SHA、日志片段、Issue 描述、追踪器状态或可直接读取的规范制品的人工操作。工作流的核心目标之一是最大程度减少此类低价值中继负担（*Preserve semantic human relay; minimize mechanical human relay.*）。详见 `browser-workflow-spec.md` → 用户操作与交互原则。

### 9. Primary-Source Continuity（一手推理源连续性）
在跨阶段或跨会话推进任务时，优先保留承载着最深层次必要推理链条的上下文，而非在每个阶段或对象边界机械执行清空或交接。详见 `browser-workflow-spec.md` → 上下文治理要求 与 `browser-workflow-spec.md` → Relationship-First 协作关系感知。

### 10. Feedback Locality（反馈就近原则）
事实获取与动作执行应尽量靠近产生对应反馈的系统：远程与追踪器事实靠近 Browser，工作区、本地运行时与自动化测试反馈靠近 IDE，业务决策靠近 User。详见 `browser-workflow-spec.md` → 用户操作与交互原则。

### 11. Canonical Artifact（标准共享制品）
具有权威性、可持久化且跨会话/跨 Agent 共享的标准制品，如 GitHub Issue、规范文档（Spec）、`CONTEXT.md`、ADR、Git 分支、代码 Diff 以及自动化测试证据等。它们充当多端协作的共享状态基准。

### 12. Mutation Authority vs Locality（修改权限与位置就近原则）
制品或事实所处的位置可用于推导最优的读取、推理与技能放置就近性，但位置本身并不自动授予直接修改该制品的权限（*Location informs placement; it does not grant authority.*）。详见 `browser-agent-playbook.md` → 角色定位 与 `browser-workflow-spec.md` → Relationship-First 协作关系感知。

### 13. Release Dependency Lock（发布级依赖锁定）
工作流发布版本在元数据层面对 Matt 流程技能权威的不可变坐标锁定（由 `MAT_REPO`、`MAT_REF`、`MAT_ROUTER_PATH` 组成）。字面值仅由 `project-instructions.md` 单一事实源维护。

### 14. MAT_REF
由工作流特定发布版锁定的不可变 Matt 源码 Commit Ref，作为该版本下的 Matt 流程技能权威（Matt Process Authority），定义该发布版的 Matt 原生行为规范。目标项目的明确适配仅能覆盖具体声明点，绝不得静默替换整个工作流发布的 `MAT_REF`。详见 `browser-workflow-spec.md` → 项目绑定与权威层级 → MAT_REF 权威边界。

### 15. MAT_UPSTREAM_HEAD
上游默认分支的动态 HEAD 提交。仅作为启动时的外部观察感知信号，不构成运行时或流程权威。

### 16. LOCAL_MAT_STATE
IDE 本地环境中实际安装并执行的 Matt Skills 状态（包含安装方式、版本与关键技能可用性）。

### 17. Candidate Freeze（候选版本冻结）
在对上游演进进行深度语义兼容性审查前，必须先将浮动的上游引用冻结为不可变的候选 Commit SHA（`CANDIDATE_MAT_REF`），停止跟随移动的分支。详见 `browser-workflow-spec.md` → 上游演进治理规范 → 候选版本冻结。

### 18. Skill Relationship Compatibility Review（技能关系兼容性审查）
针对候选 Matt Ref 对受影响技能进行的多维关系分析（涵盖三端拓扑关系、调用机制、决策归属、上下文流转、反馈循环、共享制品、中继负担、依赖链条与项目适配等维度），而非静态表格对比。详见 `browser-workflow-spec.md` → 上游演进治理规范 → 技能清单差异与 10 维动态评审透镜。

### 19. Cross-Cutting Semantic Impact（横切性语义影响）
上游改动可能波及未直接发生文件修改的 Skill 的系统性语义变化（例如调用机制、阶段边界行为或协作假设的变更）。详见 `browser-workflow-spec.md` → 上游演进治理规范 → 横切性语义影响。

### 20. Adaptation Subtraction（适配精简原则）
在 Matt 上游演进过程中，对 `matt-browser-workflow` 自身的适配层进行审视，当上游已原生支持某行为时，主动精简或删除本工作流中的对应本地适配规则，以保护 Matt 原生语义、使工作流聚焦于三端拓扑适配并避免累积影子规范。详见 `browser-workflow-spec.md` → 上游演进治理规范 → 适配精简与减法原则。

### 21. Update Notification vs Upgrade Decision（感知通知与升级决策分离）
感知并通报上游演进事实与请求用户作出升级决定是两个不同的阶段（*Update notification != Upgrade decision.*）。非实质漂移不打扰，实质更新需先提供充分证据支持的简报与建议。详见 `browser-workflow-spec.md` → 上游演进治理规范 → 用户分级通知与升级决策协议。

### 22. Durable Insight Promotion（持久洞见升格纪律）
维护者在人机协作中沉淀知识的纪律：对话中的洞见必须经过语义分类（Fact/Preference/Decision/Pattern/Invariant）与 5 问过滤，遵循“升格至最窄正确权威、不创建第二 SSOT”并经过减法检查后，方可写入仓库。详见 `AGENTS.md` → 核心执行守则 → 持久洞见升格纪律。
