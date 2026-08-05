from typing import Any, Dict, List

from invox.db.manager import db


class BaseRepository:

    table_name = None


    def __init__(self, table_name=None):
        if table_name:
            self.table_name = table_name

        if not self.table_name:
            raise ValueError("table_name is required")


    def get_all(self) -> List[Dict[str, Any]]:
        return db.select_all(self.table_name)


    def get_by_id(self, record_id: int):
        return db.select_by_id(
            self.table_name,
            record_id
        )


    def create(self, data: Dict[str, Any]):
        return db.insert(
            self.table_name,
            data
        )


    def update(self, record_id: int, data: Dict[str, Any]):
        return db.update(
            self.table_name,
            record_id,
            data
        )


    def delete(self, record_id: int):
        return db.delete(
            self.table_name,
            record_id
        )