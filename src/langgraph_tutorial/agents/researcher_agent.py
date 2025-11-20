from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from ..llm_config import model
from langgraph.graph.state import CompiledStateGraph


async def init_researcher_agent() -> CompiledStateGraph:
    """
    Initialize and compile a StateGraph for the researcher agent.
    Returns:
        CompiledStateGraph: The compiled state graph for the researcher agent.
    """

    # researcher_tools = []

    # With tools
    researcher_client = MultiServerMCPClient(
        {
            "langgraph": {
                "url": "https://docs.langchain.com/mcp",
                "transport": "streamable_http",
            }
        }
    )
    researcher_tools = await researcher_client.get_tools()

    researcher_prompt = "You are a Researcher. Find and summarize information as requested. Always use search first"
    researcher_agent = create_agent(
        model,
        tools=researcher_tools,
        system_prompt=researcher_prompt,
    )
    return researcher_agent
