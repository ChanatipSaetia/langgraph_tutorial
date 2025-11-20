from langchain_core.messages import AIMessage
from src.langgraph_tutorial.state.agent_state import AgentState
from typing import Callable

async def generic_node(state: AgentState, init_agent: Callable, agent_name: str) -> AgentState:
    """
    Generic node wrapper for any agent. Invokes the agent and formats the output message.
    Args:
        state (AgentState): The current state containing messages.
        init_agent (Callable): The agent initializer function.
        agent_name (str): The name to prefix the agent's response.
    Returns:
        AgentState: Updated state with the agent's response message.
    """
    agent = await init_agent()
    output = await agent.ainvoke({"messages": state["messages"]})
    current_length = len(state['messages'])
    left_message = output['messages'][current_length:-1]
    final_message = output['messages'][-1].content.strip()
    prefix = f"{agent_name}:"
    if final_message.startswith(prefix):
        return {"messages": left_message + [AIMessage(content=final_message)]}
    return {"messages": left_message + [AIMessage(content=f"{prefix} " + final_message)]}
