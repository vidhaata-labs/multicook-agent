from tavily import TavilyClient
from langchain.tools import tool
from typing import Dict, Any

from multicook_agent.logging_config import get_logger

logger = get_logger(__name__)
tavily_client = TavilyClient()
logger.info("TavilyClient initialized")


@tool
def web_search(query: str) -> Dict[str, Any]:
    """Tool to search the web for information"""
    logger.info("Tool call - Searching info on the web(Tavily) - query=%s", query)
    return tavily_client.search(query)