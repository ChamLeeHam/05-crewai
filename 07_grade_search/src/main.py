
from crew import GradeQueryCrew

def run_grade_query():
    try:

        user_query = input("请输入要查询的成绩：")
        crew = GradeQueryCrew()
        crew.crew().kickoff(
            inputs={
                "query": user_query
            }
        )
        print("查询结果已经保存在【output\成绩查询结果.md】")
    except Exception as e:
        print("查询失败，请检查输入是否正确")
if __name__ == "__main__":
    run_grade_query()