from langchain.agents import create_agent
from src.langgraph_tutorial.llm_config import model
from langgraph.graph.state import CompiledStateGraph


async def init_supervisor_agent() -> CompiledStateGraph:
    """
    Initialize the supervisor agent with a specific prompt and no tools.
    Returns:
        The supervisor agent instance.
    """
    supervisor_prompt = (
        "You are a supervisor. Route tasks to either the researcher or creator agent or END as appropriate. "
        "Researcher is a person who conducts search and provides information for langgraph."
        "Creator is a person who creates content and designs in Canva."
        "Coordinate their outputs and ensure the workflow is completed."
        "You need to say explicitly who needs to do next."
        "Your answer should be this format: NEXT_AGENT: <agent_name> ANSWER: <response>"
    )
    supervisor_agent = create_agent(
        model,
        tools=[],
        system_prompt=supervisor_prompt,
    )
    return supervisor_agent
