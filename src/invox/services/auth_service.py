from __future__ import annotations

import base64
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from ..config import APP_CONFIG
from ..constants import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USERNAME
from ..db.connection import get_session
from ..models.user import User


class AuthService:
    def __init__(self, db_session: Session | None = None):
        self.db_session = db_session or get_session()
        self.remember_me_path = Path(APP_CONFIG.remember_me_path)

    @staticmethod
    def _make_salt() -> str:
        return base64.urlsafe_b64encode(os.urandom(16)).decode("ascii")

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        digest = hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()
        return digest

    def seed_default_admin(self) -> User:
        user = self.db_session.query(User).filter(User.username == DEFAULT_ADMIN_USERNAME).first()
        if user is None:
            salt = self._make_salt()
            user = User(
                username=DEFAULT_ADMIN_USERNAME,
                password_hash=self.hash_password(DEFAULT_ADMIN_PASSWORD, salt),
                salt=salt,
                role="admin",
                is_active=True,
            )
            self.db_session.add(user)
            self.db_session.commit()
            self.db_session.refresh(user)
        return user

    def authenticate(self, username: str, password: str, remember_me: bool = False) -> User | None:
        user = self.db_session.query(User).filter(User.username == username, User.is_active.is_(True)).first()
        if user is None:
            return None
        if user.password_hash != self.hash_password(password, user.salt):
            return None
        user.last_login = datetime.utcnow()
        user.remember_me = remember_me
        self.db_session.commit()
        self._store_remembered_user(username if remember_me else "")
        return user

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        user = self.db_session.query(User).filter(User.username == username).first()
        if user is None or user.password_hash != self.hash_password(old_password, user.salt):
            return False
        user.salt = self._make_salt()
        user.password_hash = self.hash_password(new_password, user.salt)
        self.db_session.commit()
        return True

    def _store_remembered_user(self, username: str) -> None:
        payload = {"username": username} if username else {}
        self.remember_me_path.write_text(json.dumps(payload), encoding="utf-8")

    def load_remembered_user(self) -> str:
        if not self.remember_me_path.exists():
            return ""
        try:
            payload = json.loads(self.remember_me_path.read_text(encoding="utf-8"))
            return payload.get("username", "")
        except json.JSONDecodeError:
            return ""
