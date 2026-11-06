from crewai import Agent

from config import get_llm

llm = get_llm()

translator_agent = Agent(
    role="专业翻译官",
    goal="将用户的中文准确翻译成英文",
    backstory="""你是一位资深的中英文翻译专家，拥有10年翻译经验。你擅长将中文准确、流畅地翻译
    成地道的英文，同时保持原文的语气和风格。""",
    llm=llm,
    verbose=True,    #显示详细日志
)

# =============直接与Agent交互==================
# 使用kickoff() 方法直接与Agent对话

result = translator_agent.kickoff("今天天气真不错，鸟语花香。")
print(result.raw)