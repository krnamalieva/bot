from dataclasses import dataclass
from datetime import datetime
from telegram.classes import User, Chat
from geo import Point


@dataclass(frozen=True)
class Message:
    text: str
    chat: Chat
    user: User = None
    date: datetime = None
    id: int = None
    location: Point = None

    def __repr__(self) -> str:
        return '\n'.join(map(str, filter(bool, [
            self.id,
            self.user,
            self.chat,
            self.date.strftime('%Y-%m-%d %H:%M:%S') if self.date else None,
            self.text,
            self.location
        ])))
