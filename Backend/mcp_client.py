import requests

MCP_SERVER = "http://127.0.0.1:5001/"

def parse_pdf(file_path):
    r = requests.post(f"{MCP_SERVER}/parse_pdf", json={"file_path": file_path})
    return r.json().get("content", "")

def parse_csv(file_path):
    r = requests.post(f"{MCP_SERVER}/parse_csv", json={"file_path": file_path})
    return r.json().get("content", {})
