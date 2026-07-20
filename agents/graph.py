from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.router import RouterAgent


class AgentState(TypedDict):
    query: str
    response: str


router = RouterAgent()


def router_node(state: AgentState):

    query = state["query"]

    answer = router.route(query)

    return {
        "response": answer
    }


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node(
        "agent",
        router_node
    )

    graph.set_entry_point("agent")

    graph.add_edge(
        "agent",
        END
    )

    return graph.compile()