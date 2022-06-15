import os
import signal
from typing import Optional
import json
import sys

from PyQt5.QtWidgets import QApplication

from ui.window import MainWindow
from realtime.provider import RealtimeProvider
from realtime.providers import MockProvider, NetworkProvider

realtime_provider: Optional[RealtimeProvider] = None
windowed: bool = False

if "windowed" in sys.argv:
    sys.argv.remove("windowed")
    windowed = True

if len(sys.argv) >= 3:
    mode: str = sys.argv[1]
    mode_arg: str = sys.argv[2]

    match mode:
        case "mock":
            with open(mode_arg, encoding="utf8") as mock_file:
                realtime_provider = MockProvider(json.load(mock_file))
        case "network":
            realtime_provider = NetworkProvider(ip=mode_arg, port=9999)
        case _:
            print(f"Niepoprawny tryb: {mode}", file=sys.stderr)
            sys.exit(1)


app = QApplication([])
main_window = MainWindow(realtime_provider, windowed)
app.exec()
os.kill(os.getpid(), signal.SIGINT)  # Ensure all threads get shut down
