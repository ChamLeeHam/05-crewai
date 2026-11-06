from crewai import Crew, Process, Agent, Task
from crewai.project import crew, CrewBase, agent, task
from pathlib import Path
import sys
PROJECT_ROOT=Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import get_llm


@CrewBase
class MyCrew:
    agents_config = "configs/agents.yaml" # 定义智能体配置文件的所在位置
    tasks_config = "configs/tasks.yaml"# 定义任务配置文件的所在位置
    llm = get_llm() # 定义全局 llm

    @agent
    def researcher(self)->Agent:
        return Agent(
            config=self.agents_config["researcher"],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def writer(self)->Agent:
        return Agent(
            config=self.agents_config["writer"],
            llm=self.llm,
            verbose=True,
        )

    @task
    def researcher_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def writer_task(self) -> Task:
        return Task(
            config=self.tasks_config["writing_task"],
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


if __name__ == '__main__':
    my_crew = MyCrew()
    result = my_crew.crew().kickoff(inputs={"topic": "什么是量子计算"})
    print(result)