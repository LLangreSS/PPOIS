from __future__ import annotations
from documents.Document import Document
class Application(Document):
    def __init__(self, applicant: "Applicant", program: str):
        super().__init__(f"AP-{applicant.person_id}", applicant, "2025-10-01")
        self.program = program
        self.submitted = False

    def withdraw(self) -> None:
        self.submitted = False

    def is_complete(self) -> bool:
        return bool(getattr(self, 'program', None))
