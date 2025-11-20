from typing import TypedDict, List
from langgraph.graph import add_messages
from typing_extensions import Annotated
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    State schema for agent workflow, containing a list of messages.
    """

    messages: Annotated[List[BaseMessage], add_messages]
