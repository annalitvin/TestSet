from app.settings.components.base import *
from app.settings.components.database import *
from app.settings.components.email import *


DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(':')

STATIC_ROOT = '/var/www/TestSet/static'

MEDIA_ROOT = '/var/www/TestSet/media'

