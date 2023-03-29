from dataclasses import dataclass


@dataclass(frozen=True)
class Chat:
    id: int

    def __repr__(self) -> str:
        return str(self.id)
