from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from ..config import APP_CONFIG


class BackupService:
    def __init__(self, database_path: str | Path | None = None, backup_dir: str | Path | None = None):
        self.database_path = Path(database_path or APP_CONFIG.database_path)
        self.backup_dir = Path(backup_dir or APP_CONFIG.backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = self.backup_dir / f"invox_backup_{timestamp}.db"
        shutil.copy2(self.database_path, target)
        return target

    def restore_backup(self, backup_file: str | Path) -> Path:
        backup_file = Path(backup_file)
        shutil.copy2(backup_file, self.database_path)
        return self.database_path
