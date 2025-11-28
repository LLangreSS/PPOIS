from __future__ import annotations
from typing import Callable, List, Dict

class NotificationCenter:
    """
    Центральный узел для уведомлений на основе событий в системе склада.
    Поддерживает слабую связность между компонентами через шаблон издатель-подписчик.
    """

    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[str, dict], None]]] = {}

    def subscribe(self, event_type: str, callback: Callable[[str, dict], None]) -> None:
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def notify(self, event: str, payload: dict) -> None:
        event_type = payload.get('type', 'general')
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(event, payload)

    def unsubscribe(self, event_type: str, callback: Callable[[str, dict], None]) -> None:
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)

