from __future__ import annotations
from documents.Document import Document
class TransferDocument(Document):
    def __init__(self, student: "Student", from_group: "Group", to_group: "Group"):
        super().__init__(f"TD-{student.person_id}", student, "2025-11-06")
        self.from_group = from_group
        self.to_group = to_group
        self.processed = False

    def process(self) -> None:
        if self.from_group != self.owner.group:
            raise ValueError("Student not in the source group.")
        self.to_group.add_student(self.owner)
        self.from_group.remove_student(self.owner)
        self.processed = True

    def is_valid(self) -> bool:
        return self.approved and self.processed
