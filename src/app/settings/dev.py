from app.settings.components.base import *
from app.settings.components.database import *
from app.settings.components.dev_tools import *
from app.settings.components.email import *

DEBUG = True

ALLOWED_HOSTS = []

STATIC_ROOT = os.path.join(BASE_DIR, 'cdn/static')
