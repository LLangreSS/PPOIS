from __future__ import annotations
from documents.Document import Document
class Contract(Document):
    def __init__(self, party_a: "Person", party_b: "Person", terms: str):
        super().__init__(f"CT-{party_a.person_id}-{party_b.person_id}", party_a, "2025-11-01")
        self.party_b = party_b
        self.terms = terms

    def validate_parties(self) -> bool:
        return True

    def terminate(self) -> None:
        self.approved = False

    def renew(self, new_terms: str) -> None:
        self.terms = new_terms
        self.approved = True
