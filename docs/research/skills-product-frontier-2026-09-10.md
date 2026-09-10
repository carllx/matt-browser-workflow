# #13 当前产品事实有界复核

核实日期：2026-09-10。维护权威：v0.14；MAT_REF：`8b78b531ab965735c5dc74f6f7a219e1e37326df`。定位：Fact / Inference / Decision proposal；非生产权威。已实际读取 [#13 body 与 2026-08-17 两条评论](https://github.com/carllx/matt-browser-workflow/issues/13)，并打开以下六个官方主题页面；没有安装、修改账号、调用待测 Skill 或修改仓库。

## 当前事实与证据边界

| 问题 | 当前官方事实 | 对本项目的含义 |
|---|---|---|
| Chat / Work / Codex | Chat 偏对话，Work 承接可审查结果，Codex 提供开发工具视图；Work 也支持 shell、subagents 等，能力依赖平台、账号和工作区。[Use ChatGPT](https://learn.chatgpt.com/docs/use-chatgpt) | 不能再把 Browser 全部理解为没有工具执行能力，但本项目 Browser 默认 READ/VERIFY 权限不会随产品能力自动扩大。 |
| Projects | Web Project 共享文件、instructions、sources；能包含 Chat 和 Work；本地项目与 Web Project 的目录访问不同。[Projects](https://learn.chatgpt.com/docs/projects) | Project 保留项目上下文；Skill 不替代 Project，更不自动获得本地仓库授权。 |
| Skills | 官方区分 standalone（desktop / CLI / IDE）与 plugin bundled（亦覆盖 Web Chat/Work）；ChatGPT 用 @、Codex 用 $ 显式选择，二者也有隐式选择。[Build skills](https://learn.chatgpt.com/docs/build-skills) | 8月“网页上传独立 Skill 即可试验”不能直接作为当前执行步骤；需要先选目标 surface 与支持的承载路径。 |
| user-invoked | 同一 Build skills 页给出 agents/openai.yaml 与 allow_implicit_invocation:false，但效果说明明确写 Codex 不隐式调用。 | 尚未证明 ChatGPT Web 同语义；显式 @ 入口存在，不等于人类专属调用边界已经验证。 |
| Plugins | 官方将其定义为 skills / MCP 等安装包；个人单工作流先用 Skill，分享/连接服务再打包 Plugin。[Build plugins](https://learn.chatgpt.com/docs/build-plugins) | 支持分层共存，不支持将全 Matt 集迁移当默认答案；若 Web 承载需要包，也是分发机制需求，不是采用全架构的证据。 |
| 安装与权限 | 当前说明为 Plugins 页选择安装，可额外连接服务，新会话加载；IDE extension 不支持 plugins；账号与服务权限分别适用。[Plugins](https://learn.chatgpt.com/docs/plugins) | 目录存在或本地有工具不证明用户 ChatGPT Project 已可安装，也不证明已获安装或外发授权。 |
| 可复用工作流 | Skills 包含工作流及支持资源，Plugins 为安装共享路径；工作区设置影响共享。[Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins) | 可研究兼容性；未证明稳定性、成本、上下文收益或 nested invocation 保真。 |

## 8月记录应如何处理

- 保留为历史记录；不得继续把 `Plugins → Skills → Create → Upload from your computer`、scan / Needs Review / Blocked 完整路径写作本轮已核实事实。本轮六页没有确立该流程；也不据此断言已取消。
- “可自动/显式调用”仍获官方支持，但 standalone 与 bundled、Web 与 Desktop / Codex 必须区分。
- allow_implicit_invocation 在 Codex 的支持可确认；ChatGPT Web 的 human-only、嵌套 Skill、派生 artifact provenance 与更新语义仍未实测。
- issue 原始建议 wayfinder，8月后续评论已改为 grilling → human-only conversation Skill → wayfinder；不得忽略后续修正。

## 当前本地宿主证据

本会话系统暴露本地 Skill 目录、exec_command、native subagents、plugin 安装建议与卸载工具；可确认 Codex 侧具备这些接口。工具声明不证明任意自定义 Matt Skill 的 Web 安装可完成；未调用安装工具、未执行 capability smoke。推荐插件列表同样不等于自定义包已安装。

## 最小结论与下一 Gate

- KEEP CURRENT：现有 Project + locked Ref-Qualified Manual Invocation 保持生产路径。
- RESEARCH READY：本次公开文档已足以修正旧安装假设，无需等用户 UI 才可完成该研究切片。
- PILOT NOT YET VERIFIED READY：先确定目标是 ChatGPT Web/Work 还是 Desktop，验证该账号支持的承载/安装入口，准备 locked source 的最小 artifact 与 provenance，再取得实际安装与实验授权。不可把 Codex local smoke 冒称 Web pilot。
- ADOPT SKILLS / PILOT PLUGIN：目前没有效率与行为保真结果支持采用；只保留最小 grilling 单变量 pilot 的条件性选项。human-only 与 wayfinder 待前序条件成立。
- #13 不应因 research-ready 被误写为整体 BLOCKED；也不应因本次文档切片完成而宣称整项 deliverables（兼容性实测/性能）已完成。

本轮止于事实更新：没有生产改动、没有新依赖、没有安装/发布、没有模型或 Matt Authority 升级。

## 本轮 frontier Join

本轮从 main `ace0207936558fdade0fbe4391d197b120a0b355` 出发。以下为有界核实后的状态快照，不是新调度规则或第二 tracker。

| 工单 | 分项状态 / 最短下一步 |
| --- | --- |
| #13 | READY research 本轮已完成，纠正整体 BLOCKED 的判断；研究候选待 fixed-ref Browser review。完整 pilot / adoption 尚未成立。 |
| #18 | LIFECYCLE-CLOSE / SUPERSEDED：[旧 v0.10.1 Publish Gate](https://github.com/carllx/matt-browser-workflow/issues/18#issuecomment-5350364349) 已完成，旧部署目标被后继 release 替代；以 not planned 关闭，不补签部署 PASS。[v0.14 记录](https://github.com/carllx/matt-browser-workflow/issues/40#issuecomment-5567728419) 保留当前部署 unknown 的残余。 |
| #26 | LIFECYCLE-CLOSE / COMPLETED：正文已交付研究结论与 Revisit Triggers；关闭完成的研究，真实状态冲突/覆盖判断成本等触发时 reopen。 |
| #27 | DONE 实现、迁移及部分真实 smoke；BLOCKED runtime：真实新资源 zero-schema / 多实例场景。现有验收链准备充分，不重跑迁移；保留 OPEN，projection 属于 #30。 |
| #11 | BLOCKED formal release：本轮 `gh release view v1.2.4 -R mattpocock/skills` 为 release not found。正文已具锁定 ref、差量范围、重点语义与决策输出，未发现稳定且值得补齐的 preparation gap；不重复研究 floating main。 |
| #30 | CONDITION-TRIGGERED design：仍待真实投影/漂移/删除需要；保持四份 guidance Sources，不因 repo 已有 canonical 副本删除。 |
| #32 | CONDITION-TRIGGERED regression ledger：按既有决定保留 OPEN，需实际部署版本与直接失败轨迹改变候选选择；不恢复 #40 S1/S2。 |

#13 的最小 pilot 准备已明确：只选择一个目标 surface；model-invoked grilling 先于 human-only Skill，再先于 wayfinder。固定同一任务比较 manual/native，观察实际 invocation、输出、副作用与 provenance；没有本地测试可替代 Web 核验。具体派生包取决于目标承载路径，因此当前不预建包、安装器或分发项目。目标选定且账号入口可核实后，再从锁定 ref 取最小闭包、记录内容哈希，并在实际安装/实验授权及成本边界内运行；本轮未声称已准备好安装制品。

Decision：KEEP CURRENT；删除“不能 pilot 所以不能研究”的推断，更新研究中的产品事实，不新增生产 invariant。没有需要立即决定的产品迁移；本轮唯一交付 Gate 是研究候选的 Browser fixed-ref review，后续安装选择不与此 Gate 混淆。
