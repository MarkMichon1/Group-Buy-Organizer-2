"""
Django settings for gb project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from django.core.exceptions import ImproperlyConfigured

import json
import os

# Load JSON Config Secrets
from gb.secrets import config_dict


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY
SECRET_KEY = config_dict['SECRET_KEY']
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'pyrogroupbuys.com', 'www.pyrogroupbuys.com']
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True

# Application definition
INSTALLED_APPS = [
    'captcha',
    'crispy_forms',
    'google_analytics',
    'mathfilters',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'events',
    'fireworks',
    'forum',
    'general',
    'groupbuys',
    'knowledgebase',
    'marketplace',
    'personal_messages',
    'staff',
    'storefinder',
    'users'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
    #'general.middleware.view_count_middleware' #IMPORTANT- may have to be commented out until Instance is initialized.
]

ROOT_URLCONF = 'gb.urls'

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

WSGI_APPLICATION = 'gb.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': config_dict['DB_ENGINE'],
        'NAME': config_dict['DB_NAME'],
        'USER': config_dict['DB_USER'],
        'PASSWORD': config_dict['DB_PASSWORD'],
        'HOST': config_dict['DB_HOST'],
        'PORT': config_dict['DB_PORT']
    }
}

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ['users.backend.EmailBackend']


# Password validation
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

SITE_ID = 1

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Misc
LOGOUT_REDIRECT_URL = 'general-home'
LOGIN_REDIRECT_URL = 'general-home'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config_dict['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config_dict['EMAIL_HOST_PASSWORD']

# Off Site Analytics
GOOGLE_ANALYTICS = {
    'google_analytics_id': config_dict['SECRET_KEY'],
}

# Captcha
RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI" #these are Google test keys, not private
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error'] #remove

RECAPTCHA_REQUIRED_SCORE = 0.2
# RECAPTCHA_PUBLIC_KEY = config_dict['RECAPTCHA_PUBLIC_KEY']
# RECAPTCHA_PRIVATE_KEY = config_dict['RECAPTCHA_PRIVATE_KEY']