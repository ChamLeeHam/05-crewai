import time

from crewai.tools import tool
from ddgs import DDGS


@tool("ddgs_text_search")
def ddgs_text_search(query:str):
    """根据stock_code股票代码获取最近的股票信息"""
    try:
        with DDGS() as ddgs:
            results =  ddgs.text(
                query=query,
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