# AGENTS.md

> 仓库维护者规则层（Repository-Maintainer Layer）
> 读者：IDE Agent 及参与本仓库维护的 Agent
> 核心问题：IDE Agent 应如何维护 `matt-browser-workflow` 仓库本身？

---

## 1. 仓库定位与双重边界 (Repository Purpose & Boundaries)

本仓库用于定义和演进 **Matt / Browser Workflow** 协作体系。本项目属于 **Self-Hosting / Meta-Workflow** 仓库（即使用该工作流维护工作流自身）。

维护本仓库时，必须严格区分：

### A. 自维护边界 (Self-Maintenance Boundary)
* **维护基准 (Maintenance Authority)**：使用最后一个已经接受并冻结的 Git commit / tag（即 last accepted ref，如 `v0.3`）作为维护过程的基准指令。
* **开发对象 (Mutable Product)**：当前分支或工作区中正在编辑的文件是“被开发对象”，其尚未经 Review / 合并的新增规则**不得**反向支配当前维护会话。

### B. 规则层级边界
* 本文件（`AGENTS.md`）仅规范**维护者行为**；
* 本仓库对外提供的规范性需求以 [`PROJECT-SPEC.md`](./PROJECT-SPEC.md) 为权威 SSOT；
* 工作流的完整运作机制以 [`browser-agent-playbook.md`](./browser-agent-playbook.md) 为准。

---

## 2. 默认协作分工 (Default Split)

* **Browser Lead**：负责全局方向、阶段对齐（Destination/Gate）、跨会话上下文治理、外部核实及 Review。
* **IDE Agent**：负责本地文件编辑、环境测试、Git 操作（branch/commit/push/tag）以及向 Browser 提供充分证据（Evidence）。

---

## 3. 核心执行守则 (Maintainer Principles)

1. **结构化中继契约 (Relay Contract)**：
   - 接收来自 Browser Lead 的结构化 Work Order（目标、范围、验收标准、证据要求等）；
   - 反馈时默认假定 Browser 无法直接查看本地工作区，必须提供包含改动文件、测试命令、实际输出、未推送状态等充实证据，**严禁**仅回复“完成”。
2. **语言契约 (Language Contract)**：
   - GitHub Issue、PR 描述、计划、报告、反馈等人类可读材料**默认使用清晰简体中文**；
   - 代码、路径、命令、API、Git identifier、原始日志及专业技术术语保持英文。
3. **600 行上下文软警示 (600-Line Soft Guard)**：
   - 人工编写的代码及面向 Agent 的核心文档若超过约 600 行，作为评估合理拆分的**预警阈值（Warning Threshold）**；
   - 严禁为了凑数字而机械硬拆，若无自然职责边界应保持完整；若超出当前工单范围，只报告不顺手重构。
4. **防止过度设计 (Avoid Overdesign)**：
   - 遵循“先正确再通用、先验证再扩展、先解决当前阻塞”原则；
   - 不增加无真实第二使用者的额外抽象、复杂目录或冗余脚本。

---

## Agent skills

### Issue tracker

GitHub issues. See `docs/agents/issue-tracker.md`.

### Triage labels

Default canonical label mapping. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context. See `docs/agents/domain.md`.
