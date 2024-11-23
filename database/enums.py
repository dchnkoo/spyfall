import enum


class PackageScope(enum.StrEnum):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"


class PackageType(enum.StrEnum):
    BASE = "BASE"
    USER = "USER"
