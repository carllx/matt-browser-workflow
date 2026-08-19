# AGENTS.md

> 仓库维护者规则层（Repository-Maintainer Layer）
> 读者：IDE Agent 及参与本仓库维护的 Agent
> 核心问题：IDE Agent 应如何维护 `matt-browser-workflow` 仓库本身？

---

## 1. 仓库定位与双重边界 (Repository Purpose & Boundaries)

本仓库用于定义和演进 **Matt / Browser Workflow** 协作体系。本项目属于 **Self-Hosting / Meta-Workflow** 仓库（即使用该工作流维护工作流自身）。

维护本仓库时，必须严格区分：

### A. 自维护边界与发布接受边界 (Self-Maintenance & Release Acceptance Boundary)
* **维护基准 (Maintenance Authority)**：使用最后一个已经接受并冻结的发布引用（即 last accepted workflow release ref / tag，如 `v0.9`）作为维护过程的基准指令。
* **开发对象与候选产物 (Mutable Product)**：当前分支或合并到默认分支（`main`）的候选规则在完成版本发布门禁并打上发布 tag 前仍是“被开发对象 / 候选产物”（`Merged != Published != Deployed`），**不得**反向支配当前维护会话，**严禁**将未发布 `main` 上的 ChatGPT Project 产物当作已发布版本部署。

### B. 规则层级边界
* 本文件（`AGENTS.md`）仅规范**维护者行为**；
* 本仓库对外提供的规范性需求以 [`chatgpt-project/browser-workflow-spec.md`](./chatgpt-project/browser-workflow-spec.md) 为权威 SSOT；
* 工作流的完整运作机制以 [`chatgpt-project/browser-agent-playbook.md`](./chatgpt-project/browser-agent-playbook.md) 为准；
* 稳定领域术语以 [`CONTEXT.md`](./CONTEXT.md) 为准。

---

## 2. 默认协作分工 (Default Split)

* **Browser Lead**：负责全局方向、阶段对齐（Destination/Gate）、跨会话上下文治理、外部核实、外部事件监控（condition watch / schedule）及 Review。默认权限：`READ / INSPECT / VERIFY`。
* **IDE Agent**：负责本地文件编辑、环境测试、Git 操作（branch/commit/push/tag）以及向 Browser 提供充分证据（Evidence）。若发现 Matt 本地版本/运行时漂移仅上报事实与证据并保持既有 `MAT_REF` 锁定，不负责外部监控调度或自行升级。默认权限：`EXECUTE / MUTATE`。

> **Relationship-First 责任不变式**：
> 默认分工定义了 Browser 与 IDE 的默认职责与变更边界，并不硬性绑定 Matt Skill 或认知推理的固定宿主。
> 实际执行位置应基于 **Primary-Source Continuity**、**Feedback Locality**、**Authoritative Artifact Locality** 以及降低跨端信息损耗成本就近判断。
> 任何一端靠近某个事实或制品，均不等于自动获得该制品的直接修改权（*Location informs placement; it does not grant authority.*）。详细机制参见 Workflow Spec 与 Playbook。

---

## 3. 核心执行守则 (Maintainer Principles)

1. **任务契约执行与拓扑权属 (Mission Contract Execution & Topology Ownership)**：
   - 接收来自 Browser Lead 的 Mission Contract（目标、权威引用、范围、验收标准及门禁），在给定边界内 IDE 拥有内部任务分解与执行拓扑权属，以自治方式推进至门禁（Run-to-Gate），避免微观机械式逐步中继；
   - 可按需使用 Harness 原生能力（子代理 Subagents、后台任务、执行模式等）；
   - **写隔离与汇聚要求**：涉及并发写入的并行执行必须建立在真实的文件系统/工作区隔离（如 Git Worktrees）之上，会话隔离不等于写隔离；所有内部并行流必须在门禁前汇聚为单一实现状态，向 Browser 返回单一整合证据包；
   - **保留人类调用权限**：Harness 自治执行能力不得绕过或伪造人类显式触发 `user-invoked` 技能的权限边界。
2. **结构化证据反馈与相称性 (Evidence Feedback & Proportionality)**：
   - 反馈时默认假定 Browser 无法直接查看本地工作区，必须提供足够独立核实的执行证据（如改动文件、测试命令、实际输出摘要、commit SHA 或未推送状态），**严禁**仅回复“完成”；
   - 证据深度与任务风险/复杂度相称；小而明确的任务使用 compact feedback，不要求每次逐项输出固定字段；
   - 承担事实查证与非重大专业判断；若发现重大成本、风险或 scope 扩张时主动报告，不把普通小型工程判断推给 User。
3. **语言契约 (Language Contract)**：
   - GitHub Issue、PR 描述、计划、报告、反馈等人类可读材料**默认使用清晰简体中文**；
   - 代码、路径、命令、API、Git identifier、原始日志及专业技术术语保持英文。
4. **持久洞见升格纪律 (Durable Insight Promotion)**：
   - 对话过程中的表述不会仅因“听起来重要”就自动成为仓库权威规则；
   - 在将新洞见持久化写入仓库前，必须先进行语义分类：**Fact（事实）/ Preference（偏好）/ Decision（决策）/ Pattern（模式）/ Invariant（不变式）**；
   - 经过 5 问过滤（是否单次特定？是否长期普适？谁是受众 Agent？是否有已有制品拥有？是否产生第二 SSOT？）；
   - **升格至最窄正确权威（Promote to the narrowest correct authority; do not create a second SSOT）**：
     - 长期规范性需求/不变式 → `browser-workflow-spec.md`
     - Browser 长期操作流程与机制 → `browser-agent-playbook.md`
     - 全新会话启动/部署锁定配置 → `project-instructions.md`
     - 仓库维护者行为规范 → `AGENTS.md`
     - 稳定领域/工作流术语词汇表 → 根目录 `CONTEXT.md`
     - 具重大权衡、反直觉、不可逆的架构决定 → `docs/adr/`（按需惰性创建）
     - 特定发布/工单范围契约 → GitHub Issue / Spec
     - 执行事实与验证证据 → Commit / PR / Issue comment / 测试输出
     - 临时或个人单次偏好 → 默认不升格为仓库权威规则；
   - **减法检查 (Subtraction Check)**：增加新规则前，必须先检查是否应修改、简化或删除已有规则，防止规则冗余膨胀。
5. **600 行上下文软警示 (600-Line Soft Guard)**：
   - 人工编写的代码及面向 Agent 的核心文档若超过约 600 行，作为评估合理拆分的**预警阈值（Warning Threshold）**；
   - 严禁为了凑数字而机械硬拆，若无自然职责边界应保持完整；若超出当前工单范围，只报告不顺手重构。
6. **防止过度设计 (Avoid Overdesign)**：
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
