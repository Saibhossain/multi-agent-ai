import sys
from workflow_graph import graph

def run_ai_flow(user_query, file_path=None):
    initial_state = {
        "user_query": user_query,
        "file_path": file_path,
        "intent": None,
        "ai_response": None
    }
    final_state = graph.invoke(initial_state)
    return final_state["ai_response"]

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        query = sys.argv[1]
        file_path = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "None" else None
        print(run_ai_flow(query, file_path))
    else:
        # Fallback test runs
        print(run_ai_flow("What is your return policy?"))
        print(run_ai_flow("Please extract this document.", file_path="../sample.pdf"))

