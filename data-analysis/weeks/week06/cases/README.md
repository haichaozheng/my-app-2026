# Week06 案例：调用学校大模型 API——连通测试与聊天网页

> 对应课堂 notebook：`../llm_api.ipynb`（DeepSeek 官方 API 版）
>
> 课堂 notebook 用 DeepSeek 官方 API。本案例换成**学校自己的大模型网关**：`http://llm.swufe.edu.cn/v1`。接口是 OpenAI 兼容格式——换平台只需改 `base_url`、模型名和 API Key 环境变量，调用代码一行不用动。

## 功能

- `swufe_llm_test.py`：读取环境变量 `SwufeModel_API_KEY` → 向学校网关发一条消息 → 打印回复。用于验证「密钥、网络、模型名」三件事都通了，是后续所有 LLM 应用开发的第一步。
- `chat_app.py`：Streamlit 聊天网页。侧栏切换模型（DeepSeek / GLM / Qwen）、改系统提示词、清空对话；多轮对话历史保留，回复流式输出。切换模型不清空历史——同一段对话发给不同模型，可以直接对比回答。

## 运行

```bash
# 1. 安装依赖
pip install -r data-analysis/weeks/week06/cases/requirements.txt

# 2. 配置密钥
cp data-analysis/weeks/week06/cases/.env.example data-analysis/weeks/week06/cases/.env
# 编辑 .env，填入你的 APIKey

# 3a. 命令行测试连通（默认用 DeepSeek 发一句"你好"）
python data-analysis/weeks/week06/cases/swufe_llm_test.py

# 换成自己的问题
python data-analysis/weeks/week06/cases/swufe_llm_test.py "用一句话解释什么是市盈率"

# 换模型（第二个参数）
python data-analysis/weeks/week06/cases/swufe_llm_test.py "你好" ZhipuAI/GLM-5.2

# 列出网关上现有的模型
python data-analysis/weeks/week06/cases/swufe_llm_test.py --list

# 3b. 聊天网页
streamlit run data-analysis/weeks/week06/cases/chat_app.py
```

打开 http://localhost:8501 即可聊天。

也可以把 `SwufeModel_API_KEY` 写在仓库根目录的 `.env` 里，与其它课程密钥放在一起。

## 网关上现有的模型

| 模型 ID | 说明 |
|---|---|
| `deepseek-ai/DeepSeek-V4-Flash-0731` | DeepSeek 文本对话（脚本默认） |
| `ZhipuAI/GLM-5.2` | 智谱 GLM 文本对话 |
| `Qwen/Qwen3.8-Flash-Next` | 通义 Qwen 文本对话 |
| `Qwen/Qwen3-VL-32B` | 通义 Qwen 多模态（支持图片输入，本脚本只发文本） |

模型名区分大小写、须完整复制。网关新增模型时，同步更新脚本里的 `MODELS` 字典即可。

## 文件

| 文件 | 说明 |
|---|---|
| `swufe_llm_test.py` | 最小测试脚本：读密钥 → 调用 → 打印回复 |
| `chat_app.py` | Streamlit 聊天网页：选模型、多轮对话、流式输出 |
| `.env.example` | 密钥模板，复制为 `.env` 后填入自己的 APIKey |
| `requirements.txt` | 依赖：`streamlit`、`openai`、`python-dotenv` |

## 与 notebook 的对应关系

| notebook（DeepSeek 官方 API） | 本案例（学校网关） |
|---|---|
| `base_url="https://api.deepseek.com"` | `base_url="http://llm.swufe.edu.cn/v1"` |
| `os.environ.get('DEEPSEEK_API_KEY')` | `os.getenv("SwufeModel_API_KEY")` |
| `model="deepseek-flash"` | `model="deepseek-ai/DeepSeek-V4-Flash-0731"`（另有 GLM、Qwen 可选） |
| `client.chat.completions.create(...)` | 同（OpenAI 兼容接口，调用方式完全一致） |

## 常见报错

| 现象 | 原因与处理 |
|---|---|
| `未找到 SwufeModel_API_KEY` | `.env` 没建或变量名拼错，对照 `.env.example` |
| `401 Unauthorized` | APIKey 填错或已失效 |
| 连接超时 / Connection error | 不在校园网环境，检查网络（部分网关需校园网或 VPN） |
| `model not found` | 模型名不对，区分大小写、须完整复制，用 `--list` 查看现有模型 |

## 密钥安全

- `.env` 已在 `.gitignore`，不要提交到仓库
- 不要在代码中硬编码 API key
