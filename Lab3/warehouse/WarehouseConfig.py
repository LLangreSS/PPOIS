from __future__ import annotations
from .StorageCondition import StorageCondition

class WarehouseConfig:
    """
    Централизованная конфигурация для общескладских политик,
    таких как условия хранения по умолчанию или правила автоматизации.
    """

    def __init__(
        self,
        timezone: str = "UTC",
        default_condition: StorageCondition = None,
        auto_consolidate: bool = False,
        max_pallet_weight: float = 1000.0,
        enable_expiry_tracking: bool = True
    ):
        self.timezone = timezone
        self.default_condition = default_condition or StorageCondition()
        self.auto_consolidate = auto_consolidate
        self.max_pallet_weight = max_pallet_weight
        self.enable_expiry_tracking = enable_expiry_tracking

    def validate_config(self) -> bool:
        """Проверяет корректность конфигурации склада."""
        return (
            self.max_pallet_weight > 0 and
            len(self.timezone) > 0 and
            self.default_condition is not None
        )

    def get_config_summary(self) -> dict:
        """Возвращает сводку конфигурации."""
        return {
            "timezone": self.timezone,
            "auto_consolidate": self.auto_consolidate,
            "max_pallet_weight": self.max_pallet_weight,
            "enable_expiry_tracking": self.enable_expiry_tracking
        }

