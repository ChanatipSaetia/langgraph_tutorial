from typing import TypedDict, List
from langgraph.graph import add_messages
from typing_extensions import Annotated

class AgentState(TypedDict):
    """
    State schema for agent workflow, containing a list of messages.
    """
    messages: Annotated[List, add_messages]
