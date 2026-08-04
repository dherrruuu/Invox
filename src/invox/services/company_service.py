from __future__ import annotations

from sqlalchemy.orm import Session

from ..db.connection import get_session
from ..models.company_profile import CompanyProfile


class CompanyService:
    def __init__(self, db_session: Session | None = None):
        self.db_session = db_session or get_session()

    def get_profile(self) -> CompanyProfile:
        profile = self.db_session.query(CompanyProfile).filter(CompanyProfile.id == 1).first()
        if profile is None:
            profile = CompanyProfile(id=1)
            self.db_session.add(profile)
            self.db_session.commit()
            self.db_session.refresh(profile)
        return profile

    def update_profile(self, **fields) -> CompanyProfile:
        profile = self.get_profile()
        for key, value in fields.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)
        self.db_session.commit()
        self.db_session.refresh(profile)
        return profile
