from typing import Callable
import base64

from PyQt5 import uic
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QThreadPool, QObject
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QImage

from realtime.model import Notification
from realtime.provider import RealtimeProvider


class RealtimeWorkerSignals(QObject):
    notification_received = pyqtSignal(Notification)
    time_updated = pyqtSignal(str)


class RealtimeWorker(QRunnable):
    signals: RealtimeWorkerSignals
    provider: RealtimeProvider

    def __init__(self, provider: RealtimeProvider):
        super().__init__()
        self.signals = RealtimeWorkerSignals()
        self.provider = provider

    @pyqtSlot()
    def run(self) -> None:
        def get_emitter(signal: pyqtSignal) -> Callable:
            return lambda v: signal.emit(v)

        self.provider.notification_emitter = get_emitter(self.signals.notification_received)
        self.provider.time_emitter = get_emitter(self.signals.time_updated)
        self.provider.start()


class MainWindow(QMainWindow):
    notification_downloader_thread: QThreadPool

    icon: QLabel
    appName: QLabel
    title: QLabel
    content: QLabel
    timeDisplay: QLabel
    hideButton: QPushButton

    time_display_format: str

    def __init__(self, realtime_provider: RealtimeProvider, windowed: bool):
        super(MainWindow, self).__init__()
        self.notification_downloader_thread = QThreadPool()
        uic.loadUi("ui/main.ui", self)
        self.time_display_format = self.timeDisplay.text()
        self._reset_controls()
        self._connect_signals()
        self.show()

        if not windowed:
            self.showFullScreen()

        self._init_realtime_worker(realtime_provider)

    def hide_notification(self):
        self.icon.setPixmap(QPixmap())
        self.appName.setText("")
        self.title.setText("")
        self.content.setText("")
        self.hideButton.setVisible(False)

    def _reset_controls(self):
        self.hide_notification()
        self.timeDisplay.setText("Oczekuję na czas")

    def _connect_signals(self):
        self.hideButton.clicked.connect(self.hide_notification)

    def _init_realtime_worker(self, realtime_provider: RealtimeProvider):
        worker = RealtimeWorker(realtime_provider)
        worker.signals.notification_received.connect(self._on_notification_received)
        worker.signals.time_updated.connect(self._on_time_updated)
        self.notification_downloader_thread.start(worker)

    def _on_notification_received(self, notification: Notification):
        self.icon.setPixmap(QPixmap(QImage.fromData(base64.b64decode(notification.icon))))
        self.appName.setText(notification.appName)
        self.title.setText(notification.title)
        self.content.setText(notification.content)
        self.hideButton.setVisible(True)

    def _on_time_updated(self, time: str):
        self.timeDisplay.setText(self.time_display_format % time)
