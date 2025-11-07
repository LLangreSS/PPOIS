from __future__ import annotations

class Person:
    def __init__(self, person_id: int, name: str, email: str):
        self.person_id = person_id
        self.name = name
        self.email = email

    def change_email(self, new_email: str):
        self.email = new_email

    def get_full_info(self) -> str:
        return f"{self.name} <{self.email}>"
