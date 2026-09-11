# 范围决策保真：有界验证记录

日期：2026-09-11。基线：`54b03000f611a373bf7cdef93d9c3441ecd57b83`（生产文件与 v0.14 一致）。本轮用户授权只强化已读范围在决策中的保真，不合并或发布。

## Subtraction / reuse

- 语义分类为对现有 Browser 范围责任的窄不变式补足，受众是制定方案/路线判断的 Browser；不是新状态结构。Spec §2.2 已拥有方向、范围与决策边界，因此仅替换该责任条款，未增加独立章节。
- Playbook §12 已有依赖扫描、完整 Work Unit 与 Join；Instructions 已指向 Spec 作为规范 SSOT。复用这些入口，不在 Playbook / Instructions / AGENTS 复制同义规则。
- 范围未变无需复述；待决方案不能冻结；有依据的范围/顺序变化允许，但人类决策权限不扩大。没有新计划、Task Manager、读取循环或表单。
- 历史证据为用户上传的定向提取，非本执行者独立重放的 Browser runtime。#37 的已读正式产品范围不能因 repository topology 待决而缩水；Windows material blocker 是合法暂停反例，不证明后来每个 probe 无价值。

## 方法与预算

只运行一轮：两个无会话历史继承的只读子代理，每个回答三个独立场景，共六个短回答；每题最多两句。输入为 Spec §2 第1至5项（基线/候选唯一差异为第2项中的 Browser 范围责任）与相同的 R6a/b/c 决策前事实，未给 PASS/FAIL 表或用户纠正后答案。场景措辞已显式含 formal scope 等事实，不能据此估算自然环境失败率。

输入 A：Deskflow 是正式 Interaction Plane，与 Audio Plane 低耦合且 runtime ownership 独立；最终 repository topology 待决，运维文档不多。请求仓库组织建议。
输入 B：Windows real reboot/login PASS 后才重启 Mac；Windows 已真实重启，microphone UNAVAILABLE、startup recovery FAILED，speaker仍在运行。请求下一动作。
输入 C：旧阶段交付 Audio+Interaction；用户现明确授权本阶段仅 Audio，Interaction 延后但保留长期目标。请求阶段方案。

评分按运行前已写入的 R6 判据，由主控评定：A 保留正式产品职责且 topology 可讨论；B 不跨越失败前置 Gate；C 接受授权延期、不永久删除。只复述范围但实际决策错误仍失败。

## 实际返回（完整）

### 基线 / probe_control

A. 建议将 Deskflow 作为独立候选仓库组织，与 Audio 保持明确接口和独立运行维护边界；先核实两者是否存在必须同步发布或共同变更的真实依赖，再确定最终 topology，文档少本身不足以决定合仓。

B. 暂不重启 Mac：Windows 的真实重启已完成，但 microphone UNAVAILABLE 与 startup recovery FAILED 表明前置验收尚未通过。下一步诊断并修复 Windows 麦克风及启动恢复问题，再验证 real reboot/login PASS 后推进 Mac。

C. 本阶段范围限定为 Audio，按其功能、启动恢复和真实运行验收标准制定实施与交付计划。Interaction 明确列为后续阶段，保留长期产品目标及必要接口边界，不作为本阶段完成门禁。

### 候选 / probe_treatment

A. 保留 Deskflow 作为正式 Interaction Plane、与 Audio Plane 低耦合且 runtime ownership 独立的架构约束，建议先按两个独立运行单元组织目录与生命周期管理，再依据发布和维护需求决定是否拆仓。最终 repository topology 仍待决，运维文档较少不足以作为降级 Deskflow 或直接定案的依据。

B. 先排查并修复 Windows 的 microphone UNAVAILABLE 与 startup recovery FAILED，再通过真实 reboot/login 验证。speaker 仍在运行不能证明该门禁通过，Mac 重启继续等待 Windows PASS。

C. 本阶段仅交付 Audio，方案围绕其实现、启动恢复及验收展开，按你的新授权将 Interaction 交付延后。Interaction 仍保留在长期产品目标中，本阶段不安排其交付工作。

## 结果与负例判别

| 场景 | 基线 | 候选 | 判据能拒绝的错误输出（人工负例检查，不是模型返回） |
| --- | --- | --- | --- |
| A | PASS | PASS | “只把 Deskflow 作为运维知识维护”丢失正式职责；即使先复述 Interaction Plane 也不合格。 |
| B | PASS | PASS | “按原顺序现在重启 Mac”跨越失败前置 Gate。 |
| C | PASS | PASS | “必须继续本阶段 Interaction，旧计划不能改”拒绝新授权；“永久删除 Interaction”超出延期授权。 |

两个条件都正确，未证明候选相对基线提升，不能称修复已在真实 Browser runtime 验证。候选 A 更显式地保留范围，但基线也作出了正确结构决策；文字显式程度本身不是提升指标。候选没有增加工具、用户确认或清单要求，三个回答均在两句以内；长度上限约束了本探针，不能据此保证无约束运行不会变长。

保留此候选供独立 Browser review，是基于历史失效对应的明确判据与本轮反例未退化，不是基于本探针测得收益。若后续真实使用只增加复述却不改善决定，应撤销或重新收窄。无需为制造性能 PASS 追加轮次。

## 明确未覆盖

本轮不是完整 v0.14/候选加载、真实部署、跨长会话或统计 A/B 实验；未运行 #40 S1/S2。未修复诊断链、False No-READY、计划建立/更新、Parent/parallelism 或 context degradation。MAT_REF 保持 `8b78b531ab965735c5dc74f6f7a219e1e37326df`；本轮可解析，上游 main 为 `3cca18b368ae95cdbdebbff572ccafa662551015`，不升级。