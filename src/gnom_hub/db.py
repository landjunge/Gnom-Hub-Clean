import sqlite3
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from contextlib import contextmanager
from .config import DATA_DIR
from .log import get_logger

# =====================================================================
# CONFIGURATION & CONSTANTS
# =====================================================================

DB_PATH = DATA_DIR / "gnomhub.db"
logger = get_logger("db")


# =====================================================================
# CONNECTION MANAGER
# =====================================================================

@contextmanager
def get_db_conn():
    """Öffnet eine rohe Verbindung zu SQLite und konfiguriert grundlegende Pragmas."""
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
    finally:
        conn.close()


# =====================================================================
# INITIALIZATION & SEEDING
# =====================================================================

def _seed_agents(conn):
    """Initialisiert die 8 Standard-Agenten direkt in der übergebenen Verbindung."""
    default_agents = [
        {"name": "SoulAG", "description": "Swarm consciousness", "status": "online", "capabilities": ["@soul"], "role": "soul"},
        {"name": "GeneralAG", "description": "Task coordinator", "status": "online", "capabilities": ["@job"], "role": "general"},
        {"name": "SecurityAG", "description": "Cryptographic protection", "status": "online", "capabilities": [], "role": "security"},
        {"name": "WatchdogAG", "description": "Workspace integrity check", "status": "online", "capabilities": [], "role": "watchdog"},
        {"name": "CoderAG", "description": "Code implementation", "status": "online", "capabilities": ["@code"], "role": "normal"},
        {"name": "WriterAG", "description": "Documentation editor", "status": "online", "capabilities": ["@write"], "role": "normal"},
        {"name": "ResearcherAG", "description": "Web research & crawling", "status": "online", "capabilities": ["@research"], "role": "normal"},
        {"name": "EditorAG", "description": "Quality control & text polish", "status": "online", "capabilities": ["@edit"], "role": "normal"}
    ]
    try:
        for a in default_agents:
            conn.execute("""
                INSERT OR REPLACE INTO agents (name, id, port, description, status, capabilities, role, active_job, last_seen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (a["name"], str(uuid.uuid4()), 0, a["description"], a["status"], 
                  json.dumps(a["capabilities"]), a["role"], None, datetime.now(timezone.utc).isoformat()))
        logger.info("[DB] Default agents successfully seeded.")
    except sqlite3.Error as e:
        logger.error(f"[DB] Error seeding agents: {e}")

def init_db():
    """Erstellt alle benötigten Tabellen idempotent und führt Seeding bei Bedarf aus."""
    try:
        with get_db_conn() as conn:
            with conn:
                conn.executescript("""
                    CREATE TABLE IF NOT EXISTS state (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS agents (
                        name TEXT PRIMARY KEY,
                        id TEXT NOT NULL UNIQUE,
                        port INTEGER DEFAULT 0,
                        description TEXT,
                        status TEXT NOT NULL DEFAULT 'offline',
                        capabilities TEXT DEFAULT '[]',
                        role TEXT DEFAULT 'normal',
                        active_job TEXT DEFAULT NULL,
                        last_seen TEXT NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS chat (
                        id TEXT PRIMARY KEY,
                        project TEXT NOT NULL DEFAULT 'default',
                        sender TEXT NOT NULL,
                        agent_id TEXT NOT NULL,
                        msg_type TEXT NOT NULL DEFAULT 'chat',
                        content TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        metadata TEXT DEFAULT '{}'
                    );
                """)
                conn.execute("INSERT OR IGNORE INTO state (key, value) VALUES ('active_project', '\"default\"')")
                conn.execute("INSERT OR IGNORE INTO state (key, value) VALUES ('language', '\"en\"')")
                
                # Wenn agents Tabelle leer ist, führe Seeding aus
                if not conn.execute("SELECT 1 FROM agents").fetchone():
                    _seed_agents(conn)
        logger.info("[DB] Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"[DB] Database initialization failed: {e}")


# =====================================================================
# MODERNE RELATIONALE API
# =====================================================================

def _row_to_msg(row):
    """Konvertiert eine Zeile der chat-Tabelle in ein Message-Dictionary."""
    d = dict(row)
    try:
        d["metadata"] = json.loads(d["metadata"])
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f"[DB] Failed to parse metadata JSON for message {d.get('id')}: {e}")
        d["metadata"] = {}
    return d

def add_chat_message(project: str, sender: str, agent_id: str, msg_type: str, content: str, metadata: dict = None):
    """Fügt eine Nachricht direkt und relational in die chat-Tabelle ein (transaktionssicher)."""
    try:
        with get_db_conn() as conn:
            with conn:
                msg_id = str(uuid.uuid4())
                conn.execute("""
                    INSERT INTO chat (id, project, sender, agent_id, msg_type, content, timestamp, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (msg_id, project, sender, agent_id, msg_type, content,
                      datetime.now(timezone.utc).isoformat() + "Z",
                      json.dumps(metadata or {})))
                return msg_id
    except sqlite3.Error as e:
        logger.error(f"[DB] Failed to add chat message: {e}")
        return None

def get_chat_history(project: str = "default", limit: int = 30):
    """Lädt die letzten X Nachrichten eines Projekts aus der chat-Tabelle."""
    try:
        with get_db_conn() as conn:
            rows = conn.execute("""
                SELECT * FROM chat 
                WHERE project = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (project, limit)).fetchall()
            return [_row_to_msg(r) for r in rows]
    except sqlite3.Error as e:
        logger.error(f"[DB] Failed to retrieve chat history: {e}")
        return []

def update_agent_status(name: str, status: str, active_job: str = None):
    """Aktualisiert atomar und transaktionssicher den Online-Status eines Agenten."""
    try:
        with get_db_conn() as conn:
            with conn:
                conn.execute("""
                    UPDATE agents 
                    SET status = ?, active_job = ?, last_seen = ? 
                    WHERE name = ?
                """, (status, active_job, datetime.now(timezone.utc).isoformat(), name))
    except sqlite3.Error as e:
        logger.error(f"[DB] Failed to update agent status for {name}: {e}")

def get_all_agents():
    """Gibt alle Agenten aus der agents-Tabelle zurück."""
    try:
        with get_db_conn() as conn:
            rows = conn.execute("SELECT * FROM agents").fetchall()
            if not rows:
                with conn:
                    _seed_agents(conn)
                rows = conn.execute("SELECT * FROM agents").fetchall()
            
            res = []
            for r in rows:
                d = dict(r)
                try:
                    d["capabilities"] = json.loads(d["capabilities"])
                except (json.JSONDecodeError, TypeError) as e:
                    logger.error(f"[DB] Failed to parse capabilities JSON for agent {d.get('name')}: {e}")
                    d["capabilities"] = []
                res.append(d)
            return res
    except sqlite3.Error as e:
        logger.error(f"[DB] Failed to retrieve agents list: {e}")
        return []


# =====================================================================
# SYSTEM & PROJECT HELPER
# =====================================================================

def get_active_project() -> str:
    try:
        with get_db_conn() as conn:
            row = conn.execute("SELECT value FROM state WHERE key='active_project'").fetchone()
            return json.loads(row["value"]) if row else "default"
    except (sqlite3.Error, json.JSONDecodeError, TypeError) as e:
        logger.error(f"[DB] Failed to get active project: {e}")
        return "default"

def set_active_project(name: str):
    try:
        with get_db_conn() as conn:
            with conn:
                conn.execute("INSERT OR REPLACE INTO state (key, value) VALUES ('active_project', ?)", (json.dumps(name.strip()),))
    except sqlite3.Error as e:
        logger.error(f"[DB] Failed to set active project: {e}")

def get_language() -> str:
    try:
        with get_db_conn() as conn:
            row = conn.execute("SELECT value FROM state WHERE key='language'").fetchone()
            return json.loads(row["value"]) if row else "en"
    except (sqlite3.Error, json.JSONDecodeError, TypeError) as e:
        logger.error(f"[DB] Failed to get language: {e}")
        return "en"

def set_language(lang: str):
    try:
        with get_db_conn() as conn:
            with conn:
                conn.execute("INSERT OR REPLACE INTO state (key, value) VALUES ('language', ?)", (json.dumps(lang.strip().lower()),))
    except sqlite3.Error as e:
        logger.error(f"[DB] Failed to set language: {e}")


# =====================================================================
# LEGACY COMPATIBILITY LAYER (MINIMAL)
# =====================================================================

def get_db(n: str):
    if n == "agents":
        return get_all_agents()
    if n in ("chat", "memory"):
        return get_chat_history(limit=100)
            
    try:
        with get_db_conn() as conn:
            row = conn.execute("SELECT value FROM state WHERE key=?", (n,)).fetchone()
            return json.loads(row["value"]) if row else []
    except (sqlite3.Error, json.JSONDecodeError, TypeError) as e:
        logger.error(f"[DB] Legacy get_db('{n}') failed: {e}")
        return []

def save_db(n: str, d):
    try:
        with get_db_conn() as conn:
            with conn:
                if n == "agents":
                    for a in d:
                        conn.execute("""
                            INSERT OR REPLACE INTO agents (name, id, port, description, status, capabilities, role, active_job, last_seen)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (a["name"], a.get("id", str(uuid.uuid4())), a.get("port", 0), a.get("description"), a.get("status", "online"), 
                              json.dumps(a.get("capabilities", [])), a.get("role", "normal"), a.get("active_job"), datetime.now(timezone.utc).isoformat()))
                elif n in ("chat", "memory"):
                    for m in d:
                        conn.execute("""
                            INSERT OR REPLACE INTO chat (id, project, sender, agent_id, msg_type, content, timestamp, metadata)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (m.get("id", str(uuid.uuid4())), m.get("project", "default"), m.get("metadata", {}).get("sender", "user"),
                              m.get("agent_id", "war-room"), m.get("metadata", {}).get("type", "chat"), m.get("content"),
                              m.get("timestamp", datetime.now(timezone.utc).isoformat()),
                              json.dumps(m.get("metadata", {}))))
                else:
                    conn.execute("INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)", (n, json.dumps(d)))
    except (sqlite3.Error, TypeError) as e:
        logger.error(f"[DB] Legacy save_db('{n}') failed: {e}")
