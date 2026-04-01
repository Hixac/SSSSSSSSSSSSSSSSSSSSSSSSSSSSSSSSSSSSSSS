import os

from src.core.constants import ENV_VAR, Environment


os.environ[ENV_VAR] = Environment.test


from .fixtures import *
import pytest
