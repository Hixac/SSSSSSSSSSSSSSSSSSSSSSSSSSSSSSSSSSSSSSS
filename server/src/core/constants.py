from enum import StrEnum


class Environment(StrEnum):
    development = "development"
    test = "test"  # Used for running tests
    production = "production"


ENV_VAR = "MANYS_ENV"
