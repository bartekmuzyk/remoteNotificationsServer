from dataclasses import dataclass


@dataclass
class Notification:
    appName: str
    icon: str  # Icon data encoded in Base64
    title: str
    content: str
