from io import BytesIO
from typing import TypedDict, Optional, Literal, Dict, Any
from langgraph.graph import StateGraph, START, END
from matplotlib import image as mpimg, pyplot as plt


class GraphState(TypedDict, total=False):
    user_query: str
    file_path: Optional[str]
    file_kind: Optional[Literal["csv","pdf","other"]]
    db_result: Optional[str]
    extracted: Optional[str]
    response: Optional[str]
    route: Optional[str]

def classify_intent(state: GraphState) -> Dict[str, Any]:
    q = (state.get("user_query") or "").lower()
    if state.get("file_path"):
        return {"route": "file"}
    if any(k in q for k in ["order", "hours", "track", "status", "faq", "price"]):
        return {"route": "faq"}
    return {"route": "fallback"}

def faq_lookup(state: GraphState, db_lookup_fn) -> Dict[str, Any]:
    question = state.get("user_query","")
    answer = db_lookup_fn(question)
    if answer:
        return {"db_result": answer}
    return {"db_result": "Sorry, I couldn't find an exact answer. A support ticket may be needed."}

async def process_file(state: GraphState, mcp_client) -> Dict[str, Any]:
    path = state.get("file_path")
    kind = state.get("file_kind","other")
    if not path:
        return {}
    if kind == "csv":
        data = await mcp_client.call("parse_csv", {"path": path})
        text = f"CSV parsed. Columns: {', '.join(data.get('columns', []))}. Rows: {data.get('rows', 'unknown')}."
        return {"extracted": text}
    elif kind == "pdf":
        text = await mcp_client.call("extract_pdf_text", {"path": path, "max_pages": 3})
        return {"extracted": (text or "")[:1200]}
    return {"extracted": "Unsupported file type."}

def craft_response(state: GraphState) -> Dict[str, Any]:
    if state.get("file_path"):
        return {"response": f"File processed ({state.get('file_kind')}): {state.get('extracted')}"}
    if state.get("db_result"):
        return {"response": state["db_result"]}
    return {"response": "How can I help you today? You can ask about business hours or upload a CSV/PDF to parse."}

def build_workflow(db_lookup_fn, mcp_client):
    graph = StateGraph(GraphState)

    def node_route(state: GraphState):
        return classify_intent(state)

    def node_faq(state: GraphState):
        return faq_lookup(state, db_lookup_fn)

    async def node_file(state: GraphState):
        return await process_file(state, mcp_client)

    def node_finalize(state: GraphState):
        return craft_response(state)

    graph.add_node("router", node_route)
    graph.add_node("faq", node_faq)
    graph.add_node("file", node_file)
    graph.add_node("finalize", node_finalize)

    graph.add_edge(START, "router")

    def route_switch(state: GraphState):
        return state.get("route","fallback")

    graph.add_conditional_edges("router", route_switch, {
        "file": "file",
        "faq": "faq",
        "fallback": "finalize"
    })
    graph.add_edge("faq", "finalize")
    graph.add_edge("file", "finalize")
    graph.add_edge("finalize", END)
    graphs = graph.compile()

    graph_image = graphs.get_graph().draw_mermaid_png()
    img = mpimg.imread(BytesIO(graph_image))
    plt.imshow(img)
    plt.axis('off')
    plt.show()

    return graphs



