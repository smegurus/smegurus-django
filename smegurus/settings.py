"""
Django settings for smegurus project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Python .ENV Configuration
#

"""Add support for .env files."""
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def env_var(key, default=None):
  """Retrieves env vars and makes Python boolean replacements"""
  val = os.environ.get(key, default)
  if val == 'True':
      val = True
  elif val == 'False':
      val = False
  return val

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_var("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_var("IS_DEBUG")

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# Note: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-USE_X_FORWARDED_HOST
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = [env_var("ALLOWED_HOSTS")]

# The person to contact on error when DEBUG=False
ADMINS = [(env_var("ADMIN_NAME"), env_var("ADMIN_EMAIL")),]

SITE_ID = 1

# Automatically redirect to SSL.
# Note: https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env_var("SECURE_SSL_REDIRECT")


# Application definition

SHARED_APPS = (
  # everything below here is mandatory
  'django_tenants',  # mandatory
  'django.contrib.contenttypes', # mandatory
  'foundation_public', # you must list the app where your tenant model resides in

  # everything below is custom made by us.
  'public_index',
  'foundation_auth',

  # everything below here is optional
  'django.contrib.auth',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.sitemaps',
  'django.contrib.messages',
  'django.contrib.admin',
  'django.contrib.staticfiles',
  'rest_framework',
  'rest_framework.authtoken',
  # 'storages',
  "compressor",
)

TENANT_APPS = (
  # your tenant-specific apps
  'foundation_tenant',
  'api',
  'foundation_auth',
  'foundation_config',
  'tenant_profile',
  'tenant_message',
  'tenant_calendar',
  'tenant_community',
  'tenant_goal',
  'tenant_learning',
  'tenant_mywork',
  'tenant_progress',
  'tenant_resource',
  'tenant_reward',
  'tenant_intake',
  'tenant_faq',
  'tenant_task',
  'tenant_dashboard',
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

MIDDLEWARE_CLASSES = [
    'django_tenants.middleware.TenantMiddleware',                  # Third Party
    'htmlmin.middleware.HtmlMinifyMiddleware',                     # Third Party
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'foundation_public.middleware.BanEnforcingMiddleware',         # Custom
    'foundation_tenant.middleware.TenantMeMiddleware',             # Custom
    'smegurus.middleware.SMEGurusTokenMiddleware',                 # Custom
    'htmlmin.middleware.MarkRequestMiddleware',                    # Third Party
]

ROOT_URLCONF = 'smegurus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'smegurus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        "NAME": env_var("DB_NAME"),
        "USER": env_var("DB_USER"),
        "PASSWORD": env_var("DB_PASSWORD"),
        "HOST": env_var("DB_HOST"),
        "PORT": env_var("DB_PORT"),
    }
}

DATABASE_ROUTERS = (
  'django_tenants.routers.TenantSyncRouter',
)

TENANT_MODEL = "foundation_public.PublicOrganization" # app.Model

TENANT_DOMAIN_MODEL = "foundation_public.PublicDomain"  # app.Model

TENANT_LIMIT_SET_CALLS = True


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

if env_var("IS_DEBUG"):
    """If doing dev work, run a less secure hasher to speed up unit tests."""
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ugettext = lambda s: s
LANGUAGES = (
    ('en', ugettext('English')),
#    ('fr', ugettext('French')),
#    ('es', ugettext('Spanish')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)


# Email
#

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = env_var("MAILGUN_ACCESS_KEY")
MAILGUN_SERVER_NAME = env_var("MAILGUN_SERVER_NAME")
DEFAULT_FROM_EMAIL = env_var("DEFAULT_FROM_EMAIL")
DEFAULT_TO_EMAIL = env_var("DEFAULT_TO_EMAIL")


# Amazon S3 Service
# http://django-storages.readthedocs.org/en/latest/index.html

AWS_STORAGE_BUCKET_NAME = env_var("AWS_STORAGE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = env_var("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env_var("AWS_SECRET_ACCESS_KEY")
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'smegurus.s3utils.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'smegurus.s3utils.MediaStorage'

MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)


# Django-Compressor
# http://django-compressor.readthedocs.org/en/latest/settings/

COMPRESS_ENABLED = env_var("COMPRESS_ENABLED")
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.rCSSMinFilter',]
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']


# Django-Compressor + Django-Storages
#

COMPRESS_STORAGE = 'smegurus.s3utils.CachedS3BotoStorage'


# django-htmlmin
# https://github.com/cobrateam/django-htmlmin

HTML_MINIFY = env_var("HTML_MINIFY")
KEEP_COMMENTS_ON_MINIFYING = env_var("KEEP_COMMENTS_ON_MINIFYING")


# Django-REST-Framework
#

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.AdminRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}


# Custom authentication
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/

AUTHENTICATION_BACKENDS = (
    'smegurus.backends.UserModelEmailBackend',
    'django.contrib.auth.backends.ModelBackend',
 )
