- Stage A: 项目初始化与规划
    - Plan 1: 清理旧代码并建立项目计划
    [\u2713] 删除 engine、plugins、lucidity、persona、tests、web、deploy 等目录和 pyproject.toml 文件
    Notes: 目标是移除历史代码，为重新开发做准备。本次提交已通过 `git rm -r` 完成删除。
    ---
    - Plan 2: 制定开发计划
    [\u2713] 根据 PRD.md 制作阶段性开发计划并写入 plan.md
    Notes: 本计划概括未来各阶段的主要任务，与 PRD 中的 Sprint 计划基本保持一致，后续每完成一个阶段都会在此文档更新进展。
    ---
- Stage B: Turn Engine 与数据模型
    - Plan 1: 完成回合循环与 Tile/Agent 数据类，实现最基本的事件打印功能
    - Plan 2: 编写单元测试，确保核心逻辑可运行
- Stage C: LLM 插件与 JSON 校验
    - Plan 1: 实现可替换的 LLM 调用接口，默认 GPT-4o
    - Plan 2: 加入 JSON Schema 校验与自动重试机制
- Stage D: 数据持久化与重放
    - Plan 1: 使用 SQLite-WAL 存储事件日志和快照
    - Plan 2: 实现 `lucidity replay` 命令，保证结果可复现
- Stage E: 实时 WebSocket 与前端基础
    - Plan 1: 构建 WebSocket 服务推送 JSON Patch
    - Plan 2: 搭建 React 前端框架并显示地图与角色
- Stage F: UI 完善与事件流
    - Plan 1: 实现侧边栏和事件流界面，动态展示角色状态
    - Plan 2: 完成暂停、回放、恢复等控制功能
- Stage G: 配置向导与 Persona Builder
    - Plan 1: 提供零代码的启动向导和角色创建工具
    - Plan 2: 完成示例 persona YAML 集合
- Stage H: 集成测试与发布
    - Plan 1: 编写端到端脚本确保 docker-compose 一键启动
    - Plan 2: 完善文档并保持 ≥80% 单测覆盖率
