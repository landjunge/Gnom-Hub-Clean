import json; from datetime import datetime; from uuid import UUID; from typing import List, Optional
from gnom_hub.domain.chat.entities import ChatMessage, FlexSoul
from gnom_hub.domain.chat.repository import ChatRepository
from .connection import get_db_connection, Await, parse_dt

def _row_to_msg(r) -> ChatMessage:
    return ChatMessage(id=UUID(r["id"]), agent_id=UUID(r["agent_id"]), role=r["role"], content=r["content"], timestamp=parse_dt(r["timestamp"]), model=r["model"], token_count=r["token_count"])

class SQLiteChatRepository(ChatRepository):
    def get_messages(self, agent_id: UUID, limit: int = 50) -> Await:
        with get_db_connection() as conn: return Await([_row_to_msg(r) for r in conn.execute("SELECT * FROM chat_messages WHERE agent_id = ? ORDER BY timestamp DESC LIMIT ?", (str(agent_id), limit)).fetchall()][::-1])
    def save_message(self, m: ChatMessage) -> Await:
        with get_db_connection() as conn:
            conn.execute("INSERT OR REPLACE INTO chat_messages VALUES (?, ?, ?, ?, ?, ?, ?)", (str(m.id), str(m.agent_id), m.role, m.content, m.model, m.token_count, m.timestamp.isoformat()))
            conn.commit()
        return Await(m)
    def get_flexsoul(self, agent_id: UUID) -> Await:
        with get_db_connection() as conn:
            r = conn.execute("SELECT * FROM flexsoul WHERE agent_id = ?", (str(agent_id),)).fetchone()
            if not r: return Await(None)
            return Await(FlexSoul(UUID(r["agent_id"]), [_row_to_msg(d) for d in json.loads(r["short_term"] or "[]")], r["long_term_summary"], parse_dt(r["last_updated"])) )
    def save_flexsoul(self, fs: FlexSoul) -> Await:
        with get_db_connection() as conn:
            st = json.dumps([{"id": str(m.id), "agent_id": str(m.agent_id), "role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat(), "model": m.model, "token_count": m.token_count} for m in fs.short_term])
            conn.execute("INSERT OR REPLACE INTO flexsoul VALUES (?, ?, ?, ?)", (str(fs.agent_id), st, fs.long_term_summary, fs.last_updated.isoformat()))
            conn.commit()
        return Await(fs)
    def clear_history(self, agent_id: UUID) -> Await:
        with get_db_connection() as conn:
            res = conn.execute("DELETE FROM chat_messages WHERE agent_id = ?", (str(agent_id),)); conn.commit()
            return Await(res.rowcount > 0)
    def get_history(self, project: str = "default", limit: int = 50) -> Await:
        with get_db_connection() as conn: return Await([_row_to_msg(r) for r in conn.execute("SELECT * FROM chat_messages ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()])
    def count_messages(self) -> Await:
        with get_db_connection() as conn: return Await(conn.execute("SELECT COUNT(*) FROM chat_messages").fetchone()[0])
