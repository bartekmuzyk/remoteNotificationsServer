import time
import base64

from PyQt5 import uic
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QThreadPool, QObject
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QImage

from notifications.model import Notification
from notifications.provider import BaseNotificationProvider


class NotificationDownloaderSignals(QObject):
    notification_received = pyqtSignal(Notification)


class NotificationDownloaderWorker(QRunnable):
    signals: NotificationDownloaderSignals
    provider: BaseNotificationProvider

    def __init__(self, provider: BaseNotificationProvider):
        super().__init__()
        self.signals = NotificationDownloaderSignals()
        self.provider = provider

    @pyqtSlot()
    def run(self) -> None:
        while self.provider.active:
            notification_data = self.provider.get_available_notification()

            if notification_data:
                self.signals.notification_received.emit(notification_data)

            time.sleep(1)


class MainWindow(QMainWindow):
    notification_downloader_thread: QThreadPool

    icon: QLabel
    appName: QLabel
    title: QLabel
    content: QLabel

    def __init__(self, notification_provider: BaseNotificationProvider, windowed: bool):
        super(MainWindow, self).__init__()
        self.notification_downloader_thread = QThreadPool()
        uic.loadUi("ui/main.ui", self)
        self._reset_controls()
        self.show()

        if not windowed:
            self.showFullScreen()

        self._init_notification_worker(notification_provider)

    def _reset_controls(self):
        self.appName.setText("")
        self.title.setText("")
        self.content.setText("")

    def _init_notification_worker(self, notification_provider: BaseNotificationProvider):
        worker = NotificationDownloaderWorker(notification_provider)
        worker.signals.notification_received.connect(self._on_notification_received)
        self.notification_downloader_thread.start(worker)

    def _on_notification_received(self, notification: Notification):
        self.icon.setPixmap(QPixmap(QImage.fromData(base64.b64decode(notification.icon))))
        self.appName.setText(notification.appName)
        self.title.setText(notification.title)
        self.content.setText(notification.content)
