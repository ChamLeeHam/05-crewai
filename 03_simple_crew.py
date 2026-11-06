from crewai import Agent, Task, Crew, Process
from config import get_llm

llm = get_llm()

# 智能体
reseacher = Agent(
    role="股票研究员",
    goal="根据用户指定的股票代码分析股票的涨跌情况",
    backstory="你是一位专业的股票研究员，擅长分析股票的涨跌情况，请根据用户指定的股票代码分析股票的涨跌情况，并提供决策建议，比如：抛出或者买入。",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="内容撰写",
    goal="根据股票研究员的分析结果，撰写股票涨跌情况的介绍和决策建议",
    backstory="你是一位内容撰写专家，擅长根据股票研究员的分析结果，撰写股票涨跌情况的介绍和决策建议，注意：要具体的建议不要模拟两可的结论！",
    llm=llm,
    verbose=True
)

# 任务
reseacher_task = Task(
    description="""分析股票代码为600418的股票的涨跌情况
    要求：
    1. 用通俗易懂的方式介绍该股票的行情
    2. 提供决策建议，比如：抛出或者买入
    """,
    expected_output="根据过去的行情总结分析，给出未来3天的行情建议。",
    agent=reseacher
)
writer_task = Task(
    description="""根据股票研究员的分析结果，撰写股票涨跌情况的介绍和决策建议.
    要求：
    1、用通俗易懂的方式介绍该股票的行情
    2、提供决策建议，比如：抛出或者买入
    3、总字数不超过300字
    """,
    expected_output="使用markdown格式输出！",
    agent=writer
)

# 构建团队
crew = Crew(
    agents=[reseacher, writer],
    tasks=[reseacher_task, writer_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
print(f"最终结果：{result}")
