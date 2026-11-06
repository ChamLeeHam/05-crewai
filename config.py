from crewai import LLM
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_llm() -> LLM:
    """获取配置好的 LLM 实例
    Returns:
    LLM: 配置好的语言模型实例
    """
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = "gpt-4o"

    if not api_key:
        raise Exception("OpenAI API key is required")

    return LLM(
        model=f"openai/{model}",
        api_key=api_key,
        base_url=base_url,
    )

def get_model_name() -> str:
    """获取模型名称
    Returns:
    str: 模型名称
    """
    return os.getenv("OPENAI_MODEL", "gpt-4o")

# 测试配置
if __name__ == "__main__":
    try:
        llm = get_llm()
        print(" LLM 配置成功！")
        print(f" Base URL: {os.getenv('OPENAI_BASE_URL')}")
        print(f" Model: {get_model_name()}")
    except Exception as e:
        print(f" 配置失败: {e}")