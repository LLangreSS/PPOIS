from __future__ import annotations
from documents.Document import Document
class Certificate(Document):
    def __init__(self, recipient: "Person", title: str, description: str = ""):
        super().__init__(f"CT-{recipient.person_id}", recipient, "2025-11-06")
        self.title = title
        self.description = description

    def revoke(self) -> None:
        self.approved = False

    def is_valid_for_visa(self) -> bool:
        return self.approved and "language" in self.title.lower()
