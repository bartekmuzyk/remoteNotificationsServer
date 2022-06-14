from typing import Optional

from notifications.provider import BaseNotificationProvider
from notifications.model import Notification


class MockNotificationProvider(BaseNotificationProvider):
    notification: Notification
    got_once: bool

    def __init__(self, data: dict):
        super().__init__()
        self.notification = Notification(**data)
        self.got_once = False

    def get_available_notification(self) -> Optional[Notification]:
        ret = self.notification if not self.got_once else None
        self.got_once = True

        return ret
