from __future__ import annotations

class Conference:
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.researches: list["Research"] = []

    def accept_research(self, research: "Research") -> None:
        self.researches.append(research)
