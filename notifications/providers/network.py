from typing import Optional

from notifications.provider import BaseNotificationProvider
from notifications.model import Notification


class NetworkNotificationProvider(BaseNotificationProvider):
    def get_available_notification(self) -> Optional[Notification]:
        return None
