from crewai import Crew, Process, Agent, Task
from crewai.project import crew, CrewBase, agent, task
from pathlib import Path
import sys

PROJECT_ROOT=Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT/"07_grade_search"/"src"))

from config import get_llm
from tools.ddgs_tools import ddgs_text_search
from tools.search_pdf_tools import PDFSearchTool

pdf_search_tool = PDFSearchTool(file_path=str(PROJECT_ROOT/"07_grade_search"/"files"/"成绩单.pdf"))
@CrewBase
class GradeQueryCrew:
    agents_config = "configs/agents.yaml" # 定义智能体配置文件的所在位置
    tasks_config = "configs/tasks.yaml"# 定义任务配置文件的所在位置
    llm = get_llm() # 定义全局 llm

    @agent
    def retriever_agent(self)->Agent:
        return Agent(
            config=self.agents_config["retriever_agent"],
            llm=self.llm,
            verbose=True,
            tools=[pdf_search_tool, ddgs_text_search ]
        )

    @agent
    def response_synthesizer_agent(self)->Agent:
        return Agent(
            config=self.agents_config["response_synthesizer_agent"],
            llm=self.llm,
            verbose=True,
        )

    @task
    def retrieval_task(self) -> Task:
        return Task(
            config=self.tasks_config["retrieval_task"],
        )

    @task
    def response_task(self) -> Task:
        return Task(
            config=self.tasks_config["response_task"],
            context=[self.retrieval_task()] #依赖检索喉的结果，然后再响应
        )

    @crew
    def crew(self)->Crew:
        crew = Crew(
            agents=self.agents, # 自动获取当前类中带有@agent装饰器的所有方法返回的结果
            tasks=self.tasks, # 自动获取当前类中带有@task装饰器的所有方法返回的结果
            process=Process.sequential,
            verbose=True
        )
        return crew