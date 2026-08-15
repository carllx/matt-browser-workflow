# Matt / Browser Workflow

> 一套面向非专业开发者与全栈工程师的 **Browser Lead ↔ IDE Agent 跨端人机协同工作流**。

---

## 1. 项目简介 (Overview)

`matt-browser-workflow` 旨在解决 AI 辅助编程中的核心割裂问题：
- 网页端大模型（如 ChatGPT / Claude Web）具备强大的全局推理、上下文掌控和架构规划能力（**Browser Lead**）；
- 本地 IDE Agent（如 Antigravity / Cursor / Claude Code / Codex）擅长具体代码编写、测试执行与 Git 操作（**IDE Agent**）；
- **人类用户**作为高信任中继，通过结构化、就绪的工单（Copy-Ready Work Orders）实现两端无缝协同。

### 为什么引入 Matt Skills？
本工作流深度融合了 **Matt Pocock's Engineering Skills**（`mattpocock/skills`）的系统化软件工程哲学（如 `wayfinder` 决策地图、`grilling` 方案拷问、`to-spec` 规范制定、`to-tickets` 工单拆解、`code-review` 双轴评审等），让复杂项目从构想到上线的每一个阶段均有清晰门禁与事实纪律保护，防止越级与过度设计。

---

## 2. 默认协作分工 (Default Split)

* **Browser Lead（网页端统筹）**：
  * 负责全局架构与目标对齐（Destination & Gate）；
  * 负责事实调研（Facts）、路由分析（Skills Routing）与工单派发（Work Order）；
  * 负责跨会话上下文治理与交付结果评审（Review）。
  * 默认权限：**READ / INSPECT / VERIFY**。

* **IDE Agent（本地端执行）**：
  * 负责本地文件编辑、环境构建与自动化测试；
  * 负责 Git 版本控制（分支、提交、推送、标签）与追踪器更新；
  * 负责向 Browser Lead 提供包含充分证据（Evidence）的执行反馈。
  * 默认权限：**EXECUTE / MUTATE**。

---

## 3. 快速上手指南 (Quick Start)

### 步骤一：本地 IDE 前置准备 (IDE Setup)

1. **安装 Matt Skills**：
   在终端运行 Matt 官方技能安装器：
   ```bash
   npx skills@latest add mattpocock/skills
   ```
   * 在交互式安装界面中，选择你正在使用的本地 IDE / Agent（如 Claude Code, Cursor, Antigravity, Codex 等）；
   * 确保勾选并安装了 `setup-matt-pocock-skills`（以及其他常用工程技能）。

2. **初始化目标仓库配置（每个仓库仅需执行一次）**：
   打开你的目标代码仓库，在 **IDE Agent 的对话框** 中发送以下指令（注意：这是 Agent 对话指令，而非终端 Shell 命令）：
   ```text
   /setup-matt-pocock-skills
   ```
   * 追踪器（Issue Tracker）推荐选择：`GitHub`（或其他实际使用的系统）；
   * 领域文档（Domain Layout）推荐选择：`single-context`；
   * 若安装了 `triage` 技能，确认采用默认 canonical labels 并在 GitHub 中存在对应标签；
   * 该 Skill 会在目标仓库下自动生成 `docs/agents/*` 并在 `AGENTS.md` 中注入规则块。

---

### 步骤二：配置 ChatGPT Project (Browser Lead Setup)

打开 ChatGPT，点击创建或配置一个专用 **Project**：

1. **配置 Project Instructions（核心启动入口）**：
   复制本仓库 [`chatgpt-project/project-instructions.md`](./chatgpt-project/project-instructions.md) 的**全部文本内容**，粘贴到 ChatGPT Project 的 **Instructions** 输入框中并保存。

