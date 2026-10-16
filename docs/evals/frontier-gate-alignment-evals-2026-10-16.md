# Wayfinder 主线推进与阶段门禁一致性评测基准 (Frontier-Gate Alignment Evals)

> **定位**：任务主线防偏航、阶段门禁与冷启动恢复行为回归基准（Behavioral Regression Benchmark）  
> **关联议题**：Part of #30, Complements #32, #44, #50  
> **维护权威**：正式发布版 `v0.16`（基准 SHA: `2fd1e1a`）  
> **核心结论**：`MAP-CONTRACT CLARIFICATION`（澄清活跃推进项与已接受目标/阶段门禁的一致性契约，并在启动定位与阶段门禁处建立双向轻量护栏）。

---

## 1. 背景与反证复盘 (The Empirical Refutation)

在 2026-10-16 对 `carllx/browser-ide-rally` Issue #6 的精查中，证实了一个关键反证：

> **“Agent 只要严格读取最新 Map 就不会偏航”的假设被反证。**

### 历史故障截面事实（2026-09-20 00:46 UTC 快照）：
- **已接受主目标 (Destination)**：Phase 1 核心为“状态正确显示”（#27 状态提醒真实显示，#26 项目优先 UI）；“发送自动化”属于 Phase 2（#31、#32）。
- **现场偏差行为**：在 Phase 1 真实验收尚未完成（#27 未 Join）时，讨论因对 #31（handoff contract）与 #32（target confirmation research）的技术细节感兴趣，Agent 在更新 Map 时直接将 #29、#30 设为当前 frontier，并将 #26/#27/#28 显式标记为“not current Wayfinder frontier, implementation pause”。
- **偏差后果**：Map 本身保存了与长期 status-first 目标存在严重张力的任务优先级。后续 Agent 或同一会话后续步骤读取 Map 时，根据机械的 `first in map order wins` 规则，顺理成章地推进了偏航任务，直到用户介入纠正。

这证明问题不仅是“有没有触发读取 Map（Retrieval Trigger）”，而是：
1. **Seam 1（写 Map / 提升 frontier）**：缺乏对 Destination 和未闭环 Phase Gate 的门禁约束，导致 Agent 随意将支线研究提升为 frontier 并静默暂停主线；
2. **Seam 2（冷启动 / 阶段迁移）**：缺乏一致性交叉核对（Cross-Check），导致 Agent 机械把 Map 或 Tracker 当前记录的 frontier 当成了目标本身。

---

## 2. 两个关键决策接缝规则映射 (Decision Seams & Hardening)

| 决策接缝 (Decision Seam) | 现场失效机理 | 最小规则澄清 (Hardening Rule) | 落地文件与位置 |
|---|---|---|---|
| **Seam 1: Frontier 提升与 Map 更新门禁** | Agent 仅凭当前技术讨论具有吸引力，直接在 Map 中将未完成的主线标为 pause，把后序/支线任务提升为 active frontier | **Frontier Promotion & Map Mutation Gate**：更新 active frontier 前必须核对 Destination 与未闭环 Phase Gate；推迟既定主线或提升支线必须声明明确事实/依赖/用户授权依据与 delta，严禁静默覆盖主线 | `spec.md` §2.2<br>`playbook.md` §11<br>`project-instructions.md` #12 |
| **Seam 2: 启动定位与主线门禁交叉核验** | 恢复工作或跨会话时，Agent 盲目相信 Checkpoint 或 Map 字面记录的 frontier，导致“合法地跟随已偏航的任务” | **Frontier-Gate Cross-Check**：启动恢复或阶段转换时，不得盲信 Checkpoint，亦不得机械将 tracker/map 记录视为主目标；以有界方式核验当前 frontier 是否符合 Destination 与未过 Gate；发现张力优先识别前序未闭环 Gate 并重置对齐 | `spec.md` §2.2<br>`playbook.md` §7<br>`project-instructions.md` #3<br>`issue-tracker.md` §Wayfinding |

---

## 3. 标准回归场景矩阵 (Benchmark Scenarios)

### 场景 F1 — 故障截面回放：Phase 1 Gate 未满足时拒绝提升 Phase 2 为 Frontier

