from agents import decision_router
from db import log_ai_response

def run_ai_flow(user_query, file_path=None):
    ai_response = decision_router(user_query, file_path)
    log_ai_response(user_query, ai_response)
    return ai_response

if __name__ == "__main__":

    user_input = "What is your return policy?"
    print(run_ai_flow(user_input))
