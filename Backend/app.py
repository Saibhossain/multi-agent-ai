import os, asyncio, json, shutil
from typing import Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from dotenv import load_dotenv

from db import get_conn, ensure_connection
from mcp_client import MCPClient
from langgraph_workflow import build_workflow

load_dotenv()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Smart Knowledge Hub API")

mcp_client = MCPClient()
graph = None

def db_lookup_faq(question: str) -> Optional[str]:
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT answer FROM faq WHERE question LIKE %s ORDER BY id DESC LIMIT 1",
                (f"%{question[:200]}%",),
            )
            row = cur.fetchone()
        conn.close()
        if row:
            return row["answer"]
    except Exception:
        return None
    return None

def log_message(direction: str, content: str, meta: Dict[str, Any] | None = None):
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO ai_logs (direction, content, meta) VALUES (%s,%s,%s)",
                (direction, content, json.dumps(meta or {})),
            )
        conn.close()
    except Exception:
        pass

def detect_kind(filename: str, content_type: str) -> str:
    name = filename.lower()
    if name.endswith(".csv"):
        return "csv"
    if name.endswith(".pdf"):
        return "pdf"
    return "other"

class ChatIn(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    ok, msg = ensure_connection()
    if not ok:
        print("[WARN] MySQL connection failed on startup:", msg)
    await mcp_client.start()
    global graph
    graph = build_workflow(db_lookup_faq, mcp_client)

@app.on_event("shutdown")
async def shutdown_event():
    await mcp_client.stop()

@app.post("/chat")
async def chat(payload: ChatIn):
    user_msg = payload.message.strip()
    log_message("user", user_msg, {"source":"web"})
    result = graph.invoke({"user_query": user_msg})
    reply = result.get("response","Sorry, something went wrong.")
    log_message("assistant", reply, {"route": result.get("route")})
    return {"ok": True, "reply": reply, "route": result.get("route")}

@app.post("/upload")
async def upload(file: UploadFile = File(...), note: Optional[str] = Form(None)):
    filename = file.filename
    dest_path = os.path.join(UPLOAD_DIR, filename)
    with open(dest_path, "wb") as out:
        shutil.copyfileobj(file.file, out)

    kind = detect_kind(filename, file.content_type or "")
    result = await graph.ainvoke({"user_query": note or "process file", "file_path": dest_path, "file_kind": kind})
    reply = result.get("response","Processed.")
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO uploads (filename, path, mime, kind, summary) VALUES (%s,%s,%s,%s,%s)",
                (filename, dest_path, file.content_type, kind, result.get("extracted",""))
            )
        conn.close()
    except Exception:
        pass
    log_message("user", f"[uploaded {filename}]", {"kind": kind})
    log_message("assistant", reply, {"route": result.get("route")})
    return {"ok": True, "reply": reply, "kind": kind, "extracted": result.get("extracted")}

