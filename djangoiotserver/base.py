# -*- coding: UTF-8 -*-
import os
from unipath import Path

PROJECT_DIR = Path(__file__).parent.parent
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
USE_I18N  = True
USE_L10N  = True
USE_TZ    = True
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-CN'
#LANGUAGE_CODE = 'en-us'
DEFAULT_CHARSET = 'UTF-8'
SITE_ID   = 1
LOCALE_PATHS  = (
    'locale',
)
LANGUAGES = (
    ('zh-CN', u'简体中文'),
    ('zh-tw', u'繁體中文'),
    ('en', u'English'),
    ('de', u'Deutsch'),
#    ('fr', u'Français'),
#    ('it', u'Italiano'),
#    ('pt', u'Português'),
#    ('es', u'Español'),
#    ('sv', u'Svenska'),
#    ('ru', u'Русский'),
#    ('jp', u'日本語'),
#    ('ko', u'한국어'),
)

# Run management command 'set_site_values to set these values
SITE_NAME = 'Djando IoT Site'
SITE_DOMAIN = 'www.myiot.com'
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, '')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
FIXTURE_DIRS  = (
    os.path.join(BASE_DIR, 'fixtures'),
)
TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL='/dashboard/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL='/dashboard/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',

    # Used by Grappelli
    'django.core.context_processors.request',

    # 3rd-party context processors
    'stickymessages.context_processors.latest_sticky_message',

    # GlucoseTracker context processors
    'core.context_processors.third_party_tracking_ids',
    'core.context_processors.site_info',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 3rd-party middlewares
    'axes.middleware.FailedLoginMiddleware',
)

ROOT_URLCONF = 'djangoiotserver.urls'
WSGI_APPLICATION = 'djangoiotserver.wsgi.application'

INSTALLED_APPS = (
    # Grappelli custom admin, needs to be defined before the admin app.
    'grappelli',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    # 3rd-party apps
    'rest_framework',
    'axes',
    'compressor',
    'crispy_forms',
    'gunicorn',
    'chineseaddress',   
    'redactor',
    'stickymessages',
    'taggit',
    'storages',

    
    # Local apps
    'core',
    'air',
    'subscribers',
    'settings',
    'accounts',    
)

# Django-crispy-forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Django-axes settings
AXES_LOGIN_FAILURE_LIMIT = 20

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Session cookie expiration in seconds
SESSION_COOKIE_AGE = 7776000

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s  [%(name)s:%(lineno)s]  %(levelname)s - %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        # Silence SuspiciousOperation.DisallowedHost exception ('Invalid
        # HTTP_HOST' header messages). Set the handler to 'null' so we don't
        # get those annoying emails.
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['console', ],
            'level': 'INFO',
        }
    }
}

# Grappelli settings.
GRAPPELLI_ADMIN_TITLE = SITE_NAME

# Django WYSIWYG Redactor settings.
REDACTOR_OPTIONS = {
    'lang': 'en',
    'buttonSource': 'true',
    'toolbarFixed': 'true',
}
REDACTOR_UPLOAD = 'editor-uploads/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'PAGINATE_BY': 50
}
