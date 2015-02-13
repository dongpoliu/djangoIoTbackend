# -*- coding: UTF-8 -*-
"""
Django settings for djangoiotserver project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
#new added part
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from unipath import Path

from decouple import config
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
PROJECT_DIR = Path(__file__).parent.parent
#end of new added part

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Set paths -- new added
fillPath = lambda x: os.path.join(os.path.dirname(__file__), x)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'n)o(80l_#4^fdfee=w)lgc7$_+t5qgsxu%@rf5nm3msh5!9!+f'
SECRET_KEY = 'SECRET_KEYSECRET_KEYSECRET_KEYSECRET_KEYSECRET_KEY'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',    
    'django.contrib.sites',
    'django.contrib.admindocs',    
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    #added for location 
    'geoposition',
    'compressor',
    # local apps
    'core',
    'devices',
    'settings',
    'userauth',    
)

MIDDLEWARE_CLASSES = (  
    'django.contrib.sessions.middleware.SessionMiddleware',     
    'django.middleware.locale.LocaleMiddleware',  # new added     
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',# new added
    'django.middleware.cache.CacheMiddleware',# new added
    'django.middleware.transaction.TransactionMiddleware',# new added
    'django.middleware.cache.FetchFromCacheMiddleware', # new added
    'django.middleware.cache.UpdateCacheMiddleware',# new added  
)

ROOT_URLCONF = 'djangoiotserver.urls'
WSGI_APPLICATION = 'djangoiotserver.wsgi.application'
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': True
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
USE_I18N  = True
USE_L10N  = True
USE_TZ    = True
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-CN'
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'


#new added part
LOGIN_REDIRECT_URL = '/devices/'
PROJECT_ROOT = BASE_DIR
STATIC_ROOT = os.path.join(PROJECT_ROOT, '')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

FIXTURE_DIRS  = (
    os.path.join(BASE_DIR, 'fixtures'),
)

#modifieded
#TEMPLATE_DIRS = (
#    os.path.join(PROJECT_ROOT, 'templates').replace('\\','/'),
#)
TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

#AUTHENTICATION_BACKENDS = (
#        'django.contrib.auth.backends.ModelBackend',
#        'guardian.backends.ObjectPermissionBackend',
#)

LOGIN_URL = '/signin/'
LOGOUT_URL = '/signout/'

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
DEFAULT_FROM_EMAIL = 'Django IoT Mgmt <rubinliu@hotmail.com>'

FILE_UPLOAD_TEMP_DIR = '/tmp/'
FILE_UPLOAD_PERMISSIONS = 0644

HTTPS_SUPPORT = config('HTTPS_SUPPORT', default=True, cast=bool)
SECURE_REQUIRED_PATHS = (
    '/',
    '/admin/',
    '/signin/',
    '/signup/',
    '/reset/',
    '/settings/password/',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'PAGINATE_BY': 50
}

# apps configuration required for Django
INSTALLED_APPS += (
)

# DOMAIN will be used in link generation specially in emails
DOMAIN = '127.0.0.1:8000'

# SITE_NAME it will be used in all pages, this is the name of your website
SITE_NAME = 'Djando IoT Site'

# SITE_TITLE for index pages of your website
SITE_TITLE = 'IoT by Django'

# Meta description for SEO
SITE_DESCRIPTION = 'IoT by Django'

# COPYRIGHT statement for all pages
COPYRIGHT = 'Copyright &copy; 2015 Dongpo. All rights reserved.'

# SUPPORT_EMAIL address for bugs and error reporting
SUPPORT_EMAIL = 'rubinliu@hotmail.com'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#Allow CORS requests from all domains (oauth2)
CORS_ORIGIN_ALLOW_ALL = True

SITEMESSAGES_SETTINGS = {
    'twitter': [],
    'smtp': []
}

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

# some johnny settings
#CACHES = {
#  'default' : dict(
#        BACKEND = 'johnny.backends.memcached.MemcachedCache',
#      LOCATION = ['127.0.0.1:11211'],
#        JOHNNY_CACHE = True,
#   )
#}
#JOHNNY_MIDDLEWARE_KEY_PREFIX='jc_myproj'
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
CACHE_BACKEND = 'db://django_db'

 