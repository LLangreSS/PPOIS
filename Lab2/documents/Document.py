from __future__ import annotations

class Document:
    def __init__(self, doc_id: str, owner: "Person", issue_date: str):
        self.doc_id = doc_id
        self.owner = owner
        self.issue_date = issue_date
        self.approved = False

    def approve(self) -> None:
        self.approved = True

    def is_valid(self) -> bool:
        return self.approved
