from langgraph.graph import StateGraph, END

from app.agents.state import AgentState

from app.agents.supervisor import (
    supervisor_node,
    route_intent,
)

from app.agents.search_agent import search_agent_node

from app.agents.youtube_agent import (
    youtube_find_node,
    youtube_summarize_node,
)

from app.agents.curriculum_agent import curriculum_agent_node

from app.agents.memory_agent import memory_agent_node

from app.agents.synthesizer import synthesizer_node


def build_call_graph():

    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)

    graph.add_node("search", search_agent_node)

    graph.add_node("youtube_find", youtube_find_node)

    graph.add_node("youtube_summarize", youtube_summarize_node)

    graph.add_node("curriculum", curriculum_agent_node)

    graph.add_node("memory", memory_agent_node)

    graph.add_node("synthesizer", synthesizer_node)

    graph.set_entry_point("supervisor")

    graph.add_conditional_edges(
        "supervisor",
        route_intent,
        {
            "concept_search": "search",
            "youtube_find": "youtube_find",
            "youtube_summary": "youtube_summarize",
            "exam_question": "curriculum",
            "memory_query": "memory",
            "general_tutor": "synthesizer",
            "unknown": "synthesizer",
        },
    )

    graph.add_edge("search", "synthesizer")

    graph.add_edge("youtube_find", "synthesizer")

    graph.add_edge("youtube_summarize", "synthesizer")

    graph.add_edge("curriculum", "synthesizer")

    graph.add_edge("memory", "synthesizer")

    graph.add_edge("synthesizer", END)

    return graph.compile()


CALL_GRAPH = build_call_graph()