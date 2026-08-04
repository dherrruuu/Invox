from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from .constants import PROJECT_ROOT


@dataclass(frozen=True)
class AppConfig:
	project_root: Path
	database_path: Path
	bills_dir: Path
	quotations_dir: Path
	customers_dir: Path
	backup_dir: Path
	reports_dir: Path
	assets_dir: Path
	remember_me_path: Path

	@property
	def database_url(self) -> str:
		return f"sqlite:///{self.database_path.as_posix()}"

	def as_dict(self) -> Dict[str, str]:
		return {
			"project_root": str(self.project_root),
			"database_path": str(self.database_path),
			"bills_dir": str(self.bills_dir),
			"quotations_dir": str(self.quotations_dir),
			"customers_dir": str(self.customers_dir),
			"backup_dir": str(self.backup_dir),
			"reports_dir": str(self.reports_dir),
			"assets_dir": str(self.assets_dir),
			"remember_me_path": str(self.remember_me_path),
		}


def _resolve_root() -> Path:
	candidates = [PROJECT_ROOT, Path.home() / "INVOX"]
	for candidate in candidates:
		try:
			candidate.mkdir(parents=True, exist_ok=True)
			return candidate
		except OSError:
			continue
	fallback = Path.cwd() / "INVOX"
	fallback.mkdir(parents=True, exist_ok=True)
	return fallback


def load_config() -> AppConfig:
	root = _resolve_root()
	database_dir = root / "Database"
	bills_dir = root / "Bills"
	quotations_dir = root / "Quotations"
	customers_dir = root / "Customers"
	backup_dir = root / "Backup"
	reports_dir = root / "Reports"
	assets_dir = root / "Assets"

	for directory in (database_dir, bills_dir, quotations_dir, customers_dir, backup_dir, reports_dir, assets_dir):
		directory.mkdir(parents=True, exist_ok=True)

	return AppConfig(
		project_root=root,
		database_path=database_dir / "invox.db",
		bills_dir=bills_dir,
		quotations_dir=quotations_dir,
		customers_dir=customers_dir,
		backup_dir=backup_dir,
		reports_dir=reports_dir,
		assets_dir=assets_dir,
		remember_me_path=root / "remember_me.json",
	)


APP_CONFIG = load_config()