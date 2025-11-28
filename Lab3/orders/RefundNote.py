from __future__ import annotations
from datetime import datetime
from staff.Employee import Employee


class RefundNote:
    """
    Документирует финансовое возмещение за обработанный возврат.
    Привязан к запросу на возврат и сотруднику, который его обработал.
    """

    def __init__(self, return_id: str, amount: float, processed_by: Employee):
        if amount <= 0:
            raise ValueError("Refund amount must be positive")
        self.return_id = return_id
        self.amount = amount
        self.processed_by = processed_by
        self.processed_date = datetime.now()
        self.status = "created"

    def issue(self) -> bool:
        """
        Выпускает возмещение и обновляет статус.
        """
        self.status = "issued"
        return True

    def get_refund_details(self) -> dict:
        """
        Возвращает детали возмещения в виде словаря с ключами на английском языке.
        """
        return {
            "return_id": self.return_id,
            "amount": self.amount,
            "processed_by": self.processed_by.name,
            "processed_date": self.processed_date,
            "status": self.status
        }