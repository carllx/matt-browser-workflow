# 最终 v0.15 范围裁决：有限前瞻

2026-09-11；base `96965df2206d970dade4972399c53cdaee974aea`。选择 B：MINIMAL PRODUCTION GAP。范围只涉及当前策略选择，不新增后续 feature。

## 证据与最窄归属

用户提供 Bounded Look-Ahead Evidence Brief：cross-desk-flow 2026-09-09/10，Case 1 产品壳/可靠性、Case 2 cold-login/#22 Dictation、Case 3 两端只读采证及串行 reboot 反例。它是历史提取报告，不是本执行者独立取得的完整时间线；报告中的 Verified 标签不自动升级为本轮独立核实。Case 1/2 的提前收益属反事实推断，Case 2 后来 superseded 不证明当时即可取消当前验收。

现有 Spec §2 的关键路径/边际价值与 §10 的依赖/隔离、Playbook §12 的派发扫描/共享闭环足以拥有这项要求；缺的是在当前策略定型前，用已知 successor 的语义反查当前前提，而非只对已选任务排序。Case 2 是主要区分证据；Case 3 与 reboot 反例支持“关联不等于一起执行”。

Subtraction：替换 Playbook 原有 Browser 权属与依赖扫描条款中的操作部分，不新增章节、名称体系或扫描步骤；Spec、Instructions、AGENTS不复制同义表达。既有项目指针作为入口，只核对会改变当前选择的必要关联；无关联不展开；后续计划不自动生效，不扩大授权。

## 有界验证

复用现有 probe_treatment 子代理，非 fresh、非盲化、非统计 A/B；只读取候选 Playbook §12.A，对R7五个短输入给出实际建议，不读取eval评分表。第一轮输出如下（完整）：

A. 登录恢复策略应恢复到 normal 的 speaker-only 状态，并保证 mic 可在 request 时启用、结束后还原 speaker，避免把“登录即持续启用 mic”固化为成功条件。当前只实现可靠性所需的恢复能力，不提前实施完整 Dictation 流程。

B. shell 不必等待所有 reliability 工作完成：已有 controller IPC，可将独立的状态展示与 Start/Stop 工作分开安排，仅把确实依赖 reboot 的验收留到恢复后。当前授权只涵盖可靠性，因此先推进可靠性，shell 实施需取得范围授权。

C. 两端的只读日志与注册状态可以并行采集，标明主机、同次 reboot 标识和时间，汇总比对启动失败链。采证期间保持现场不变，不同时修复或重启以免污染归因。

D. 按既定门禁先执行 Windows reboot 并验证启动结果，失败则留在 Windows 定位和修复。只有 Windows reboot PASS 后才执行 Mac reboot，分别保留前后状态与证据。

E. 直接完成局部拼写修正，按明确标准验证并提交最小充分反馈。后续工作没有相关依赖，无需额外扫描或扩展当前范围。

主控评分：B/C/D/E符合R7；A为PARTIAL，未先区分未来语义与当前验收。针对这一个问题，生产条款补上“后续方案尚未生效时，不自动替换当前已接受的验收条件”。复核输入明确当前dual-active验收仍生效、下一阶段speaker-only未实施/未授权，并提供首次问题反馈；因此属于边界澄清后的带反馈复核，不是同输入独立对照。实际回答：

> 当前 cold-login 恢复仍按已接受的 dual-active 验收实现与验证，同时让恢复策略便于下一阶段切换，避免将 dual-active 硬编码为永久要求。Dictation 的 speaker-only 契约尚未生效，只有获得明确授权并更新当前验收后才能切换。

该回答符合澄清后的边界；最终条款仅增加这一限制，B-E相关行为未改，不为取得更多PASS追加轮次。人工负例校验：永久忽视successor、无授权启动shell、reinstall抹现场、同时reboot、无关工作全库扫描，均被R7对应判据拒绝。人工判据检查不是模型执行结果。

## 限制与冻结

本候选属于规范性行为强化；没有证明长期 runtime reliability、成本或工期改善，没有重建完整历史/真实Browser部署。无全tracker扫描、计划维护、状态机、第二SSOT、Parent模型专属规则；不修#40诊断链、False No-READY或context degradation，不改MAT_REF。

此项裁决后 v0.15 功能范围冻结：已合并的范围保真 + 本候选的有限策略前瞻；后续只允许本候选的审查/必要修正，不继续发现下一项v0.15功能。未合并、未tag、未release。