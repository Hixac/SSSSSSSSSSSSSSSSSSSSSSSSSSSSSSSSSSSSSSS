from fastapi import FastAPI

from .core.setup import create_application
from .api import router


app: FastAPI = create_application(router)
