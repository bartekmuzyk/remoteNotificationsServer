from typing import Callable

from realtime.model import Notification


class RealtimeProvider:
    notification_emitter: Callable[[Notification], None]
    time_emitter: Callable[[str], None]

    def start(self):
        raise NotImplementedError
