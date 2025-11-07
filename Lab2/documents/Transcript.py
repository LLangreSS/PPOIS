from __future__ import annotations
from documents.Document import Document
class Transcript(Document):
    def __init__(self, student: "Student"):
        super().__init__(f"TR-{student.person_id}", student, "2025-11-06")
        self.student = student

    def generate_grades_summary(self) -> str:
        grades = [str(g.value) for g in getattr(self.student, 'academic_record', type('', (), {'grades': []})()).grades]
        return ", ".join(grades) if grades else "No grades"
