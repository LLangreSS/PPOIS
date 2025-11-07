from __future__ import annotations

class StudyPlan:
    def __init__(self, curriculum: "Curriculum"):
        self.curriculum = curriculum
        self.approved = False

    def needs_approval(self) -> bool:
        return not self.approved

    def is_valid(self) -> bool:
        return self.approved and len(self.curriculum.content) > 0
