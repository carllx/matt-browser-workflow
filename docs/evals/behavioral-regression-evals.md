# Behavioral Regression Evals: Mission-Level Efficiency & Session Targeting

> **定位**：长期行为回归套件与评测基准（Durable Behavioral Regression Artifact）  
> **关联议题**：Part of #32, Implementation of #33, #36  
> **核心目的**：建立跨模型版本、跨工作流迭代的执行姿态（Execution Posture）与跨端中继防退化守护基准，验证 Agent 是否在满足正确性、权威性与门禁的前提下表现出使命级效率与精准的会话目标指示。

---

## 1. 为什么本评测资产值得长期存在 (Rationale for Long-Term Existence)

模型天然存在“为了显得周全而过度执行（100→110 polishing）”、“遇到多步骤任务默认串行处理”以及“在提示词/上下文变长后逐渐遗漏 cross-session targeting 细节或凭空推测会话存活”的统计归纳偏好。即使在提示词中写入原则，若缺乏明确的场景基准，随着底座模型微调、提示词微调或跨端中继重构，形式主义、低效串行与中继显著性退化极易反复回潮。

本回归套件提供 5 个标准场景（R1–R5），重点评估**规划结果、执行姿态与跨端中继指示**，不硬编码固定的实现细节或子代理数量，作为工作流发布与模型升级时的必要门禁验证。

---

## 2. 核心场景评测矩阵 (Evaluation Scenarios R1–R5)

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

### 场景 R5 — 显式且有据的 IDE 会话目标指示 (Session Targeting Advice & Fact-Grounded Placement)

- **输入特征**：
  - Browser 向用户生成并派发需要转交 IDE 的 Work Order，涵盖以下典型场景：
    - **5a（新独立 Issue / Fresh Browser 会话）**：Fresh Browser 会话接收新的独立 implementation Issue（自包含 Work Unit），无前序已核实的活跃 IDE 会话；
    - **5b（同 Issue 窄修正 / 活跃连续会话）**：在同一次开发推进中派发紧密相邻的局部修正 Work Order，已知 IDE 会话健康且仍需一手推理延续；
    - **5c（退化信号感知）**：IDE 会话出现重复读取、遗忘 acceptance 或前后矛盾等退化信号；
    - **5d（生命周期独立）**：Browser 会话轮次较多但 IDE 端独立且上下文健康。
- **通过行为 (PASS Criteria)**：
  1. 每次下发 Work Order 时，均显式包含会话目标指示（`Continue current IDE session` 或 `Fresh IDE session`）；
  2. 附带清晰简要的一句话事实依据（One-line rationale）；
  3. 场景 5a 建议 `Fresh IDE session`，说明为独立 Work Unit 且无已核实 IDE 状态，不臆测 Continue；
  4. 场景 5b 建议 `Continue current IDE session`，说明上下文健康且延续当前一手推理；
  5. 场景 5c 建议 `Fresh IDE session`（或 Clear/重置），说明检测到上下文退化信号；
  6. 场景 5d 保持生命周期独立，不因 Browser 会话长度机械要求 IDE 重启，反之亦然；
  7. 决策极简清晰，不引入复杂状态机、token 阈值或长 checklist。
- **失败行为 (FAIL Anti-Patterns)**：
  - 静默退化：Work Order 完全遗漏 Session Targeting Advice；
  - 无依据连续性臆测：在 Fresh Browser 会话或缺乏已核实证据时，凭空假定某个既往 IDE 会话存在并指示 Continue；
  - 机械全量 Fresh（破坏正常推理连续性）或机械全量 Continue；
  - 将 `/handoff` 误用为普通 Work Order 中继。

---

## 3. 可重复执行的运行时冒烟评测协议 (Published Immutable Test-Only Prerelease Protocol)

依据 Issue #35 决策，为解除“未发布候选无法通过 Fail-Closed 部署”的循环依赖，评测**严禁直接将未发布的 PR 分支内容作为正式 Project Authority 部署**，而是采用**已发布的不可变测试专用预发布版本（Published Immutable Test-Only Prerelease）**路径：

### 核心坐标定义 (Audit Coordinates)
- **`H`**：经过静态 Browser Review 批准的不可变生产候选提交（Underlying Reviewed Candidate SHA）；
- **`S`**：仅包含测试身份元数据覆盖的独立冒烟提交（Identity-Only Smoke Overlay Commit），满足 `parent(S) == H` 且 `H...S` 仅有元数据差异；
- **`T`**：指向提交 `S` 的测试专用不可变预发布标签（Test-Only Prerelease Tag，格式为 `smoke/issue-<N>/<short-H>`）。

---

### 标准评测执行步骤 (Standard Protocol Steps)

#### 步骤 1：前置条件检查 (Precondition Check)
- 确认目标代码仓库已启用 GitHub 仓库级不可变发布保护：
  ```bash
  gh api -H "X-GitHub-Api-Version: 2026-03-10" /repos/<owner>/<repo>/immutable-releases --jq .enabled
  ```
  必须验证输出为 `true`。

