import sqlite3
from pathlib import Path
import json

db_path = Path.home() / ".gnom-hub" / "data" / "gnomhub.db"
print("Reading DB from:", db_path)
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    
    print("\n--- Recent blocked events in Chat ---")
    rows = conn.execute("SELECT sender, msg_type, content, timestamp FROM chat WHERE content LIKE '%block%' OR content LIKE '%verweigert%' OR content LIKE '%BLOCKADE%' ORDER BY timestamp DESC LIMIT 20").fetchall()
    for r in rows:
        print(f"[{r['timestamp']}] {r['sender']} ({r['msg_type']}): {r['content'][:400]}")
        
    print("\n--- Recent Audit Logs ---")
    audit_rows = conn.execute("SELECT timestamp, agent, event_type, details FROM audit_log ORDER BY timestamp DESC LIMIT 30").fetchall()
    for r in audit_rows:
        print(f"[{r['timestamp']}] {r['agent']} - {r['event_type']}: {r['details']}")
        
    conn.close()
else:
    print("No database found.")
