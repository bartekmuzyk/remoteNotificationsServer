from typing import Optional
import json
import sys

from PyQt5.QtWidgets import QApplication

from ui.window import MainWindow
from notifications.provider import BaseNotificationProvider
from notifications.providers import MockNotificationProvider, NetworkNotificationProvider

notification_provider: Optional[BaseNotificationProvider] = None

if len(sys.argv) >= 3:
    mock_mode: bool = sys.argv[1] == "mock"

    if mock_mode:
        with open(sys.argv[2], encoding="utf8") as mock_file:
            notification_provider = MockNotificationProvider(json.load(mock_file))


if not notification_provider:
    notification_provider = NetworkNotificationProvider()


app = QApplication([])
main_window = MainWindow(notification_provider, windowed="windowed" in sys.argv)
app.exec()
notification_provider.active = False  # Deactivate provider to tell the worker thread to stop its job
