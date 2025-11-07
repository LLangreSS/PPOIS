import pytest
from documents.Transcript import Transcript
from people.Student import Student
from academia.Group import Group

def test_transcript_init():
    group = Group("G1", 1)
    student = Student(1, "Alex", "a@example.com", group)
    transcript = Transcript(student)
    assert transcript.student == student
    assert transcript.owner == student

def test_generate_grades_summary():
    group = Group("G1", 1)
    student = Student(1, "Alex", "a@example.com", group)
    # Добавим оценку
    from academia.Grade import Grade
    from academia.Course import Course
    c = Course("Math", 5)
    Grade(student, c, 85.0)
    transcript = Transcript(student)
    summary = transcript.generate_grades_summary()
    assert "85.0" in summary