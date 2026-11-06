from crewai.tools import tool
@tool
def get_statistics(topic: str) -> str:
    """获取指定主题的相关统计数据
    Args:
    topic: 要查询的主题
    Returns:
    相关的统计数据
    """
    print(f"[工具调用] 正在获取统计数据：{topic}")
    # 模拟统计数据
    statistics = {
        "人工智能": """
        AI行业统计数据：
        - 全球AI市场规模：预计2025年达到1900亿美元
        - 中国AI市场增速：年均增长率超过30%
        - AI人才缺口：全球约100万，中国约30万
        - 企业AI采用率：超过60%的大型企业已部署AI应用
        """,
        "CrewAI": """
        CrewAI框架统计数据：
        - GitHub Stars：超过43,000
        - 月度下载量：超过50万次
        - 贡献者数量：超过200人
        - 企业用户：数千家企业在生产环境使用
        """,
        "默认": """
        通用科技统计数据：
        - 全球科技支出：预计2025年超过5万亿美元
        - 数字化转型投资：年均增长15%
        - 远程办公普及率：超过40%的知识工作者
        """
    }
    for key in statistics:
        if key in topic:
            return statistics[key]
    return statistics["默认"]