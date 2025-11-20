from functools import partial
from langgraph.graph import StateGraph, START, END
from src.langgraph_tutorial.agents.node_wrappers import generic_node
from src.langgraph_tutorial.agents.researcher_agent import init_researcher_agent
from src.langgraph_tutorial.agents.creator_agent import init_creator_agent
from src.langgraph_tutorial.agents.supervisor_agent import init_supervisor_agent
from src.langgraph_tutorial.state.agent_state import AgentState
from typing import Dict, Any

# Node wrappers for agents are imported from agent files
researcher_node = partial(generic_node, init_agent=init_researcher_agent, agent_name="Researcher")
creator_node = partial(generic_node, init_agent=init_creator_agent, agent_name="Creator")
supervisor_node = partial(generic_node, init_agent=init_supervisor_agent, agent_name="Supervisor")

async def supervisor_routing(state: AgentState) -> Any:
    """
    Conditional routing function for supervisor node.
    Returns the next node name(s) based on user input.
    Args:
        state (AgentState): The current state containing messages.
    Returns:
        str or list: The next node name(s) or END.
    """
    user_content = state["messages"][-1].content if state["messages"] else ""
    user_content = user_content.split("ANSWER:")[0]
    if "researcher" in user_content.lower():
        return "researcher"
    elif "creator" in user_content.lower():
        return "creator"
    else:
        return END

# Build the StateGraph
workflow_builder = StateGraph(AgentState)
workflow_builder.add_node("supervisor", supervisor_node)
workflow_builder.add_node("researcher", researcher_node)
workflow_builder.add_node("creator", creator_node)
workflow_builder.add_edge(START, "supervisor")
workflow_builder.add_conditional_edges("supervisor", supervisor_routing, ["researcher", "creator", END])
workflow_builder.add_edge("researcher", "supervisor")
workflow_builder.add_edge("creator", "supervisor")
workflow = workflow_builder.compile()