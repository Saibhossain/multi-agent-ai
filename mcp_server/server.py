import os
from typing import List
import pandas as pd
from pypdf import PdfReader
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("file_tools")

def safe_path(path: str) -> str:
    return os.path.abspath(path)

@mcp.tool()
def parse_csv(path: str, sample_rows: int = 5) -> dict:
    """Parse a CSV and return summary (columns, row count, head)."""
    full = safe_path(path)
    if not os.path.exists(full):
        return {"error": f"File not found: {full}"}
    df = pd.read_csv(full)
    return {
        "columns": list(df.columns),
        "rows": int(df.shape[0]),
        "preview": df.head(sample_rows).to_dict(orient="records")
    }

@mcp.tool()
def extract_pdf_text(path: str, max_pages: int = 3) -> str:
    """Extract text content from the first N pages of a PDF."""
    full = safe_path(path)
    if not os.path.exists(full):
        return f"File not found: {full}"
    reader = PdfReader(full)
    pages = min(len(reader.pages), max_pages)
    chunks: List[str] = []
    for i in range(pages):
        page = reader.pages[i]
        chunks.append(page.extract_text() or "")
    return "\n\n".join(chunks)

if __name__ == "__main__":
    mcp.run(transport="stdio")