#### 步骤 2：构建不可变测试冒烟提交与预发布 (Create Smoke Overlay & Publish Prerelease)
1. **创建仅包含身份覆盖的提交 `S`**：
   - 从 `H` 签出临时冒烟分支或 worktree；
   - **仅允许修改** `chatgpt-project/project-instructions.md` 的身份元数据：
     - 添加 `CANDIDATE SMOKE ONLY / NOT ACCEPTED STABLE RELEASE` 明确标识；
     - 将 `WORKFLOW_REF` 填为专用冒烟 tag 名 `T`（如 `smoke/issue-33/68317cb`）；
     - 必要时同步顶部版本展示为同一 smoke identity；
   - **严禁修改**任何 Spec、Playbook、行为规则或生产候选逻辑；
2. **发布不可变测试专用 Prerelease**：
   - 依据提交 `S` 创建并发布 GitHub Prerelease：
     - 标签名称：`T`（如 `smoke/issue-33/68317cb`）；
     - 标题与描述：必须醒目标注 `CANDIDATE SMOKE ONLY / NOT ACCEPTED STABLE RELEASE`；
     - 参数设置：`prerelease: true` 且 `make_latest: "false"`（绝不得成为 latest release）；
3. **GitHub API 不可变性机器核验**：
   - 发布后立即通过 GitHub API 查询该 release，机器核验满足：
     - `prerelease == true`
     - `immutable == true`（受仓库级 Immutable Releases 保护）
     - target commit SHA 严格等于 `S`。

#### 步骤 3：部署隔离测试项目 (Deploy Isolated Test Project)
1. 在 ChatGPT / Claude 网页端创建或重置一个**独立的测试专用 Project**（严禁覆盖生产 Project）；
2. 从该 published immutable prerelease `T` 获取 `project-instructions.md` 填入 Instructions（配置测试仓库绑定）；
3. 从该 prerelease `T` 上传 `browser-agent-playbook.md` 与 `browser-workflow-spec.md` 至 Project Sources；
4. 开启 Fresh Session 验证启动，确认 Fail-Closed 身份核验通过。

#### 步骤 4：多会话注入标准场景测试 Prompt (Inject Fixtures in Fresh Sessions)
为避免跨场景上下文污染与推理残留，**各场景使用一个独立的 Fresh Browser Session** 分别评测：

- **R1 测试 Session（独立实验并发）**：
  > “请针对当前项目的三个独立依赖库 A、B、C（分别用于解析、序列化、网络请求）调研其最新兼容性与迁移风险，供我们决策技术选型。请给出你的执行计划与 Work Order。”
  - *观察重点*：Browser 是否将 A/B/C 识别为无依赖的并行/批量候选；是否生成共享闭环边界的 Work Order；是否要求 IDE 完成后返回单一整合报告。

- **R2 测试 Session（小任务充分即止）**：
  > “请将 `CONTEXT.md` 中的拼写错误 'reciver' 修复为 'receiver'，并运行 linter 确保通过。”
  - *观察重点*：Browser 是否直接输出精炼 Work Order；IDE 报告修复并给出测试输出后，Browser 是否直接通过门禁并停止，不自发追加全文词汇重构或冗长说明。

- **R3 测试 Session（真正依赖任务保真）**：
  > “我们需要首先确定重构方案架构设计（ADR），然后依据该设计修改核心核心数据模型 `model.py`，最后更新依赖它的 API 层 `api.py`。请派发执行计划。”
  - *观察严禁*：Browser 是否识别出 ADR → Model → API 之间的严格因果阻塞；是否拒绝在设计未决前盲目并发修改代码。

- **R4 测试 Session（人机注意力保护自治）**：
  > “请自治执行 Issue #XX 的完整实现。这是已明确范围的 Mission Contract。请 Run-to-Gate 并返回最终结果。”
  - *观察重点*：执行端是否自治完成中间常规步骤，避免每个子命令都请求确认；是否仅在遇到真实重大取舍时才中断。

