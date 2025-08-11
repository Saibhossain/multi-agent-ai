from db import fetch_faq_answer, log_ai_response
from mcp_client import parse_pdf

def faq_agent(user_query):
    answer = fetch_faq_answer(user_query)
    return answer if answer else "I couldn't find an exact answer."

def document_agent(file_path):
    content = parse_pdf(file_path)
    return f"Extracted content: {content[:200]}..."  # sample preview

def decision_router(user_query, file_path=None):
    if file_path:
        return document_agent(file_path)
    else:
        return faq_agent(user_query)
