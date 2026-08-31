# Matt / Browser Workflow

> 一套面向非专业开发者与全栈工程师的 **Browser Lead ↔ IDE Agent 跨端人机协同工作流**。

---

## 1. 项目简介 (Overview)

Matt 原生工程 Skills 的典型关系模型是 `Human ↔ Agent in working directory ↔ Repo / Runtime / Tracker`。本项目面对的实际拓扑是 `User ↔ Browser Agent ↔ IDE Agent ↔ Repo / Tracker`：Browser 与 IDE 拥有不同的 context、工具能力、事实位置和 feedback loop。

本项目存在的核心价值不是再造一套 Matt workflow，而是：

> 在 User / Browser / IDE 分离的协作关系中，保护 Matt 的 **decision ownership**、**primary-source continuity**、**feedback locality** 与 **durable shared state / canonical artifacts**。

### 三端角色
- **Browser Lead**（ChatGPT / Claude Web 等）：Workflow Steward、远程事实与 tracker 协调、全局目标与阶段对齐、Review Gate。
- **IDE Agent**（Antigravity / Cursor / Claude Code / Codex 等）：本地文件、运行时、Git 、本地测试的默认执行端。
- **User**：**decision / trust participant**—主导产品与架构取舍、explicit authorization、user-invoked Skill 指令、关键 HITL exchange。在跨端默认协作循环中同时承担 relay 角色，但不是首要的机器间传输层。

### 为什么引入 Matt Skills？
本工作流融合了 **Matt Pocock's Engineering Skills**（`mattpocock/skills`）的工程 discipline：这些 Skill 是小型、可组合的工具，各自拥有明确的 Gate 和边界。Browser 根据当前真正的 blocker 选择合适的 Skill，而非驱动所有项目顺序走完固定的全量流程。Well-scoped work 不应被迫走完整条大型流程。

### 依赖锁定与演进治理 (Dependency Integrity & Upstream Governance)
- **发布级依赖锁定与来源完整性 (Release Lock & Provenance)**：每个工作流版本通过不可变的 `MAT_REPO @ MAT_REF` 锁定 Matt 流程技能权威。历史已发布版本不可追溯修改，当前 `MAT_REF` 作为继承自 v0.9 的 legacy carry-forward lock 继续沿用，未来更新必须严格等于上游正式 non-prerelease release tag 解析的不可变 commit；源码检索受 Ref 严格约束，保证确定性与可复现性；
- **感知演进与分级通知**：`Update notification != Upgrade decision.` 启动时可轻量感知上游演进，但绝不自动升级；非实质漂移不打扰，实质更新候选出具升级简报（Upgrade Brief），运行时完整性问题（如 ref 不存在或内容不一致）作为阻塞呈现并 Fail-Closed；
- **Relationship-First 演进审查**：升级评估不依赖静态矩阵，而是通过 10 维关系透镜审视对 User / Browser / IDE 三端拓扑及横切性语义的影响，并遵循适配精简（Adaptation Subtraction）原则。

---

## 2. 默认协作分工 (Default Split)

* **Browser Lead（网页端统筹）**：
  * 负责全局架构与目标对齐（Destination & Gate）；
  * 负责事实调研（Facts）、路由分析（Skills Routing）与工单派发（Work Order）；
  * 负责跨会话上下文治理与交付结果评审（Review）。
  * 默认权限：**READ / INSPECT / VERIFY**（含窄范围 tracker-native 与 domain-modeling 功能下的带授权写入）。

* **IDE Agent（本地端执行）**：
  * 负责本地文件编辑、环境构建与自动化测试；
  * 负责 Git 版本控制（分支、提交、推送、标签）与追踪器更新；
  * 负责向 Browser Lead 提供包含充分证据（Evidence）的执行反馈。
  * 默认权限：**EXECUTE / MUTATE**。

> **默认分工说明 Browser / IDE 的层次和责任，不规定 Skill 执行的实际位置**。Skill 的实际执行位置应根据 primary-source continuity、feedback locality、authoritative artifact 位置以及跨端信息损耗成本就近判断，不建立固定 Skill → Host 映射表。

---

## 3. 快速上手指南 (Quick Start)

### 步骤一：本地 IDE 前置准备 (IDE Setup)

1. **安装 Matt Skills**：
   在终端运行 Matt 官方技能安装器：
   ```bash
   npx skills@latest add mattpocock/skills
   ```
   * 在交互式安装界面中，选择你正在使用的本地 IDE / Agent（如 Claude Code, Cursor, Antigravity, Codex 等）；
   * 确保勾选并安装了 `setup-matt-pocock-skills`（以及其他常用工程技能）；
   * > **注意**：本地安装（即使来自当前上游）不证明本地版本完全等同于工作流锁定的 `MAT_REF`；在关键技能执行前若对齐状态未知，Browser 可向 IDE 发起窄范围 Fact Probe。

