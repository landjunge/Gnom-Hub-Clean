from ...core.config import Config
from ..database.schema import create_tables

class AdminService:
    def nuke(self):
        Config.DB_PATH.unlink(missing_ok=True)
        create_tables()

    def clean(self):
        for p in Config.LOG_DIR.glob("**/*"):
            if p.is_file():
                p.unlink(missing_ok=True)
