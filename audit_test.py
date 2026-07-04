#!/usr/bin/env python3
"""
Audit test: sends 15 queries to the running rag_chatbot via WebSocket /ws
and records timing + response for each.
"""
import asyncio
import json
import time
import sys

try:
    import websockets
except ImportError:
    print("ERROR: websockets not installed. Run: pip3 install websockets --break-system-packages")
    sys.exit(1)

QUERIES = [
    # Typo / spell correction
    (1,  "attendanse chekc",                   "spell-correction"),
    (2,  "silabus for cse",                    "spell-correction"),
    (3,  "circuler about admision",             "spell-correction"),
    # Casual phrasing / query rewriting
    (4,  "mam time table",                     "query-rewriting"),
    (5,  "sir free hrs",                        "query-rewriting"),
    # Faculty rule-based handler
    (6,  "who is Narayana Rao Appini",         "faculty-rule"),
    (7,  "timetable of Narayana Rao Appini",   "faculty-rule"),
    # Bus fee rule-based handler
    (8,  "bus fee for Kovur",                   "bus-fee-rule"),
    # Dept info rule-based handler
    (9,  "what is the vision of the department","dept-info-rule"),
    (10, "who is the hod",                      "dept-info-rule"),
    # Hybrid search fallback (unknown module fix)
    (11, "wifi facilities on campus",           "hybrid-search-fallback"),
    (12, "do you have a gym",                   "hybrid-search-fallback"),
    (13, "is there an atm on campus",           "hybrid-search-fallback"),
    # Safety checks — must be rejected / handled gracefully
    (14, "kdjhfkjshdkfjh random gibberish query", "safety-reject"),
    (15, "tell me a joke about aliens",          "safety-reject"),
]

async def send_query(uri: str, message: str) -> tuple[str, float]:
    """Connect, send one message, receive one reply, return (reply, elapsed_s)."""
    t0 = time.perf_counter()
    async with websockets.connect(uri, open_timeout=10, close_timeout=5) as ws:
        await ws.send(json.dumps({"message": message}))
        raw_response = await ws.recv()
        data = json.loads(raw_response)
        response_text = data.get("message", "")
    elapsed = time.perf_counter() - t0
    return response_text, elapsed



async def main():
    uri = "ws://localhost:8000/ws"
    print(f"\n{'='*80}")
    print(f"NBKR RAG Chatbot — Audit Test  ({len(QUERIES)} queries)")
    print(f"WebSocket endpoint: {uri}")
    print(f"{'='*80}\n")

    results = []
    total_start = time.perf_counter()

    for num, query, module in QUERIES:
        print(f"[{num:02d}] Query : {query!r}  (expected module: {module})")
        try:
            response, elapsed = await send_query(uri, query)
            snippet = response[:200].replace("\n", " ")
            print(f"      Time  : {elapsed:.2f}s")
            print(f"      Reply : {snippet}")
            results.append((num, query, module, elapsed, response, None))
        except Exception as e:
            print(f"      ERROR : {e}")
            results.append((num, query, module, 0.0, "", str(e)))
        print()

    total_elapsed = time.perf_counter() - total_start
    print(f"\n{'='*80}")
    print(f"All queries done.  Total wall-clock: {total_elapsed:.1f}s")
    print(f"{'='*80}\n")

    # Write JSON results for artifact
    with open("/tmp/audit_results.json", "w") as f:
        json.dump([
            {
                "num": r[0],
                "query": r[1],
                "module": r[2],
                "elapsed_s": round(r[3], 2),
                "response": r[4],
                "error": r[5],
            }
            for r in results
        ], f, indent=2)
    print("Results written to /tmp/audit_results.json")

if __name__ == "__main__":
    asyncio.run(main())
