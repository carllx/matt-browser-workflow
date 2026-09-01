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

## 3. 可重复执行的运行时评测协议 (Repeatable Runtime Eval Protocol)

为确保在 Fresh Browser Session 下对候选规则进行客观、可复现的行为验证，执行以下标准评测协议：

### 步骤 1：部署候选指令与源文件 (Deploy Candidate Context)
1. 在 ChatGPT / Claude 网页端创建或重置一个测试专用 Project；
2. 将候选分支的 `chatgpt-project/project-instructions.md` 复制填入 Project Instructions（配置测试 repo 绑定）；
3. 上传候选 `chatgpt-project/browser-agent-playbook.md` 与 `chatgpt-project/browser-workflow-spec.md` 至 Project Sources；
4. 开启一个 **Fresh Session**，确认启动身份识别无漂移。

### 步骤 2：注入标准场景测试 Prompt (Inject Scenario Fixtures)
向该 Fresh Session 依次或分会话注入以下标准场景测试 Prompt：

- **R1 测试 Prompt**：
  > “请针对当前项目的三个独立依赖库 A、B、C（分别用于解析、序列化、网络请求）调研其最新兼容性与迁移风险，供我们决策技术选型。请给出你的执行计划与 Work Order。”
  - *观察重点*：Browser 是否将 A/B/C 识别为无依赖的并行/批量候选；是否生成共享闭环边界的 Work Order；是否要求 IDE 完成后返回单一整合报告。

- **R2 测试 Prompt**：
  > “请将 `CONTEXT.md` 中的拼写错误 'reciver' 修复为 'receiver'，并运行 linter 确保通过。”
  - *观察重点*：Browser 是否直接输出精炼 Work Order；IDE 报告修复并给出测试输出后，Browser 是否直接通过门禁并停止，而不是自发要求追加全文词汇重构或冗长说明。

- **R3 测试 Prompt**：
  > “我们需要首先确定重构方案架构设计（ADR），然后依据该设计修改核心核心数据模型 `model.py`，最后更新依赖它的 API 层 `api.py`。请派发执行计划。”
  - *观察严禁*：Browser 是否识别出 ADR → Model → API 之间的严格因果阻塞；是否拒绝在设计未决前盲目并发修改代码。

- **R4 测试 Prompt**：
  > “请自治执行 Issue #XX 的完整实现。这是已明确范围的 Mission Contract。请 Run-to-Gate 并返回最终结果。”
  - *观察重点*：执行端是否自治完成中间常规步骤，避免每个子命令都请求确认；是否仅在遇到真实重大取舍时才中断。

### 步骤 3：记录并评估结果 (Record & Score)
按照上述 Pass/Fail 判定标准填入执行评测记录表。

---

## 4. 验证状态矩阵 (Verification Status Matrix)

区分**静态/代码审查验证 (Static Pre-Deployment Verification)** 与 **候选运行时行为冒烟验证 (Live Browser Runtime Smoke)**：

| 评测维度 / 场景 | 静态与规范审查 (Static / Spec Review) | 候选部署运行时冒烟 (Live Browser Runtime Smoke) | 备注说明 |
|---|---|---|---|
| **代码规范与 600 行检查** | **VERIFIED (PASS)** | N/A (静态检查) | Playbook 590 行，Spec 306 行，双轴 Review PASS |
| **R1 — 独立实验并发** | **VERIFIED (SPEC ALIGNED)** | `PENDING DEPLOYMENT SMOKE` | 规范与操作语义已就绪，待候选部署后注入 R1 fixture |
| **R2 — 小任务充分即止** | **VERIFIED (SPEC ALIGNED)** | `PENDING DEPLOYMENT SMOKE` | 规则与触发词已就绪，待候选部署后注入 R2 fixture |
| **R3 — 真正依赖任务保真** | **VERIFIED (SPEC ALIGNED)** | `PENDING DEPLOYMENT SMOKE` | 依赖优先与 Join 不变式已写入，待候选部署后验证 |
| **R4 — 人机注意力保护** | **VERIFIED (SPEC ALIGNED)** | `PENDING DEPLOYMENT SMOKE` | Mission Contract 自治边界已强化，待候选部署后验证 |

> **生命周期说明**：
> 本 PR 完成静态规范与配置分层的落地。由于真实 R1–R4 行为冒烟必须在候选产物部署至 Fresh Browser Session 后方可验证，**PR #34 不自动 `Closes #33`，保持 Issue #33 开启（Open）**，待用户完成候选部署并执行运行时冒烟验证确认无误后，再行关闭并进入后续工作流发布门禁。
