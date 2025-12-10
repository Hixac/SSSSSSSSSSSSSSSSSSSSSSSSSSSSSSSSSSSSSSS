from .core.setup import create_application
from .core.config import settings
from .api import router

app = create_application(router, settings)