2. **初始化目标仓库配置（每个仓库仅需执行一次）**：
   打开你的目标代码仓库，在 **IDE Agent 的对话框** 中发送以下指令（注意：这是 Agent 对话指令，而非终端 Shell 命令）：
   ```text
   /setup-matt-pocock-skills
   ```
   * 追踪器（Issue Tracker）推荐选择：`GitHub`（或其他实际使用的系统）；
   * 领域文档（Domain Layout）推荐选择：`single-context`；
   * 若安装了 `triage` 技能，确认采用默认 canonical labels 并在 GitHub 中存在对应标签；
   * 该 Skill 会在目标仓库下自动生成 `docs/agents/*` 并在 `AGENTS.md` 中注入规则块；
   * 若目标项目拥有特定的外部知识库、领域模型或工具能力（如 NotebookLM、OpenBB 等），可按需在目标仓库中创建 `docs/agents/capabilities.md` 进行轻量声明（属于 Project Authority，供 Browser 发现并按需路由）。

---

### 步骤二：配置 ChatGPT Project (Browser Lead Setup)

打开 ChatGPT，点击创建或配置一个专用 **Project**：

1. **配置 Project Instructions（核心启动入口、发布身份、依赖锁定与仓库绑定）**：
   - 从本工作流**对应不可变发布版本（如 `v0.11` Release Tag）**中获取 [`chatgpt-project/project-instructions.md`](./chatgpt-project/project-instructions.md) 的全部文本内容，粘贴到 ChatGPT Project 的 **Instructions** 输入框中；
   - 将文本顶部 `## Project Binding` 中的 `PROJECT_REPO: <SET_PER_CHATGPT_PROJECT>` 替换为该 Project 对应的**目标仓库 URL**（例如 `https://github.com/<owner>/<repo>`）并保存。

2. **上传 Project Sources（核心知识库）**：
   从对应**不可变发布版本**下载以下 **2 个交付文件**，上传至该 ChatGPT Project 的 **Files / Sources** 中：
   * [`chatgpt-project/browser-agent-playbook.md`](./chatgpt-project/browser-agent-playbook.md)（执行手册）
   * [`chatgpt-project/browser-workflow-spec.md`](./chatgpt-project/browser-workflow-spec.md)（规范性需求 SSOT）

> [!IMPORTANT]
> **部署来源不可变与 Fail-Closed 原则**：
> 部署或升级 ChatGPT Project 时，**必须**使用特定不可变发布 Tag（如 `v0.11`）下的文件，**严禁**直接从未发布的 `main` 默认分支下载部署。未发布的 `main` 分支属于开发中候选产物（Mutable Product），`Merged != Published != Deployed`。若在 Project 中误填了尚未发布或不存在的 `WORKFLOW_REF`，工作流在启动与接手时将作为 **Workflow Runtime Integrity Problem** 立即 Fail-Closed 阻断并提示重新部署。

> [!NOTE]
> **关于无需上传文件的说明**
> 根目录的 `README.md`、`AGENTS.md` 以及 `docs/agents/*` 属于仓库自维护或 IDE 端本地配置，正常安装时**无需上传**到 ChatGPT Project Sources。

---

### 步骤三：开启第一次协作对话 (First Session)

在配置好的 ChatGPT Project 中开启新对话，只需说明你的当前开发目标（仓库地址已在 Project Binding 中自动加载）：

```text
你好，请接手当前项目：
- 目标：<你现在想完成什么>
```

> **自动化事实解析**：遵循“不要求非专业用户填写 Browser 可以自行查证的工程事实”原则：`WORKFLOW_REF` 从 Instructions 的 Workflow Release Identity 读取；`MAT_REPO` / `MAT_REF` / `MAT_ROUTER_PATH` 从 Release Dependency Lock 读取；Browser Lead 会基于绑定的 `PROJECT_REPO` 自动核实并解析 `PROJECT_DEFAULT_BRANCH`、`PROJECT_ACTIVE_REF` 与 `PROJECT_TRACKER`（现场事实）；`MAT_UPSTREAM_HEAD` 为现场观察信号；若需获取本地环境的 `LOCAL_MAT_STATE`，Browser 会向 IDE 发出窄范围 Fact Probe，而不会要求你自己回答工程事实。

随后，Browser Lead 将会自动完成小范围现场同步（Bounded Project Sync），并向你输出极简的启动定位反馈：
> **现在在哪里 → 本次判断依据的现场/ref → 当前真正的阻塞 → 推荐下一步 → 当前还不应该做什么。**

---

## 4. 默认开发协作循环 (Default Relay & Autonomous Execution Loop)

v0.11 默认开发协作循环采用**任务契约与自治推进至门禁（Mission Contract & Run-to-Gate）**模型：

```text
  [Browser Lead]
        │
   (下发 Mission Contract / 目标、范围、依赖与门禁)
        ▼
   [人类用户] ──(一键语义中继 / 授权或触发)──► [本地 IDE Agent]
                                                  │
                                            (拥有执行拓扑自治权：
                                             内部任务分解、子代理/
                                             工作区隔离、自治推进至门禁)
                                                  │
                                            (Git commit / push / 测试)
                                                  ▼
   [人类用户] ◄──(返回整合证据包 / Pushed SHA)─── [IDE Agent]
        │
   (中继完成信号)
        ▼
  [Browser Lead] ──(基于推送固定 SHA 独立 Review / Gate)──► [下一阶段]
```

