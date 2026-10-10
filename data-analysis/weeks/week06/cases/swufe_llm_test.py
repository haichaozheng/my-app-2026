"""测试调用学校的大模型 API（OpenAI 兼容接口）。

Base URL：http://llm.swufe.edu.cn/v1
模型：deepseek-ai/DeepSeek-V4-Flash-0731

运行前：
  - 安装依赖：pip install openai python-dotenv
  - 配置密钥：在本目录 .env（或仓库根目录 .env）中写入：
      SwufeModel_API_KEY=sk-你的APIKey
    参考同目录 .env.example；.env 已在 .gitignore，不会提交入库。

用法：
  python swufe_llm_test.py                            # 默认发一句"你好"，验证连通
  python swufe_llm_test.py "写个数据分析的笑话"          # 换成你自己的问题
  python swufe_llm_test.py "你好" ZhipuAI/GLM-5.2      # 换成其它模型
  python swufe_llm_test.py --list                     # 列出网关上现有的模型
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

BASE_URL = "http://llm.swufe.edu.cn/v1"

# 网关上现有的模型（模型名区分大小写，须完整复制）
MODELS = {
    "deepseek-ai/DeepSeek-V4-Flash-0731": "DeepSeek 文本对话（默认）",
    "ZhipuAI/GLM-5.2": "智谱 GLM 文本对话",
    "Qwen/Qwen3.8-Flash-Next": "通义 Qwen 文本对话",
    "Qwen/Qwen3-VL-32B": "通义 Qwen 多模态（支持图片输入）",
}
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V4-Flash-0731"

CASES_DIR = Path(__file__).resolve().parent
# 优先读本目录 .env，再读仓库根目录 .env（dotenv 默认不覆盖已加载的值）
load_dotenv(CASES_DIR / ".env")
load_dotenv(CASES_DIR.parents[3] / ".env")


def get_api_key() -> str:
    api_key = os.getenv("SwufeModel_API_KEY")
    if not api_key:
        raise SystemExit(
            "未找到 SwufeModel_API_KEY。请在本目录（或仓库根目录）新建 .env 文件，写入：\n"
            "  SwufeModel_API_KEY=sk-你的APIKey\n"
            "可参考同目录 .env.example"
        )
    return api_key


def chat(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """把 prompt 发给指定模型，返回回复文本。"""
    client = OpenAI(api_key=get_api_key(), base_url=BASE_URL)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content


def list_models() -> None:
    print(f"网关可用模型（base_url={BASE_URL}）：")
    for name, desc in MODELS.items():
        print(f"  {name:<32} {desc}")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] in ("-l", "--list"):
        list_models()
        return

    prompt = sys.argv[1] if len(sys.argv) > 1 else "你好"
    model = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL
    if model not in MODELS:
        print(f"提示：{model} 不在已知模型列表中，仍然尝试调用。")
        list_models()

    print(f"模型：{model}")
    print(f"问题：{prompt}")
    print(f"回复：{chat(prompt, model)}")


if __name__ == "__main__":
    main()
