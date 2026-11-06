import sys
from pathlib import Path

from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import get_llm

from tools.search_news_tools import search_news
from tools.get_statistics_tools import get_statistics



@CrewBase
class NewsCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = get_llm()

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            llm=self.llm,
            verbose=True,
            tools=[search_news, get_statistics],
        )
    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config["writer"],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config["editor"],
            llm=self.llm,
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["writing_task"],
        )

    @task
    def editing_task(self) -> Task:
        return Task(
            config=self.tasks_config["editing_task"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    news_crew = NewsCrew()
    result = news_crew.crew().kickoff(inputs={
        "topic": "人工智能"
    })
    print(result)


