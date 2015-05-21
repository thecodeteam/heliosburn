"""
Django settings for hbproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

from django.contrib.messages import constants as message_constants
import os
from configurations import Configuration, values
import redis


class Common(Configuration):

    from mongoengine import connect
    connect(db='heliosburn',
            host=mongo)

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    API_KEY = "deadbeef"

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    TEMPLATE_DEBUG = values.BooleanValue(DEBUG)

    ALLOWED_HOSTS = []

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'mongoengine.django.mongo_auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'django_bootstrap_breadcrumbs',
        'bootstrap3',

        'webui',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.request',
        'django.contrib.messages.context_processors.messages',
    )

    ROOT_URLCONF = 'hbproject.urls'

    WSGI_APPLICATION = 'hbproject.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # This is only used for unit-test stats
            'NAME': 'dummy.sqlite3',
        }
        # 'default': {
        #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #     'NAME': 'heliosburn',
        #     'USER': 'postgres',
        #     'PASSWORD': 'postgres',
        #     'HOST': 'localhost',
        # }
    }

    SESSION_ENGINE = 'mongoengine.django.sessions'
    SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'

    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.7/howto/static-files/

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, '../static')

    LOGIN_URL = '/webui/signin'

    AUTHENTICATION_BACKENDS = (
        'webui.backends.HeliosAuthBackend',
    )

    API_BASE_URL = 'http://127.0.0.1:8000/api'

    TOKEN_TTL = 3600  # milliseconds

    REDIS_HOST = 'redis'
    REDIS_PORT = 6379
    REDIS_DB = 0

    # Workaround to adapt the message levels to Bootstrap css styles
    MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                    message_constants.INFO: 'info',
                    message_constants.SUCCESS: 'success',
                    message_constants.WARNING: 'warning',
                    message_constants.ERROR: 'danger', }

    MONGODB_HOST = 'mongo'
    MONGODB_PORT = 27017
    MONGODB_DATABASE = {
        'production': 'heliosburn',  # for normal operation
        'test': 'heliosburn_test'  # for unit testing
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'redis': {
                'level': 'DEBUG',
                'class': 'redislog.handlers.RedisHandler',
                'channel': 'hblog',
                'redis_client': redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB),
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'INFO',
            },
            'webui': {
                'handlers': ['console', 'redis'],
                'level': 'DEBUG',
            },
            'api': {
                'handlers': ['console', 'redis'],
                'level': 'DEBUG',
            },
        }
    }


class Development(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True

    TEMPLATE_DEBUG = True

    ALLOWED_HOSTS = []

    INSTALLED_APPS = Common.INSTALLED_APPS + (
        'debug_toolbar',
    )

    # Django-Debug-Toolbar workaround to make it work with the Vagrant VM
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': "%s.true" % __name__,
    }


class Staging(Common):
    """
    The in-staging settings.
    """
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']


class Production(Staging):
    """
    The in-production settings.
    """
    pass


# Django-Debug-Toolbar workaround to make it work with the Vagrant VM
def true(request):
    return True