2. **上传 Project Sources（核心知识库）**：
   将以下 **2 个交付文件** 上传至该 ChatGPT Project 的 **Files / Sources** 中：
   * [`chatgpt-project/browser-agent-playbook.md`](./chatgpt-project/browser-agent-playbook.md)（执行手册）
   * [`chatgpt-project/browser-workflow-spec.md`](./chatgpt-project/browser-workflow-spec.md)（规范性需求 SSOT）

> [!IMPORTANT]
> **哪些文件不需要上传？**
> * 根目录的 `README.md`、`AGENTS.md` 以及 `docs/agents/*` 属于仓库自维护或 IDE 端本地配置，**严禁上传**到 ChatGPT Project Sources，以保持网页端上下文精简。

---

### 步骤三：开启第一次协作对话 (First Session)

在配置好的 ChatGPT Project 中开启新对话，只需发送你的仓库地址与当前目标：

```text
你好，请接手这个项目：
- PROJECT_REPO: https://github.com/<owner>/<repo>
- 目标：<你现在想完成什么>
```

Browser Lead 将会自动通过 Bounded Project Sync 解析默认分支与 Tracker 现场，并向你输出极简的启动定位反馈：
> **现在在哪里 → 本次判断依据的现场/ref → 当前真正的阻塞 → 推荐下一步 → 当前还不应该做什么。**

---

## 4. 基本工作循环 (Relay Contract Loop)

整个开发过程遵循严密、闭环的中继契约（Relay Contract）：

```text
  [Browser Lead]
        │
   (下发结构化 Copy-Ready Work Order)
        ▼
   [人类用户] ──(一键复制粘贴)──► [本地 IDE Agent]
                                        │
                                  (执行编辑、测试与 Git 操作)
                                        ▼
   [人类用户] ◄──(返回充足 Evidence)─── [IDE Agent]
        │
   (粘贴反馈报告)
        ▼
  [Browser Lead] ──(独立核实验证 / Gate 判定)──► [下一阶段]
```

1. **Browser 派发工单**：Browser Lead 会生成一个结构清晰、易于一键复制的 Markdown 代码块，包含唯一目标（Goal）、范围（Scope）、验收标准（Acceptance Criteria）和所需证据（Evidence Required）。
2. **用户中继传递**：你只需将该代码块一键复制发送给本地 IDE Agent。
3. **IDE 本地执行与反馈**：IDE Agent 执行操作后，必须返回包含具体改动文件、命令输出、commit SHA 及未推送状态的完整报告，**严禁仅回复“已完成”**。
4. **Browser 独立评审**：Browser Lead 核验证据与线上事实后，批准通过并进入下一个工作流节点。

---

## 5. 跨会话治理与退化预警 (Context Stewardship)

* **双会话独立（Dual-Session）**：Browser 端与 IDE 端是各自独立的上下文空间。一端开启新会话（Fresh Session）不影响另一端继续工作。
* **阶段边界切换（Phase Boundary）**：严禁在阶段中途（Mid-Phase）随意打断会话。只在任务完成、Issue 关闭或明确的阶段节点进行 Context Compact / Clear / Fresh Session。
* **退化信号识别**：当 Agent 出现反复询问已知问题、推翻已定决策、回复泛化等情况时，应在最近的阶段节点交接并开启新会话。
* **600 行软警示**：单文件超过 600 行时仅作为合理拆分的评估预警线，绝不进行为了指标而割裂代码的机械硬拆。

---

## 6. 版本升级指引 (Upgrading)

当 `matt-browser-workflow` 发布新版本（如 `v0.5` 等）时：

1. 从本仓库拉取最新文件；
2. 将最新的 [`chatgpt-project/project-instructions.md`](./chatgpt-project/project-instructions.md) 重新复制并覆盖 ChatGPT Project Instructions；
3. 将最新的 `browser-agent-playbook.md` 与 `browser-workflow-spec.md` 重新上传至 ChatGPT Project Sources；
4. 若 `MAT_REF` 发生重大版本迭代，按需在 IDE 中重新校验目标仓库的 `/setup-matt-pocock-skills`。
