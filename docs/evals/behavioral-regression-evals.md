# Behavioral Regression Evals: Mission-Level Efficiency

> **定位**：长期行为回归套件与评测基准（Durable Behavioral Regression Artifact）  
> **关联议题**：Part of #32, Implementation of #33  
> **核心目的**：建立跨模型版本、跨工作流迭代的执行姿态（Execution Posture）防退化守护基准，验证 Agent 是否在满足正确性、权威性与门禁的前提下表现出使命级效率。

---

## 1. 为什么本评测资产值得长期存在 (Rationale for Long-Term Existence)

模型天然存在“为了显得周全而过度执行（100→110 polishing）”以及“遇到多步骤任务默认串行处理”的统计归纳偏好。即使在提示词中写入原则，若缺乏明确的场景基准，随着底座模型微调、提示词微调或跨端中继重构，形式主义与低效串行极易反复回潮。

本回归套件提供 4 个标准场景（R1–R4），重点评估**规划结果与执行姿态**，不硬编码固定的实现细节或子代理数量，作为工作流发布与模型升级时的必要门禁验证。

---

## 2. 核心场景评测矩阵 (Evaluation Scenarios R1–R4)

### 场景 R1 — 多个独立实验并发与单整合汇聚 (Three Independent Experiments)

- **输入特征**：
  - 任务包含 A、B、C 三个在逻辑上相互独立、各自读取独立资源且无共享可变写入冲突的子任务，共同服务于下游的一个决策点（如对比三个库的 API、调查三个独立的现场事实、测试三个独立的配置方案）。
- **通过行为 (PASS Criteria)**：
  1. 识别各子任务之间不存在阻塞依赖（No blocking edges）；
  2. 显式标记为批量（Batching）或并行候选（Parallel Candidate）；
  3. 兄弟分支共享同一闭环边界（Shared closure boundary）；
  4. 内部各分流仅返回最小必要结果，在父级完成汇聚（Join）；
  5. 最终向 Browser/User 提交**单一整合证据包**（One Consolidated Evidence Bundle）。
- **失败行为 (FAIL Anti-Patterns)**：
  - 人为串行化：`A 执行 → A 独立总结汇报 → 请求中间确认 → B 执行 → B 独立总结汇报 → 请求中间确认 → C 执行`；
  - 碎片化打断：每个子任务独立向外部输出长篇大论，频繁打断用户注意力。

---

### 场景 R2 — 小而明确任务充分即止 (Small & Well-Scoped Task / Sufficiency Stop)

- **输入特征**：
  - 任务范围清晰、修改局部、验收标准与完成门禁明确（例如修复单行拼写错误、增补一个既定术语、执行一个现成单元测试）。
- **通过行为 (PASS Criteria)**：
  1. 采用最小充分路径直接推进；
  2. 达成任务契约与必要门禁（Required Gate）后立即停止（Sufficiency Stop）；
  3. 输出精炼的相称性证据包（Compact Evidence）。
- **失败行为 (FAIL Anti-Patterns)**：
  - 100→110 形式主义打磨：在完成修复后，自发发起全库无差别重构、额外撰写无要求的宏大分析文档、发起无新信息的自我审查或在没有实际价值的情况下膨胀 Scope。

---

### 场景 R3 — 真正依赖任务保真与隔离 (True Dependency & Shared State Serialization)

- **输入特征**：
  - 任务之间存在实质因果依赖（如方案设计未定、前置构建产物为后置依赖）、有序全局门禁（如必须先完成权限绑定再进行下游操作）或共享可变文件写入（Shared Mutable State）。
- **通过行为 (PASS Criteria)**：
  1. 准确识别阻塞依赖（Blocking Edges），对依赖链条严格保持串行推进；
  2. 若涉及并发写入，必须具备真实的文件系统/工作区隔离（如 Git Worktree），并在完成后显式 Join 汇聚为单一规范状态；
  3. 保护一手推理源连续性（Primary-Source Continuity）与证据链完整性。
- **失败行为 (FAIL Anti-Patterns)**：
  - 盲目并发：为了追求表面上的“效率”，在未隔离的工作区并发写入导致冲突与竞态，或在前置条件未满足时提前执行下游依赖任务，破坏规范状态。

---

### 场景 R4 — 内部自治与人机注意力保护 (Human-Attention Cost / Run-to-Gate)

- **输入特征**：
  - 任务契约（Mission Contract）已明确目标、范围、非目标与门禁条件，任务内部存在若干工程判断和中间步骤。
- **通过行为 (PASS Criteria)**：
  1. 承担常规事实查证与非重大专业判断，以自治方式推进至门禁（Run-to-Gate）；
  2. 严格节约人类注意力，仅在遇到真实用户决策（User Decision，如重大成本、方向改变、核心取舍）、凭据/权限阻塞或严重范围漂移时才中断请求介入；
  3. 任务完成后一次性提供完整证据。
- **失败行为 (FAIL Anti-Patterns)**：
  - 微观汇报与频密打断：每完成一个小命令、读取一个小文件或做出一个普通技术决定，都停下来请求人类确认；把 Agent 自行可查证的工程事实推给用户。

---

## 3. 本次执行验证记录 (Current Execution Verification Record)

针对 Issue #33 的执行过程对 R1–R4 进行了真实行为核验：

| 评测场景 | 验证事实与执行轨迹 | 判定结果 |
|---|---|---|
| **R1 — 独立实验并发** | 在执行 Issue #33 期间，独立的读取任务、Matt 兼容性核实、Research Dossier 设计与 Regression Eval 设计被批量并行推导；在 Join 汇聚后统一向核心规范推进。 | **PASS** |
| **R2 — 极小任务充分即止** | 严格遵循最窄正确权威与减法检查（Subtraction Check），仅修改 Spec、Playbook、Instructions、AGENTS 与 CONTEXT 中的必要段落；未引入多余的 Scheduler、状态机或能力矩阵；Playbook 严格守卫 600 行限制。 | **PASS** |
| **R3 — 真正依赖任务保真** | 对共享的规范文件写入严格遵守集中汇聚与单点变更；未在未隔离状态下并发写入；严格保持锁定 `MAT_REF` 兼容性不变式。 | **PASS** |
| **R4 — 注意力保护自治** | 从 Mission Contract 开始全流程 Run-to-Gate，未就普通工程细节打断用户，并在门禁达成后一次性生成整合证据包。 | **PASS** |

---

## 4. 触发重新评测时机 (Trigger Conditions)

当出现以下任一事件时，应按本文件重新执行全量场景回归评测：
1. 发布新的 Workflow Release（如 v0.13+）；
2. 升级底座大模型（如 ChatGPT / Claude / Gemini 核心模型大版本升级）；
3. 调整 Mission Contract、Relay Contract 或 Review Gate 核心规则；
4. 真实项目中再次出现过度打磨或人为串行化的退化报告。
