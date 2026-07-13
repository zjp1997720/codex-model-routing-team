# Codex 模型路由团队

[English](README.md)

让 Codex 的主 Agent 继续负责规划、集成和验收，同时把复杂任务交给可指定模型与推理强度的后台 Worker。

## 为什么做这个 Skill

Codex 原生 MultiAgentV2 当前没有暴露按 Worker 选择模型和推理强度的能力。原生 Subagent 会继承当前会话模型，并行任务可能因此产生远高于预期的 Token 成本。

这个 Skill 改用 Codex App 的独立后台任务。主 Agent 负责判断复杂度、拆分任务、分配文件所有权、整合结果和最终验收；后台 Worker 根据任务特点使用不同的可用模型与推理强度。

## 主要能力

- 只路由真正复杂且可并行的任务，例如多来源调研、多章节内容、复杂 Skill 或 PPT、跨模块开发和独立验证。
- 为后台 Worker 显式指定模型和推理强度，默认围绕 Sol 与 Luna 路由，禁止 Ultra。
- 每波最多新增 3 个任务，同时运行最多 6 个，单个根任务累计最多 8 个。
- 首个任务必须通过实体化检查；Worker 禁止继续派生任务；只归档已完成且结果被采纳的任务。
- 发布、付款、删除、账户操作和生产变更始终由主 Agent 执行。

## 环境要求

- Codex App 能够提供项目定位、后台任务创建、任务读取、追问和归档工具。
- 当前账号可以使用主 Agent 选择的模型与推理强度。
- Codex 工具环境运行正常。后台任务无法验证时，Skill 会停止委派并由主 Agent 接管。

## 安装

```bash
npx skills add zjp1997720/codex-model-routing-team -g -a codex --skill codex-model-routing-team -y
```

## 使用

直接对 Codex 说：

```text
使用 $codex-model-routing-team 并行调研这 6 个互不依赖的主题，最后统一核验并整合结论。
```

```text
使用 $codex-model-routing-team 分别实现、测试和审查 3 个独立模块，避免文件所有权重叠。
```

```text
使用 $codex-model-routing-team 准备一套培训 PPT，分别安排调研、写作和审查 Worker。
```

如果用户的 Codex 指令已经长期授权后台模型路由，这个 Skill 也可以在合适的复杂任务中自动触发。

## 工作方式

1. 主 Agent 先判断并行收益是否高于协调成本。
2. 第一个真实 Worker 充当健康探针，确认任务可以读取后才继续派遣。
3. 后续 Worker 按受控批次创建，并明确模型、推理强度、范围、文件所有权和验收标准。
4. 主 Agent 亲自核验事实和产物、处理冲突并完成最终交付。
5. 已采纳且完成的任务逐个归档。

完整规则见 [SKILL.md](SKILL.md)，配套策略见 [references](references/)。

## 本地验证

该工作流已在独立调研任务和绑定工作区的写入任务中完成本地实测，覆盖模型与推理强度核验、结果读取和串行归档。

## 许可证

[MIT](LICENSE)
