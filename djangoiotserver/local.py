# -*- coding: UTF-8 -*-
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'SECRET_KEYSECRET_KEYSECRET_KEYSECRET_KEYSECRET_KEY'

# 3rd-party apps tracking IDs.
INTERCOM_APP_ID = None
GOOGLE_ANALYTICS_TRACKING_ID = None
ADDTHIS_PUBLISHER_ID = None

EMAIL_HOST = 'smtp.example.com'
EMAIL_HOST_USER = 'test'
EMAIL_HOST_PASSWORD = 'test'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ADMINS = (
    ('Local Admin', 'root@myiot.com'),
)

MANAGERS = ADMINS

CONTACTS = {
    'support_email': 'support@myiot.com',
    'admin_email': 'admin@myiot.com',
    'info_email': 'info@myiot.com',
}

# For 'subscribers' app
SEND_SUBSCRIBERS_EMAIL_CONFIRMATION = True

#DATABASES = {
#   'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'myiotcom',
#        'USER': 'myiotcom',
#        'PASSWORD': 'password',
#        'HOST': os.environ.get('POSTGRESQL_HOST', 'localhost'),
#        'PORT': '',
#    }
#}

# Django-debug-toolbar config
INSTALLED_APPS += ('debug_toolbar',)
INTERNAL_IPS = (
    '127.0.0.1',
)
MIDDLEWARE_CLASSES += \
    ('debug_toolbar.middleware.DebugToolbarMiddleware', )

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
    'HIDE_DJANGO_SQL': False,
}