1. **Browser 派发任务契约 (Mission Contract)**：Browser Lead 统筹把握方向、依赖、范围与门禁标准，生成结构清晰的 Mission Contract（或基于 Issue 指针传递 execution delta），不微观调度 IDE 的内部执行拓扑。
2. **用户语义中继 (Semantic Relay)**：用户仅需将任务指令一键传递给 IDE，保留决策、授权与 slash 技能调用的控制边界；无需充当机械数据搬运工。
3. **IDE 自治执行与汇聚 (Autonomous Execution & Join Gate)**：IDE Agent 在任务边界内拥有内部任务分解与拓扑权属（按需使用子代理、后台任务或工作区隔离），自治推进至门禁，并在完成时将所有分支汇聚为单一规范状态，提交并推送到远程仓库。
4. **固定引用审查 (Fixed-Ref Browser Review Gate)**：IDE 返回包含测试结果摘要与已推送固定引用（fixed pushed commit SHA 或 PR head SHA）的单一整合证据包；Browser Lead 直接远程比对代码事实进行独立审查。

---

## 5. 跨会话治理与退化预警 (Context Stewardship)

* **双会话独立（Dual-Session）**：Browser 端与 IDE 端是各自独立的上下文空间。一端开启新会话（Fresh Session）不影响另一端继续工作。
* **阶段边界切换（Phase Boundary）**：严禁在阶段中途（Mid-Phase）随意打断会话。只在任务完成、Issue 关闭或明确的阶段节点进行上下文治理。治理策略按有序逻辑评估：Continue → Clear → Handoff（需要 portability 时）→ Subagent → Compact，Compact 不是首选。
* **退化信号识别**：当 Agent 出现反复询问已知问题、推翻已定决策、回复泛化等情况时，应在最近的阶段节点执行治理并按需开启新会话。
* **Session Checkpoint**：Browser 的跨会话状态恢复材料称为 Session Checkpoint / Snapshot，与 Matt `/handoff` Skill 的窄 portability 语义不同（Matt `/handoff` 用于需要跨工具或向他人交接时）。
* **600 行软警示**：单文件超过 600 行时仅作为合理拆分的评估预警线，绝不进行为了指标而割裂代码的机械硬拆。

---

## 6. 版本升级与部署核实 (Upgrading & Deployment)

工作流遵循发布完整性原则：**`Issue done != Release done`** 且 **`Merged != Published != Deployed`**。

> [!NOTE]
> **版本说明 (Superseded v0.10)**：旧 `v0.10` tag 包含部署前已修复的正确性缺陷，已被 `v0.10.1` 完整取代（superseded），旧 `v0.10` 不应部署。

当 `matt-browser-workflow` 发布正式新版本（如 `v0.11`）时，遵循以下步骤更新你的 ChatGPT Project：

1. **获取正式发布文件 (Exact Release Ref)**：
   - 访问 GitHub 对应**不可变发布 Tag**（例如 `https://github.com/carllx/matt-browser-workflow/tree/v0.11`），**绝不要**使用 `main` 分支的浮动文件；
2. **记录现有仓库绑定**：在更新前，先记下当前 ChatGPT Project Instructions 顶部绑定的 `PROJECT_REPO` URL；
3. **更新 Project Instructions**：将发布 Tag 下的 [`chatgpt-project/project-instructions.md`](./chatgpt-project/project-instructions.md) 文本复制并粘贴到 Instructions 中；
4. **恢复 Project Binding**：将第 2 步记录的 `PROJECT_REPO` URL 填回新版 Instructions 顶部的 `## Project Binding` 中，确认不再是占位符；
5. **更新 Project Sources**：将发布 Tag 下的 `browser-agent-playbook.md` 与 `browser-workflow-spec.md` 重新上传至 ChatGPT Project 的 Sources（替换旧文件）；
6. **部署后完整性核实 (Post-Deployment Verification)**：
   - 在 ChatGPT Project 开启新对话，确认 Browser Lead 成功识别新的 `WORKFLOW_REF`（如 `v0.11`）及绑定的 `PROJECT_REPO`；
   - 确认加载的 Instructions 与 Sources 内容与发布版本完全一致。若 ref 不可解析或发现版本漂移，Browser 会立即 Fail-Closed 阻断并提示重新从发布 Tag 覆盖上传；
7. **按需检查本地 Skills 与仓库配置**：
   - **Skill 版本更新**：若新工作流发布版本更新了 `MAT_REF` 锁定，使用官方 `npx skills update` 进行 IDE 本地更新；
   - **仓库级配置**：`/setup-matt-pocock-skills` 仅在目标仓库配置缺失或新版本对前置产生不兼容变更时才需重新执行。

> **核心原则**：工作流通用指令可随版本升级，但目标项目的仓库绑定（`PROJECT_REPO`）必须始终保留；且部署来源必须来自不可变的发布 Tag。项目专属的能力声明（`docs/agents/capabilities.md`）保存在目标仓库自身（Project Authority），工作流升级无需重新录入。
