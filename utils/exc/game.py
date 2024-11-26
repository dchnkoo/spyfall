class GameException(Exception):
    pass


class Exit(GameException):
    pass


class GameEnd(GameException):
    pass


class GameRoomNotExists(GameException):
    pass


class RoundException(GameException):
    pass


class RoundNotEnded(RoundException):
    pass


class NotSave(GameException):
    pass
