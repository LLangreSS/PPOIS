import pytest
import sys
import os
from people.Person import Person
from people.Applicant import Applicant

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class MockApplication:
    """Минимальная заглушка для Application, чтобы избежать circular import в тестах."""
    def __init__(self, applicant, program: str = "CS"):
        self.owner = applicant
        self.program = program
        self.submitted = False


class TestApplicant:
    def test_applicant_instantiation(self):
        person_id = 101
        name = "Alex Petrov"
        email = "alex@example.com"
        application = MockApplication(None, "Data Science")

        applicant = Person.__new__(Applicant)  # bypass __init__ temporarily
        Applicant.__init__(applicant, person_id, name, email, application)

        assert applicant.person_id == 101
        assert applicant.name == "Alex Petrov"
        assert applicant.email == "alex@example.com"
        assert applicant.application == application

    def test_submit_application(self):
        application = MockApplication(None)
        applicant = Applicant(102, "Ivan Sidorov", "ivan@example.com", application)

        applicant.submit_application()

        assert applicant.application.submitted is True

    def test_withdraw_application(self):
        application = MockApplication(None)
        applicant = Applicant(103, "Maria Ivanova", "maria@example.com", application)
        applicant.submit_application()

        applicant.withdraw()

        assert applicant.application.submitted is False

    def test_is_complete_true(self):
        application = MockApplication(None, program="ML")
        applicant = Applicant(104, "Dmitry", "dmitry@example.com", application)

        assert applicant.is_complete() is True

    def test_is_complete_false(self):
        application = MockApplication(None)
        application.program = None  # simulate incomplete
        applicant = Applicant(105, "Oleg", "oleg@example.com", application)

        assert applicant.is_complete() is False

