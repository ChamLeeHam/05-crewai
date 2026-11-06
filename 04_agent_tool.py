import time

from crewai import Agent, Task, Crew, Process

from config import get_llm
from ddgs import DDGS
from crewai.tools import tool
llm = get_llm()


@tool("get_stock_info")
def get_stock_info(stock_code:str):
    """根据stock_code股票代码获取最近的股票信息"""
    try:
        with DDGS() as ddgs:
            results =  ddgs.text(
                query=f"股票代码：{stock_code}",
                max_results=10,
                region="cn-zh",
                timelimit="m"
            )

            output = []
            for i, result in enumerate(results, 1):
                output.append(f"【结果{i}】")
                output.append(f"标题：{result['title']}")
                output.append(f"来源：{result['href']}")
                output.append(f"摘要：{result['body']}")
                time.sleep(1)

            return "\n".join(output) if output else "没有找到相关信息"
    except Exception as e:
        return f"搜索失败：{str(e)}"

# 智能体
reseacher = Agent(
    role="股票研究员",
    goal="根据用户指定的股票代码分析股票的涨跌情况",
    backstory="你是一位专业的股票研究员，擅长分析股票的涨跌情况，请根据用户指定的股票代码分析股票的涨跌情况，并提供决策建议，比如：抛出或者买入。"
              "请根据当前股票行情分析，使用以下工具："
              "**get_stock_info**:根据股票代码获取股票信息",
    llm=llm,
    tools=[get_stock_info],
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




if __name__ == '__main__':
    # result = get_stock_info("600418")
    # print(result)
    result = crew.kickoff()
    print(f"最终结果：{result}")