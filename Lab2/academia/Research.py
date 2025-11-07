from __future__ import annotations

class Research:
    def __init__(self, title: str, lead: "Teacher"):
        self.title = title
        self.lead = lead
        self.participants: list["Teacher"] = []

    def add_participant(self, teacher: "Teacher") -> None:
        self.participants.append(teacher)

    def submit_to_conference(self, conference) -> None:
        conference.accept_research(self)
