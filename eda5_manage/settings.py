"""
Django settings for eda5_manage project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#BASE_DIR = '/home/eda5/public/eda5_org/eda5_manage'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$b0+p#1icsm41_)i+jcto7f_h^*@rkl#-g#(0z%!q1nb!c834v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False 

TEMPLATE_DEBUG = False 

ALLOWED_HOSTS = [
	'interview.eda5.org',
        'interview.dev.dsm'
]


# Application definition

INSTALLED_APPS = (
#    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    # 'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
#    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'api_auth',
    'tokenapi',
    'api'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'api_auth.middleware.WebTokenMiddleware',
#    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'eda5_manage.urls'

WSGI_APPLICATION = 'eda5_manage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/dashboard/django-static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
		os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = BASE_DIR+'/public/django-static'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)



TEMPLATE_DIRS = (
	BASE_DIR + '/templates',
)


AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'tokenapi.backends.TokenBackend',
)

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
	'localhost',
	'google.com',
)

# LOGGING_CONFIG = None

LOGGING = {
    'version': 1,
    # 'disable_existing_loggers': True,

    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)s %(levelname)s %(pathname)s %(lineno)d %(message)s',
        }
    },
    'handlers': {
        'django_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/jc/dsm/log/requests.log',
            'formatter': 'verbose'
        },
        'sql_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/jc/dsm/log/sql.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.db':{
            'handlers': ['sql_file'],
            'level': 'INFO',
            'propagate': False
        },
        'django': {
            'handlers': ['django_file'],
            'level': 'INFO',
            'propagate': False
        },
        'eda5': {
            'handlers': ['django_file'],
            'level': 'INFO',
            'propagate': False
        },

    }
}

TIMEOUT = 60

NOTEBOOK_ARGUMENTS = [
    '--ip=0.0.0.0'
]
