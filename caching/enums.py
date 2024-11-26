import enum


class CachePrefix(enum.StrEnum):
    user = "user"
    game_room = "game_room"
    in_game = "in_game"
