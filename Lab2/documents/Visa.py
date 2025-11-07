from __future__ import annotations
from documents.Document import Document
class Visa(Document):
    def __init__(self, student: "ForeignStudent", expiry_date: str):
        super().__init__(f"VS-{student.person_id}", student, "2024-01-10")
        self.expiry_date = expiry_date

    def is_expired(self) -> bool:
        return self.expiry_date < "2025-11-06"

    def extend(self, days: int) -> None:
        self.expiry_date = "2026-11-06"
