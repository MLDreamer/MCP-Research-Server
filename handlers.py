import httpx
import sqlite3
import os
from pathlib import Path

WORKSPACE = Path(os.environ.get("WORKSPACE", str(Path.home() / "research-workspace")))
DB_PATH = WORKSPACE / "notes.db"

async def handle_web_search(args: dict) -> str:
    query = args.get("query")
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get("https://api.duckduckgo.com/", params={"q": query, "format": "json"})
        data = resp.json()
        results = [data['AbstractText']] if data.get('AbstractText') else []
        results.extend([t.get('Text', '') for t in data.get('RelatedTopics', [])[:3]])
        return "\n".join(results) or "No specific results found."

async def handle_read_note(args: dict) -> str:
    filename = args.get("filename", "")
    if not filename.endswith(".md"): filename += ".md"
    filepath = WORKSPACE / filename
    if not filepath.exists(): return f"File {filename} not found."
    return filepath.read_text(encoding="utf-8")[:10000]

async def handle_search_notes(args: dict) -> str:
    query = args.get("query")
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.execute("SELECT title, content FROM notes_fts WHERE notes_fts MATCH ? LIMIT 5", (query,))
        rows = cursor.fetchall()
        return "\n---\n".join([f"Title: {r[0]}\n{r[1][:200]}..." for r in rows]) or "No matches."
    finally:
        conn.close()
