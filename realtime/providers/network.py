import json
from typing import Optional, Final, Callable
import sys
import traceback
from datetime import datetime

from flask import Flask, request
from werkzeug.exceptions import BadRequest

from realtime.provider import RealtimeProvider
from realtime.model import Notification


NotifyRequestHandler = Callable[[Notification], None]

PROTOCOL_VERSION: Final[int] = 1


class InvalidNotificationData(Exception):
    pass


class NetworkProvider(RealtimeProvider):
    address: tuple[str, int]

    def __init__(self, ip: str, port: int):
        self.address = ip, port

    def start(self):
        app = Flask(__name__)
        app.add_url_rule("/ver", view_func=lambda: str(PROTOCOL_VERSION))
        app.add_url_rule("/notify", methods=["POST"], view_func=self._handle_notify_request)
        app.add_url_rule("/time", methods=["POST"], view_func=self._handle_time_request)
        app.run(*self.address, debug=False)

    def _handle_notify_request(self):
        req_data = request.data.decode("utf8")

        try:
            data: dict = json.loads(req_data)

            if not isinstance(data, dict):
                raise InvalidNotificationData
        except Exception as e:
            print(f"Nie udało się przetworzyć danych w żądaniu:\n{req_data}\n\n", file=sys.stderr)
            traceback.print_tb(e.__traceback__, file=sys.stderr)

            return

        if "icon" not in data:
            data["icon"] = ""

        self.notification_emitter(Notification(**data))

        return "ok"

    def _handle_time_request(self):
        unix_timestamp = round(float(request.data.decode("utf8")))
        time = datetime.fromtimestamp(unix_timestamp)
        formatted = time.strftime("%d %b %H:%M")
        self.time_emitter(formatted)

        return "ok"
