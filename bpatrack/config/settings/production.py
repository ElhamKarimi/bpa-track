# -*- coding: utf-8 -*-
'''
Production Configurations

- Use djangosecure
'''

from __future__ import absolute_import, unicode_literals

from django.utils import six


from .common import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env.get("DJANGO_SECRET_KEY")

# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# django-secure
# ------------------------------------------------------------------------------
INSTALLED_APPS += ("djangosecure", )

SECURITY_MIDDLEWARE = (
    'djangosecure.middleware.SecurityMiddleware',
)


# Make sure djangosecure.middleware.SecurityMiddleware is listed first
MIDDLEWARE_CLASSES = SECURITY_MIDDLEWARE + MIDDLEWARE_CLASSES

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.get( "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", True)
SECURE_FRAME_DENY = env.get("DJANGO_SECURE_FRAME_DENY", True)
SECURE_CONTENT_TYPE_NOSNIFF = env.get("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = env.get("DJANGO_SECURE_SSL_REDIRECT", True)

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.get('DJANGO_ALLOWED_HOSTS', 'downloads.bioplatforms.com')
# END SITE CONFIGURATION


# Static Assets
# ------------------------
#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env.get('DJANGO_DEFAULT_FROM_EMAIL', 'No Reply <no-reply@mg.ccgapps.com.au>')
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = env.get('DJANGO_MAILGUN_API_KEY')
MAILGUN_SERVER_NAME = env.get('DJANGO_MAILGUN_SERVER_NAME')
EMAIL_SUBJECT_PREFIX = env.get("DJANGO_EMAIL_SUBJECT_PREFIX", '[BPA Track] ')
SERVER_EMAIL = env.get('DJANGO_SERVER_EMAIL', DEFAULT_FROM_EMAIL)


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]


# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
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
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'mail_admins'],
            'propagate': True
        }
    }
}


# Your production stuff: Below this line define 3rd party library settings
