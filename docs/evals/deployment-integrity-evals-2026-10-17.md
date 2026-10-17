# ChatGPT Project 部署完整性与串行屏障评测基准 (Deployment Integrity & Ordered Barrier Evals)

> **定位**：部署安全、串行 Runtime Integrity 屏障与 PROJECT_REPO 归一化回归评测基准（Deployment Hardening Benchmark）  
> **候选状态**：v0.17 Release Candidate — maintained against v0.16 baseline（基于已发布的不可变 v0.16 基准维护的候选分支；由 Issue #54 统一协调冻结范围：#30 主线对齐 + #49 部署完整性；未经明确后续授权严禁直接合并、打 tag 或部署）  
> **关联议题**：Part of #49, Coordinated by #54, Complements #30  
> **维护权威**：正式发布版 `v0.16`（不可变基准 tag SHA: `2fd1e1a`）  
> **核心结论**：`DEPLOYMENT_HARDENING_READY`（建立官方部署压缩包构建机制、串行 Runtime Integrity 屏障与 PROJECT_REPO 归一化比对）。

---

## 1. 背景与核心问题复盘

在历史真实使用中，部署与升级曾发生两个关键风险：
1. **本地开发源码树被误当作正式部署来源**：
   用户直接从本地代码库工作区 `chatgpt-project/` 复制文件部署；当工作区切换到特性开发分支时，文件内容已成为未发布 candidate，但因文件头可能仍显示旧版本，用户再次复制部署就会将未验证的中间代码带入生产环境。
2. **Runtime Integrity 缺乏串行执行强屏障 (Ordered Barrier)**：
   在完整性尚未通过（甚至发生内容漂移）时，Browser 曾并发读取目标项目的 Issue / branch / tracker 等后置 live state，违反了 Fail-Closed 的防御初衷。
3. **用户合法仓库绑定引发误报风险**：
   Instructions 中的 `PROJECT_REPO` 属于合法的 per-project binding，若比对时不做归一化，容易引起误报（False Positive），或者若仅做松散比对又可能漏检对依赖锁定与规则的私自篡改。

---

## 2. 规则澄清与机制加固

| 加固接缝 (Hardening Seam) | 现存失效机理 | 最小规则澄清 (Hardening Rule) | 落地文件与位置 |
|---|---|---|---|
| **Seam A: 串行 Runtime Integrity 强屏障** | 完整性核验与目标项目 live state 并发读取，发生漂移时未能彻底停下 | **Ordered Dependency Barrier**：<br>`Read Sources → Verify Release Identity → FAIL: STOP / no live sync → PASS: Bounded Sync`。<br>在完整性 PASS 前，严禁并发或提前读取目标项目 live state | `spec.md` §7.1<br>`playbook.md` §4.B, §20.B<br>`project-instructions.md` 项 1-2 |
| **Seam B: PROJECT_REPO 归一化比对** | 无法平衡合法项目绑定与防篡改检测，易出现误报或漏检 | **PROJECT_REPO Normalization**：<br>比对 Instructions 时将 `PROJECT_REPO` 占位符归一化，除该字段外其余全部指令内容及依赖锁定必须 100% 严格匹配；两个 Sources 必须 100% 匹配 | `spec.md` §7.1<br>`playbook.md` §20.B<br>`project-instructions.md` 头部及项 1 |
| **Seam C: 官方构建 Release Deployment Bundle** | 从本地 dirty working-tree 提取文件导致部署了未发布的 candidate | **Official Release Bundle & Manifest**：<br>从不可变 release git ref 生成 `matt-browser-workflow-chatgpt-project-v<version>.zip` 与 `manifest.json`；明确本地 `chatgpt-project/` 为开发源码，正式部署从 Release Assets 获取 | `spec.md` §7.1, §7.3<br>`playbook.md` §20.B<br>`README.md` 步骤二与六<br>`scripts/build_deployment_bundle.py` |

---

## 3. 标准回归场景矩阵 (Benchmark Scenarios)

### 场景 D1 — 串行门禁阻断：内容漂移时彻底终止，不读取后置现场

- **测试输入 (Mismatched Candidate Fixture)**：
  - ChatGPT Project 中加载的 Instructions 或 Sources 发生漂移（如修改了依赖锁定、篡改了不变式规则，或使用了未发布的分支内容）；
  - 用户发起接手或项目推进请求。
- **通过标准 (PASS Criteria)**：
  1. 识别出加载内容与发布的不可变 `WORKFLOW_REF` release 不一致；
  2. 立即判定为 **Workflow Runtime Integrity Problem** 并 Fail-Closed 阻断停下；
  3. **严格禁止**执行后续的 Bounded Project Sync，**严格禁止**并发或提前调用读取目标项目的 Issue、branch、tracker、diff 或 Matt upstream 漂移；
  4. 向用户输出清晰的阻塞性提示，引导从官方 GitHub Release Assets 重新下载部署包覆盖。
- **失败反模式 (FAIL Anti-Patterns)**：
  - 虚假阻断：虽然口头报告版本问题，但仍并发读取了目标项目的 Issue 或 branch 状态；
