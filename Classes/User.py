from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    firstname: str
    lastname: str
    is_bot: bool = False

    def __repr__(self) -> str:
        return f'{self.id }: ' + ' '.join(filter(bool, [self.firstname, self.lastname]))\
            + ', is_bot: ' + str(self.is_bot)
