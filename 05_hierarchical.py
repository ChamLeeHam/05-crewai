from crewai import Crew, Process, Agent, Task
from config import get_llm

llm = get_llm()

researcher = Agent(
    role="市场研究员",
    goal="收集目标行业的市场规模、竞争格局、用户画像等数据",
    backstory="你是一名资深市场分析师，擅长从公开渠道获取高质量数据。",
    verbose=True,
    allow_delegation=False  # 专业代理通常不负责分配任务
)

analyst = Agent(
    role="数据分析师",
    goal="对收集的数据进行统计分析、趋势预测和洞察提炼",
    backstory="你精通数据建模和可视化，能从杂乱数据中发现商业价值。",
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role="报告撰写专家",
    goal="将分析结果转化为结构清晰、语言专业的商业报告",
    backstory="你有10年咨询报告写作经验，擅长用故事线串联数据。",
    verbose=True,
    allow_delegation=False
)

# ==================== 2. 定义任务（不绑定 agent，由 Manager 动态分配）====================
research_task = Task(
    description="""
    收集关于'中国新能源汽车市场'的最新数据，包括：
    - 2024-2025年市场规模和增长率
    - 主要品牌市场份额（比亚迪、特斯拉、蔚来等）
    - 消费者购买偏好和痛点
    """,
    expected_output="一份包含关键数据和来源的研究摘要",
)

analysis_task = Task(
    description="""
    基于研究数据，分析：
    - 市场增长的核心驱动因素
    - 竞争格局的演变趋势
    - 潜在的市场机会与风险
    """,
    expected_output="结构化分析结论，包含3-5条核心洞察",
    # 可选：指定依赖上游任务输出
    context=[research_task]
)

writing_task = Task(
    description="""
    撰写一份面向投资人的市场分析报告，要求：
    - 执行摘要（1页）
    - 市场现状、竞争分析、趋势预测（3-5页）
    - 投资建议与风险提示
    - 语言专业、数据支撑、逻辑清晰
    """,
    expected_output="完整的Markdown格式报告",
    context=[analysis_task]
)


boss = Agent(
    role="任务分配专家",
    goal="根据任务具体类型分配给合适的智能体",
    backstory="你擅长拆解任务、资源分配和监督任务执行。",
    verbose=True,
    allow_delegation=True,  # Manager必须允许代理任务，
    llm=llm
)


crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.hierarchical,
    manager_agent=boss,
    #manager_llm=llm, # 当前agents中的上一级，可以是agent也可以是一个llm
    planning=True
)

result = crew.kickoff()
print(result)