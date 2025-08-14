from langgraph.graph import StateGraph
from typing import TypedDict, Optional
from db import fetch_faq_answer,log_ai_response
from mcp_client import parse_pdf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import BytesIO

class GraphState(TypedDict):
    user_query: str
    file_path: Optional[str]
    intent: Optional[str]
    ai_response: Optional[str]

# --- Node: Intent Classifier ---
def classify_intent(state: GraphState):
    query = state["user_query"].lower()
    if state["file_path"]:
        intent = "document"
    elif any(keyword in query for keyword in ["order", "return", "price", "policy"]):
        intent = "faq"
    else:
        intent = "unknown"
    return {**state, "intent": intent}

# --- Node: FAQ Agent ---
def faq_agent_node(state: GraphState):
    answer = fetch_faq_answer(state["user_query"])
    if not answer:
        answer = "I couldn't find an exact answer."
    return {**state, "ai_response": answer}

# --- Node: Document Agent ---
def document_agent_node(state: GraphState):
    content = parse_pdf(state["file_path"])
    preview = content[:300] + "..." if len(content) > 300 else content
    return {**state, "ai_response": f"Extracted content preview:\n{preview}"}

# --- Node: Fallback for Unknown ---
def unknown_agent_node(state: GraphState):
    return {**state, "ai_response": "I'm not sure how to handle this request yet."}

# --- Node: Final Response Logger ---
def log_and_return(state: GraphState):
    log_ai_response(state["user_query"], state["ai_response"])
    return state

# --- Build Graph ---
workflow = StateGraph(GraphState)

workflow.add_node("classify_intent", classify_intent)
workflow.add_node("faq_agent", faq_agent_node)
workflow.add_node("document_agent", document_agent_node)
workflow.add_node("unknown_agent", unknown_agent_node)
workflow.add_node("log_and_return", log_and_return)

# Entry point
workflow.set_entry_point("classify_intent")

# Edges
def route_intent(state: GraphState):
    if state["intent"] == "faq":
        return "faq_agent"
    elif state["intent"] == "document":
        return "document_agent"
    else:
        return "unknown_agent"

workflow.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "faq_agent": "faq_agent",
        "document_agent": "document_agent",
        "unknown_agent": "unknown_agent"
    }
)

# All agents → final log node
workflow.add_edge("faq_agent", "log_and_return")
workflow.add_edge("document_agent", "log_and_return")
workflow.add_edge("unknown_agent", "log_and_return")

# Compile
graph = workflow.compile()

graph_image = graph.get_graph().draw_mermaid_png()
img = mpimg.imread(BytesIO(graph_image))
plt.imshow(img)
plt.axis('off')
plt.show()