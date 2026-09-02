from enum import StrEnum


class Environment(StrEnum):
    development = "development"
    test = "test"  # Used for running tests
    production = "production"


ENV_VAR = "MANYS_ENV"


class MediaType(StrEnum):
    image = "image"
    video = "video"


class RoleType(StrEnum):
    admin = "admin"
    editor = "editor"


ALLOWED_FORMATS = {"png", "jpg", "jpeg", "mp4"}
