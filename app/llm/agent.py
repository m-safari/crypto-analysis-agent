from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from app.llm.prompts import CRYPTO_ANALYST_SYSTEM_PROMPT

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def create_agent(llm, tools):

    llm_with_tools = llm.bind_tools(tools)

    # LLM node
    def call_model(state: AgentState):
        messages = [
            SystemMessage(content=CRYPTO_ANALYST_SYSTEM_PROMPT),
            *state["messages"],
        ]

        response = llm_with_tools.invoke(messages)

        return {"messages": [response]}

    # Build graph
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("agent", call_model)
    graph_builder.add_node("tools", ToolNode(tools))

    graph_builder.add_edge(START, "agent")

    graph_builder.add_conditional_edges(
        "agent",
        tools_condition,
    )

    graph_builder.add_edge("tools", "agent")

    # Persist conversation state in memory
    memory = MemorySaver()

    return graph_builder.compile(checkpointer=memory)
