from __future__ import annotations
from exceptions.ScholarshipCriteriaException import ScholarshipCriteriaException

class Scholarship:
    MIN_GPA = 85.0

    def __init__(self, student: "Student", amount: float):
        self.student = student
        self.amount = amount
        self.awarded = False

    def evaluate_eligibility(self) -> bool:
        record = getattr(self.student, 'academic_record', None)
        if not record:
            raise ScholarshipCriteriaException("No academic record.")
        avg_grade = record.get_gpa()
        if avg_grade < self.MIN_GPA:
            raise ScholarshipCriteriaException(f"GPA {avg_grade:.2f} below threshold {self.MIN_GPA}.")
        return True

    def disburse(self) -> None:
        self.student.balance += self.amount
        self.awarded = True

    def revoke(self) -> None:
        if self.awarded:
            self.student.balance -= self.amount
            self.awarded = False
