from __future__ import annotations
from documents.Document import Document
class Diploma(Document):
    def __init__(self, graduate: "Graduate", degree: str):
        super().__init__(f"DP-{graduate.person_id}", graduate, "2025-06-15")
        self.graduate = graduate
        self.degree = degree

    def reissue(self) -> None:
        self.issue_date = "2025-11-06"

    def is_authentic(self) -> bool:
        return self.approved and len(self.degree) > 0

    def get_degree_level(self) -> str:
        return "Bachelor" if "бакалавр" in self.degree.lower() else "Master"

    def verify_by_ministry(self) -> bool:
        return self.is_authentic()
