"""Admin Service — full admin dashboard with CRUD for timetable, faculty, circulars, FAQ."""

import json
import os
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

# ── Config ────────────────────────────────────────────────────────────────────
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "nbkr2026")
PORT = int(os.getenv("ADMIN_PORT", "8005"))

# Data file paths — resolved relative to the working directory so they work
# both locally (project root) and inside Docker (mounted at /app).
DATA_DIR = os.getenv("DATA_DIR", ".")

def _path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="NBKR Admin Service",
    description="Administrative dashboard for managing chatbot knowledge data",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _check_admin(request: Request) -> bool:
    """Validate admin password from X-Admin-Password header."""
    pwd = request.headers.get("X-Admin-Password", "")
    return pwd == ADMIN_PASSWORD


def _audit_log(action: str) -> None:
    """Append an entry to the admin audit log (keeps last 200)."""
    audit_file = _path("admin_audit.json")
    entries: list = []
    if os.path.exists(audit_file):
        try:
            with open(audit_file, "r", encoding="utf-8") as f:
                entries = json.load(f)
        except Exception:
            entries = []

    entries.append({
        "ts": datetime.now().isoformat(),
        "user": "admin",
        "action": action,
    })
    entries = entries[-200:]

    with open(audit_file, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def _load_json(filename: str, default):
    """Load a JSON file, returning default if missing or corrupt."""
    path = _path(filename)
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _save_json(filename: str, data) -> None:
    """Write data to a JSON file."""
    path = _path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "admin_service", "version": "1.0.0"}


@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    """Serve the admin dashboard HTML."""
    # Look for the HTML file next to this file, or in DATA_DIR, or in /app
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "admin_dashboard.html"),
        os.path.join(DATA_DIR, "admin_dashboard.html"),
        "/app/admin_dashboard.html",
        "admin_dashboard.html",
    ]
    for html_path in candidates:
        html_path = os.path.normpath(html_path)
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())

    return HTMLResponse(
        content="<h1>Admin dashboard file not found</h1><p>admin_dashboard.html is missing.</p>",
        status_code=404,
    )


@app.get("/admin/data")
async def admin_data(request: Request):
    """Return all editable data for the admin dashboard."""
    if not _check_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    # Timetable
    tt_data = _load_json("aids_timetable_data.json", {"timetable": {}, "subjects": {}, "faculty": {}})

    # Faculty
    fac_data = _load_json("aids_faculty_data.json", [])

    # Circulars
    circ_data = _load_json("nbkr_circulars.json", [])

    # Knowledge base — stored as list, exposed as dict {title: text}
    raw_kb = _load_json("knowledge_updates.json", {})
    if isinstance(raw_kb, dict):
        kb_data = raw_kb
    elif isinstance(raw_kb, list):
        kb_data = {
            item.get("title", f"item_{i}"): item.get("text", "")
            for i, item in enumerate(raw_kb)
        }
    else:
        kb_data = {}

    _audit_log("LOGIN")

    return JSONResponse({
        "timetable_data": tt_data,
        "faculty_data": fac_data,
        "circular_data": circ_data,
        "knowledge_data": kb_data,
    })


@app.post("/admin/save-timetable")
async def save_timetable(request: Request):
    """Save timetable data."""
    if not _check_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    data = await request.json()
    _save_json("aids_timetable_data.json", data)
    _audit_log("SAVE_TIMETABLE")
    return JSONResponse({"status": "ok", "message": "Timetable saved successfully"})


@app.post("/admin/save-circular")
async def save_circular(request: Request):
    """Save circulars data."""
    if not _check_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    data = await request.json()
    _save_json("nbkr_circulars.json", data)
    _audit_log("SAVE_CIRCULARS")
    return JSONResponse({"status": "ok", "message": "Circulars saved successfully"})


@app.post("/admin/save-faculty")
async def save_faculty(request: Request):
    """Save faculty data."""
    if not _check_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    data = await request.json()
    _save_json("aids_faculty_data.json", data)
    _audit_log("SAVE_FACULTY")
    return JSONResponse({"status": "ok", "message": "Faculty data saved successfully"})


@app.post("/admin/save-knowledge")
async def save_knowledge(request: Request):
    """Save knowledge base / FAQ data."""
    if not _check_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    data = await request.json()

    # Convert dict → list format for storage
    if isinstance(data, dict):
        kb_list = [
            {
                "title": key,
                "text": val,
                "category": "general",
                "added_by": "admin",
                "added_at": datetime.now().isoformat(),
            }
            for key, val in data.items()
        ]
        _save_json("knowledge_updates.json", kb_list)
    else:
        _save_json("knowledge_updates.json", data)

    _audit_log("SAVE_KNOWLEDGE")
    return JSONResponse({"status": "ok", "message": "Knowledge base saved successfully"})


@app.get("/admin/audit")
async def get_audit_log(request: Request):
    """Return the admin audit log."""
    if not _check_admin(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    entries = _load_json("admin_audit.json", [])
    return JSONResponse({"entries": entries})


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n🚀 Starting NBKR Admin Service on port {PORT}")
    print(f"📍 http://localhost:{PORT}/admin\n")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
