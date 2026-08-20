"""Submit your team's model result to the board.
Run this inside your container while server.py is running.
Standard library only.
"""
import json, urllib.request, urllib.error

BOARD = "https://aidc.nadir.sh/model"
TEAM  = "1"
BY    = "Khuzama"
IMAGE = "ghcr.io/sckhuzama/aidc-1-warmup:latest"

def request(url, body=None):
    data = json.dumps(body).encode() if body else None
    headers = {"User-Agent": "aidc-student/1.0"}
    if body:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

# 1. read /generate off your own server
status, result = request("http://localhost:8000/generate")
print("my server said", status, result)
if status != 200:
    raise SystemExit("your server is not running, or /generate is broken")

# 2. submit to the board
status, reply = request(BOARD, {
    "team": TEAM,
    "by": BY,
    "model": result["model"],
    "image": IMAGE,
    "tokens_per_sec": result["tokens_per_sec"],
    "sample": result["sample"],
})
print("the board said", status)
print(json.dumps(reply, indent=2))
