"""
Django settings for agendador project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def get_secret(secret_name):
    try:
        with open('/run/secrets/{0}'.format(secret_name), 'r') as secret_file:
            return secret_file.read()
    except IOError:
        return None

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&vn=ld^l+t0bo3r_3uy!3*6&x3x6_ppru#1lhm(gku!z+s6=kc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0','127.0.0.1', 'localhost']
INTERNAL_IPS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = (
    'material.theme.lightblue',
    'material',
    'material.frontend',
    'material.admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    #'agenda',
    'agenda.apps.AgendaConfig',
    #'django_cas_ng',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

SITE_ID = 1

CAS_SERVER_URL= 'https://sistemas.ufsc.br'
CAS_IGNORE_REFERER=True
CAS_LOGOUT_COMPLETELY=True

ROOT_URLCONF = 'agendador.urls'

WSGI_APPLICATION = 'agendador.wsgi.application'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret('agendador_name_db'),
        'USER': get_secret('agendador_user_db'),
        'PASSWORD': get_secret('agendador_password_db'),
        'HOST': 'mysql.sites.ufsc.br',
        'PORT': '3306',
    }
}

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
                ],
            },
        },
]

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

#USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

LOGIN_REDIRECT_URL = '/'

EMAIL_HOST = "smtp.sistemas.ufsc.br"
EMAIL_PORT = 465
EMAIL_HOST_USER = get_secret('agendador_email_user')
EMAIL_HOST_PASSWORD = get_secret('agendador_email_password')
EMAIL_USE_SSL = True

#Sessao agendador
SESSION_COOKIE_AGE = 43200 # 12 horas * 60 minutos * 60 segundos
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
