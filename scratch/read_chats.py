import sqlite3
from pathlib import Path

db_path = Path.home() / ".gnom-hub" / "data" / "gnomhub.db"
print("Reading DB from:", db_path)
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT sender, msg_type, content, timestamp FROM chat ORDER BY timestamp DESC LIMIT 50").fetchall()
    for r in reversed(rows):
        print(f"[{r['timestamp']}] {r['sender']} ({r['msg_type']}): {r['content']}")
    conn.close()
else:
    print("No database found.")
