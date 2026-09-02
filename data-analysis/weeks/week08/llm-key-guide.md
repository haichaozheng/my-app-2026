# LLM API Key 获取与使用指南（W8）

> 本周产品要接入 LLM 智能解读，需要一枚可用的 API Key。按下面三条路径任选其一，**优先自己申请免费额度（路径①）**。

## 路径① 自行申请免费额度（推荐）

多数主流大模型平台对个人用户提供免费额度或免费模型，具体额度与规则以各平台官网为准：

- **国产平台**：智谱 GLM、硅基流动 SiliconFlow、通义千问、豆包（火山方舟）、Kimi、DeepSeek 等——通常注册即送新人额度，部分模型长期免费
- **国际平台**：OpenRouter（有免费档模型）、Google AI Studio（Gemini 免费层）、Hugging Face Inference
- 申请步骤通法：注册 → 实名认证（如需要）→ 控制台创建 API Key → 复制保存 → 查看免费额度与计费页，**设置消费提醒**

选型提示：中文财经语境下先试国产平台的免费档；LangChain 侧用 OpenAI 兼容接口（改 `base_url` 即可切换平台，见 `knowledge/phase2-2-13-llm-api.md`）。

## 路径② 课程演示 Key（兜底）

申请受阻（实名认证卡住、无支付方式、额度审批慢）时：

1. 在课程群按格式申请：`申请演示Key：学号+姓名+受阻原因`
2. 教师在群内回复当期共享演示 Key（有时效与限流，先到先得）
3. **使用规则**：仅限本地开发期间验证功能逻辑；**禁止**写入代码仓库、禁止用于 W10-W11 部署（上线前必须换成自己的 Key）；禁止转借他人

## 路径③ 完全没有网络条件

找教师约办公时间，现场用教师机完成功能验证并录制演示视频，功能设计文档照常提交。

---

## 安全红线（违反即须立即处理）

1. **Key 绝不写进代码**——用环境变量或 `.env` 文件读取：

```bash
# .env（加入 .gitignore，永不提交）
LLM_API_KEY=sk-xxxx
LLM_BASE_URL=https://api.example-platform.com/v1
```

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("LLM_API_KEY")
base_url = os.getenv("LLM_BASE_URL")
```

2. 已推送到 GitHub 的 Key 视同泄露：**立刻去平台吊销 → 重新生成 → 检查 git 历史**（`git log -p | grep sk-`）
3. 云端部署时用平台 Secrets 机制（Streamlit Cloud 的 `st.secrets` / 服务器 systemd 环境变量），详见 `weeks/week10/deployment-faq.md` 第四节
4. 用量自查：每周看一次平台控制台账单页，MVP 阶段的个人用量通常极低；出现异常增长立即吊销 Key 并报课程群