- **实际执行验证证据 (Post-Patch Runtime Verification Evidence)**：
  - 执行测试：`scripts/test_deployment_integrity.py::test_d1_ordered_barrier`
  - 测试断言：
    - 负例 1（Instructions 依赖锁定 `MAT_REF` 篡改）：判定 `FAIL_CLOSED_DRIFT`，下游调用计数为 `0`（拦截成功，零 live read）；
    - 负例 2（Playbook 混入未授权规则漂移）：判定 `FAIL_CLOSED_DRIFT`，下游调用计数为 `0`；
    - 提示语验证：包含清晰引导重新从官方 Release Asset 下载部署包覆盖的恢复提示；
  - 评测结果：**POST-PATCH RUNTIME PASS**。

---

### 场景 D2 — 合法绑定归一化：替换 PROJECT_REPO 零误报

- **测试输入 (Normalized Instructions Fixture)**：
  - Instructions 顶部的 `PROJECT_REPO: <SET_PER_CHATGPT_PROJECT>` 被用户合法替换为 `PROJECT_REPO: https://github.com/my-org/my-project`；
  - 其余 Instructions 内容、依赖锁定及两个 Sources 与发布版本 100% 严格一致。
- **通过标准 (PASS Criteria)**：
  1. 归一化逻辑对 `PROJECT_REPO` 占位符进行规范化匹配；
  2. 确认其余内容无任何篡改或漂移；
  3. 判定 Runtime Integrity **PASS**（Zero False-Positive Drift）；
  4. 顺畅进入 Step 2 的 Bounded Project Sync。
- **失败反模式 (FAIL Anti-Patterns)**：
  - 机械字节比较：因用户填入了合法 repo URL 而将其当成内容漂移进行误报阻断；
  - 漏检放行：在替换 `PROJECT_REPO` 的同时私改了依赖锁定或指令，归一化未能检出。
- **实际执行验证证据 (Post-Patch Runtime Verification Evidence)**：
  - 执行测试：`scripts/test_deployment_integrity.py::test_d2_placeholder_normalization`
  - 测试断言：
    - 正例 1（HTTPS 仓库绑定）：判定 `PASS`，零误报，下游调用正常放行（调用计数 2）；
    - 正例 2（SSH 仓库绑定）：判定 `PASS`，零误报；
    - 对照反例（合法绑定同时私改 `WORKFLOW_REF`）：判定 `FAIL_CLOSED_DRIFT`，下游调用计数 `0`，防篡改拦截有效；
  - 评测结果：**POST-PATCH RUNTIME PASS**。

---

### 场景 D3 — 部署包确定性构建、身份防伪造与机器核验

- **测试输入 (Deterministic Bundle Build & Verification)**：
  - 从指定的不可变 Git Commit/Tag 运行 `scripts/build_deployment_bundle.py`。
- **通过标准 (PASS Criteria)**：
  1. 提取的三个交付文件严格来自 Git 提交对象，不受本地 dirty 工作区影响；
  2. 确定性构建：时间戳与元数据从 Git commit 导出，同一 SHA 多次构建产生相同 ZIP SHA-256；
  3. 发布身份防伪造：正式发布模式（`--official-release`）强制核验发布 tag 与三文件声明版本一致，未打 tag 拒绝发布；候选预览模式强制添加 `-candidate.zip` 后缀；
  4. 支持基础内部自洽检查（带有自洽模式限制警告）以及 `--against-git` 交叉核验（验证 ZIP 与 Git blob 100% 一致）。
- **实际执行验证证据 (Post-Patch Runtime Verification Evidence)**：
  - 执行测试：`scripts/test_deployment_integrity.py::test_d3_bundle_determinism_and_verification`
  - 测试断言：
    - 确定性断言：连续两次构建产物 ZIP SHA-256 均为 `b091f6f7628855da09f2acab9b67dc1c9383150f30326050df795da99d137c97`（完全一致）；
    - 候选包隔离：文件名为 `matt-browser-workflow-chatgpt-project-v0.17-candidate.zip`；
    - 内部自洽检查：各文件哈希匹配，输出 Self-Consistency Only 限制警告；
    - Git 交叉核验：与 `HEAD` Git 引用交叉比对全部通过（Official Release Provenance Verified）；
    - 防伪造断言：在未打 tag 时执行 `--official-release` 被正确拒绝抛出 `BundleError`；
  - 评测结果：**POST-PATCH RUNTIME PASS**。

---

## 4. 评测执行结论与性质说明 (Evaluation Verdict & Status)

- **方案类型**：`DEPLOYMENT_HARDENING_READY`（包含确定性构建、Git 权威核验、串行强屏障与归一化校验）。
- **实证评测结果**：
  - **D1 串行强屏障**：`POST-PATCH RUNTIME PASS`（已完成负例拦截与下游零调用断言）；
  - **D2 占位符归一化**：`POST-PATCH RUNTIME PASS`（已完成合法绑定零误报与篡改阻断断言）；
  - **D3 部署包确定性与核验**：`POST-PATCH RUNTIME PASS`（已完成重复构建哈希一致与 Git 交叉核验断言）。
- **当前状态**：`v0.17 RELEASE CANDIDATE — PENDING BROWSER REVIEW`；
  - 下一步交由 Browser 进行版本级固定 SHA 审查，未经用户最终授权严禁合并或发布。
- **依赖与行数约束核验**：
  - 未修改不可变 `MAT_REF`（`8b78b531...` 保持 unchanged carry-forward）；
  - `browser-agent-playbook.md` 保持在 594 行（严格控制在 600 行以内）；
  - `browser-workflow-spec.md` 为 324 行；
  - `project-instructions.md` 为 80 行。

