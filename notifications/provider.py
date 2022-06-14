from typing import Optional

from notifications.model import Notification


class BaseNotificationProvider:
    active: bool

    def __init__(self):
        self.active = True

    def get_available_notification(self) -> Optional[Notification]:
        raise NotImplementedError
