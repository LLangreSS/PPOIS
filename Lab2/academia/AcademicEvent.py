from __future__ import annotations

class AcademicEvent:
    def __init__(self, name: str, date: str, description: str = ""):
        self.name = name
        self.date = date
        self.description = description
        self.participants = []

    def register_participant(self, person) -> None:
        self.participants.append(person)

    def send_notification(self) -> str:
        return f"Reminder: {self.name} on {self.date}"

    def is_upcoming(self) -> bool:
        return self.date >= "2025-11-06"
