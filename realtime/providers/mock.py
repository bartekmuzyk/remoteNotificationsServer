from typing import Callable

from realtime.model import Notification
from realtime.provider import RealtimeProvider


class MockProvider(RealtimeProvider):
    notification: Notification

    def __init__(self, data: dict):
        self.notification = Notification(**data)

    def start(self):
        self.notification_emitter(self.notification)
        self.time_emitter("12:34")

        while True:
            continue
