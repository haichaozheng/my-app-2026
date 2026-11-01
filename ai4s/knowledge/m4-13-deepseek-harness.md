# DeepSeek Harness（dsh）使用指南

> **引入时机**：W7 | **核心挑战**："编程智能体harness是什么？它和opencode/cursor有何异同？如何用它开发Mesa仿真模型并留下可审计的开发痕迹？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

W1起你一直在用opencode/cursor做AI辅助编程，已经把"编程智能体"当成工作习惯。但如果你只用过一家工具，容易把**产品**误认为**类别**——以为编程智能体"就是长这样"。W7引入第二个harness（DeepSeek Harness，下称dsh），让你在真实任务（开发Mesa基线模型）中做一次双工具对比，体会harness是可替换的类别：模型可换、工具可换、界面可换、甚至agent loop本身都可换。这种"harness自觉"是AI4S工具栈方法论的一部分——工具栈服务于研究，而不是研究绑定在某个工具上。

同时，dsh的**Trajectory视图**（逐步展示模型响应、工具调用、嵌套活动、token用量与耗时）是"每一次LLM调用可审计"理念的现成教具：你开发Mesa模型的过程本身就留下了完整的机器可读痕迹，与仿真阶段的LLM调用日志互相印证。

## 这个知识点的核心内容

### 什么是harness，dsh是什么

**Harness（运行时脚手架）**：围绕大模型构建的agent运行环境——工具调用、会话管理、系统提示组装、沙箱与审批、子智能体编排。模型是"大脑"，harness是"身体"。opencode、cursor、Claude Code、dsh都是harness。

**dsh的差异化主张——"一切皆插件"（everything is a plugin）**：基于Cordis插件运行时构建，模型适配器、工具注册表、会话日志、agent loop、甚至Web UI本身都是可挂载、可卸载、可替换的插件。没有需要打补丁的特权内核：扩展dsh = 在其他插件旁边挂一个新插件。它也是model-agnostic的——任何OpenAI兼容provider（包括DeepSeek、OpenAI、Anthropic等）都能接入，不锁定DeepSeek自家模型。

**四种agent模式**：

| 模式 | 给你什么 |
|---|---|
| Standard | 完整编程智能体：文件编辑、shell、文件与网络搜索、skills、规划、子智能体 |
| Code | 通过Code Mode SDK把工具暴露给模型，让模型在一个程序里组合多步操作 |
| Minimal | 只有两个工具（持久shell + str_replace编辑器）的极简循环 |
| Creator | 检查运行时、在内存中测试插件、组合出新模式 |

> 与W4/W5的呼应：dsh的plugin/subagent架构是"主Agent编排 + 子智能体各受权限约束"的同类思想，可作为理解opencode agents多智能体设计的第二参照系。

### 安装与启动（课程推荐路径）

**路径A（推荐）：Python SDK**——自带运行时，无需Node.js，与课程Python环境一致：

```powershell
# 在仓库根目录激活 .venv 后
py -3.13 -m pip install deepseek-harness-sdk
```

```python
from deepseek_harness import DeepSeekHarness

with DeepSeekHarness(
    dsh_home="C:/work/dsh-home",        # 隔离的harness主目录（勿指向 ~/.dsh）
    cwd="C:/work/mesa-project",          # 一次性/专用工作区
    provider="deepseek-official",
    model="deepseek-chat",
) as harness:
    result = harness.run(
        "帮我搭一个Mesa基线模型：Schelling隔离模型，网格100x100，两类智能体……",
        session_id="w7-schelling-001",
    )
print(result.final_response)
```

**路径B：Web UI**——需要Node.js，`npx @deepseek-ai/dsh web` 后浏览器访问 `http://127.0.0.1:3080`，界面内配置provider与API key。

**API key**：设置环境变量 `DEEPSEEK_API_KEY`（`$env:DEEPSEEK_API_KEY = "sk-..."`），与Mesa-LLM的DeepSeek后端共用同一把key。

### 在W7怎么用：以Mesa基线模型开发为案例

1. **开发**：用dsh（Standard模式）完成模块一的Mesa基线模型——对话式提出需求（智能体类型、状态、交互规则），让它生成、调试、运行代码
2. **审计**：打开Trajectory视图，逐步检视：模型每步说了什么、调用了哪些工具、读了改了哪些文件、token花在哪里——对照检查AI是否引入了隐蔽错误（呼应W7验证报告）
3. **留痕**：交付物中附dsh版本号与Trajectory摘要（会话统计：turns、steps、模型时间、工具时间、token用量）

### 与课程其他工具的关系

| 工具 | 角色 | 与dsh的关系 |
|---|---|---|
| opencode | 课程主力harness（W1-W9全程） | 双harness对比对象；W4/W5/W8多智能体架构**仍基于opencode agents实现，不迁移** |
| dsh | W7引入的第二harness，体验"会用"级 | 以Mesa开发为案例；Trajectory提供开发过程留痕 |
| Mesa / Mesa-LLM | ABM框架 / 把LLM接入仿真智能体决策 | dsh帮你**开发**Mesa模型；Mesa-LLM里的LLM是**仿真对象**——两者是"用AI写模型"与"模型里有AI"的区别，不可混淆 |

### 配套：Mesa-LLM默认走DeepSeek API

W7模块二仿真调用量大（每个智能体每步都调LLM），推荐DeepSeek API为默认后端（OpenAI兼容端点，国内访问稳定、成本低）：

```python
from mesa_llm.module_llm import ModuleLLM

llm = ModuleLLM(
    llm_model="openai/deepseek-chat",
    api_base="https://api.deepseek.com/v1",  # OPENAI_API_KEY 填 DeepSeek key
    system_prompt="你是一个……的仿真智能体。",
)
```

## 纪律与风险

- **developer preview**：dsh 2026-08进入公测，官方明示会有兼容性破坏变更。课程纪律与Mesa-LLM相同——安装后**锁定版本号**并在实验报告中记录，这本身就是可复现性训练的一环
- **安全**："一切皆插件"意味着社区插件与第一方插件权限相同，存在供应链风险——只装课程需要的官方插件；在一次性工作区/容器中运行，勿指向个人主目录
- **本体论澄清**：dsh是**编程智能体harness**，不是仿真框架，也不能替代Mesa-LLM扮演仿真中的LLM智能体（用任务型编程agent充当每步决策的仿真智能体，既重又贵且非其设计用途）

## 延伸阅读

- [DeepSeek Harness GitHub仓库](https://github.com/deepseek-ai/deepseek-harness)
- [dsh官方文档（含架构与Python SDK指南）](https://deepseek-harness.github.io/deepseek-harness/)
- [DeepSeek Harness产品页](https://www.deepseek.com/harness/)
- Cordis设计论文：*A Programming Paradigm for Spatiotemporal Composability*（"一切皆插件"架构的理论基础）