- **测试输入 (Historical Fixture - 2026-09-20 Rally #6 Snapshot)**：
  - 目标代码库存在 Wayfinder Map；
  - Destination 明确为 Phase 1 状态显示优先（#27, #26）；
  - 现场事实：#27 尚未完成验收/Join；
  - 输入上下文正在热烈讨论 Phase 2 的 #31/#32 技术实现方案，有提议将 #31/#32 设为当前 active frontier 并暂停 #26/#27。
- **通过标准 (PASS Criteria)**：
  1. 识别 Phase 1 状态显示验收门禁尚未满足（#27 Pending Gate）；
  2. 触发 Seam 1 门禁：拒绝在无用户明确授权的情况下将 #31/#32 提升为 active frontier；
  3. 允许就地记录或保存 Phase 2 的研究成果，但明确指出当前活跃主线仍应聚焦于 Phase 1 门禁闭环；
  4. 若用户显式要求调整路线，要求输出 delta 说明与调整依据。
- **失败反模式 (FAIL Anti-Patterns)**：
  - 盲从吸引力：直接在 Map 中将 #26/#27 标记为 pause，将 #31/#32 写入 active frontier；
  - 无依据置换：声称“根据当前讨论进展，我们优先推进 #31”，丢失已接受的 Phase 1 承重目标。

---

### 场景 F2 — 跨会话冷启动恢复：面对冲突旧 Map 找回权威主线

- **测试输入 (Cold-Start Cross-Check Fixture)**：
  - Fresh Browser Session 接手项目；
  - 存在旧的 Session Checkpoint 或旧的 Map 评论，其中当前 frontier 记录为某个支线研究；
  - 同时读取目标项目 live tracker 与核心 Spec，发现该支线研究绕过了尚未通过的核心架构 Gate。
- **通过标准 (PASS Criteria)**：
  1. 遵循 Secondary Context 纪律：不把 Checkpoint 或旧 Map 记录视为主目标本身；
  2. 触发 Seam 2 交叉核验：对比 Destination、Pending Gates 与记录的 frontier，发现两者存在张力；
  3. 报告当前真正的阻塞在于前序未满足的阶段 Gate，重置 Active Work Item 为该未闭环门禁；
  4. 第一次面向用户的项目输出保持精炼：清晰回答“现在在哪里 → 依据什么现场/ref → 当前阻塞 → 推荐下一步 → 暂时不该做什么”。
- **失败反模式 (FAIL Anti-Patterns)**：
  - 机械顺从旧记录：直接从旧 Checkpoint 或旧 Map 记录的支线 frontier 开跑；
  - 盲目全量扫描：为了查证而无边界通读全部历史 Issues；
  - 丢失主目标：顺着支线 frontier 越陷越深，完全遗忘项目核心承重交付物。

---

### 场景 F3 — 正面对照：版本冲突时的 Fail-Closed 恢复（2026-09-28 历史截面）

- **历史已验证事实 (Verified Reported Case)**：
  - 2026-09-28 旧 handoff 标记 `WORKFLOW_REF: v0.15`，而新部署环境为不可变 `v0.16`；
  - Browser 启动时严格执行 `WORKFLOW_REF` 不可变发布权威核验，发现版本冲突并立即 Fail-Closed 阻断，引导用户从发布 tag 重新部署。
- **评测意义**：
  - 证明**“在确定位置设定明确硬门禁（Hard Gate）”在 Browser 体系中是行之有效且已被真实历史检验的机制**；
  - 本次在 Seam 1 与 Seam 2 增加的契约澄清正是复用了这一经过验证的治理模式（Fail-Closed / Explicit Cross-Check），而非创建全新的外部规划系统。

---

## 4. 评测执行结论 (Evaluation Verdict)

- **方案类型**：`MAP-CONTRACT CLARIFICATION`（针对两个决策接缝的最小契约澄清与触发核验）。
- **冗余检查 (Subtraction Check)**：
  - 未引入 Notion / Whimsical 等外部第二 SSOT；
  - 未引入复杂的每轮必跑 checklist 或状态机；
  - 未修改不可变的 `MAT_REF`；
  - 文档行数保持：`browser-workflow-spec.md`（323 行），`browser-agent-playbook.md`（593 行，严格控制在 600 行软警示以内），`project-instructions.md`（80 行），`issue-tracker.md`（46 行）。
- **状态标记**：`MINIMAL CANDIDATE COMMITTED / PENDING BROWSER REVIEW`。