- **R5 测试 Session（显式且有据的会话目标指示，紧凑 4 轮合成交互）**：
  > *注：本 Session 为行为回归合成测试（Synthetic behavioral fixture），不执行真实 GitHub/IDE 操作，不要求解析真实 Issue 编号。Fixture 提供了已核实的 Session / Work Unit 现场前提事实，Browser 仅需据此生成 Work Order 与 Session Targeting Advice。*
  - **Turn 1（5a: 新独立 Work Unit / 无已核实 IDE 状态）**：
    > “这是运行时行为测试，不执行真实 GitHub/IDE 操作。假设一个新的独立 implementation Work Unit A 已由 `/to-tickets` 产出，其 scope 已核实；当前没有已核实的活跃 IDE 会话。请仅生成 IDE Work Order 与 Session Targeting Advice。”
    - *观察重点*：Work Order 必须显式包含 `Fresh IDE session`（或 `Open fresh IDE session`），并附简要理由（新独立自包含 Work Unit 且无已核实 IDE 连续性）；**严禁**无证据推断 `Continue current IDE session`。
  - **Turn 2（5b: 同一 Work Unit 窄修正 / 活跃健康会话）**：
    > “这是同一个 synthetic Work Unit A 的后续步骤。刚才在 IDE 会话中运行单测，发现还有一个边界用例需微调，已核实当前 IDE 上下文刚刚完成实现且完全健康，仍需一手推理延续。请给出下一步 Work Order 与 Session Targeting Advice。”
    - *观察重点*：Work Order 必须显式包含 `Continue current IDE session`，并附简要理由（同一 Work Unit 紧密窄修正，IDE 上下文健康且仍需一手推理延续）；**严禁**机械全量建议 Fresh。
  - **Turn 3（5c: IDE 出现退化信号）**：
    > “继续同一个 synthetic fixture。在当前 IDE 会话继续修正时，已核实 IDE 开始出现上下文退化信号（反复询问已知事实、丢失刚确认的验收标准、给出前后矛盾的改动）。请给出阶段边界的下一步 Work Order 与 Session Targeting Advice。”
    - *观察重点*：Work Order 必须显式包含 `Fresh IDE session`（或 Clear/重置会话），理由指出检测到 IDE 上下文退化信号。
  - **Turn 4（5d: Browser 会话变长但 IDE 健康）**：
    > “继续同一个 synthetic fixture。我们在 Browser 端已经进行了多轮长讨论与架构规划，当前 Browser 会话较长；但刚刚 IDE 端是刚开启且已核实健康的全新会话，并顺畅完成 probe。请给出下一步 Work Order 与 Session Targeting Advice。”
    - *观察重点*：Work Order 保持 `Continue current IDE session`（或依 IDE 自身状态健康判定），理由说明 IDE 独立且健康；**严禁**仅因 Browser 会话长度机械要求 IDE 重启。

#### 步骤 5：结果绑定与生命周期流转 (Lifecycle & Gate Closure)
评测结果必须同时绑定三元审计坐标：`Prerelease Tag T` + `Overlay Commit SHA S` + `Underlying Candidate Commit SHA H`。

- **若冒烟 FAIL**：
  - 返回 PR 分支修改生产代码 → 产生新生产候选 `H2`；
  - 重新从 `H2` 创建新 overlay `S2` 与新不可变 prerelease `T2`；
  - 历史 prerelease `T` 作为不可变证据保留，绝不移动或删除；
- **若冒烟 PASS**：
  - 允许原生产候选 `H` 进入最终合并决策（Merge Decision）；
  - **最终合并进入 default 分支的是生产候选 H，而非仅包含测试身份的 overlay S**；
  - 历史已发布的 `v0.12` 属于 legacy accepted release，保持既有历史完整性，不追溯重写；
  - 未来所有正式工作流发布（Stable Releases）均继续使用仓库级 Immutable Releases 受保，smoke prerelease 绝不等于已发布的正式工作流版本。

---

## 4. 验证状态矩阵 (Verification Status Matrix)

区分**静态/代码审查验证 (Static Pre-Deployment Verification)** 与 **候选运行时行为冒烟验证 (Live Browser Runtime Smoke)**：

| 评测维度 / 场景 | 静态与规范审查 (Static / Spec Review) | 候选部署运行时冒烟 (Live Browser Runtime Smoke) | 审计坐标与备注说明 |
|---|---|---|---|
| **代码规范与 600 行检查** | **VERIFIED (PASS)** | N/A (静态检查) | Playbook 593 行，Spec 307 行，Evals 208 行，双轴 Review PASS |
| **仓库级 Immutable Releases** | **VERIFIED (PASS)** | N/A (前置环境配置) | GitHub API 验证 `enabled: true` |
| **R1 — 独立实验并发** | **VERIFIED (SPEC ALIGNED)** | `PENDING PRERELEASE SMOKE` | 待发布不可变 smoke prerelease 并注入 R1 fixture |
| **R2 — 小任务充分即止** | **VERIFIED (SPEC ALIGNED)** | `PENDING PRERELEASE SMOKE` | 待发布不可变 smoke prerelease 并注入 R2 fixture |
| **R3 — 真正依赖任务保真** | **VERIFIED (SPEC ALIGNED)** | `PENDING PRERELEASE SMOKE` | 待发布不可变 smoke prerelease 并注入 R3 fixture |
| **R4 — 人机注意力保护** | **VERIFIED (SPEC ALIGNED)** | `PENDING PRERELEASE SMOKE` | 待发布不可变 smoke prerelease 并注入 R4 fixture |
| **R5 — 显式且有据会话目标指示** | **VERIFIED (SPEC ALIGNED)** | `PENDING PRERELEASE SMOKE` | 待发布不可变 smoke prerelease 并注入 R5 fixture |

> **生命周期说明**：
> 本 PR 完成 Session Targeting Advice 运行时显著性修复与规范分层落地。由于真实 R1–R5 行为冒烟必须在候选产物发布为测试专用不可变 Prerelease 并部署至 Fresh Browser Session 后方可验证，**本 PR 不直接关闭主议题，保持相关 Issue 开启**，待运行时冒烟验证确认无误后，再行进入合并与后续工作流正式发布门禁。

