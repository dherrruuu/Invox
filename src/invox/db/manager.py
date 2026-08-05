from typing import Any, Dict, List, Optional

from .supabase import get_supabase


class DatabaseManager:
    def __init__(self):
        self.client = get_supabase()

    # ---------- SELECT ----------

    def select_all(self, table: str) -> List[Dict[str, Any]]:
        response = self.client.table(table).select("*").execute()
        return response.data or []

    def select_by_id(self, table: str, record_id: int):
        response = (
            self.client.table(table)
            .select("*")
            .eq("id", record_id)
            .execute()
        )
        return response.data[0] if response.data else None

    def find(self, table: str, column: str, value):
        response = (
            self.client.table(table)
            .select("*")
            .eq(column, value)
            .execute()
        )
        return response.data

    # ---------- INSERT ----------

    def insert(self, table: str, data: Dict[str, Any]):
        response = self.client.table(table).insert(data).execute()
        return response.data

    # ---------- UPDATE ----------

    def update(self, table: str, record_id: int, data: Dict[str, Any]):
        response = (
            self.client.table(table)
            .update(data)
            .eq("id", record_id)
            .execute()
        )
        return response.data

    # ---------- DELETE ----------

    def delete(self, table: str, record_id: int):
        response = (
            self.client.table(table)
            .delete()
            .eq("id", record_id)
            .execute()
        )
        return response.data


db = DatabaseManager()