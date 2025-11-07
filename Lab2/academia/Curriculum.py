from __future__ import annotations

class Curriculum:
    def __init__(self, program: str, content: str = ""):
        self.program = program
        self.content = content

    def is_outdated(self, year: int) -> bool:
        try:
            prog_year = int(self.program.split('-')[-1])
            return year - prog_year > 5
        except (ValueError, IndexError):
            return True

    def assign_to_study_plan(self, plan: "StudyPlan") -> None:
        plan.curriculum = self
