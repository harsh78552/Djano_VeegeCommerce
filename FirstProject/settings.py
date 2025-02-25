from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

from django.conf.global_settings import MEDIA_URL, STATICFILES_DIRS, CSRF_TRUSTED_ORIGINS

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# load our environment variable
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r+t@kl)9ofvptcc1xwxe)x*dsm$(!)-5xcwy1a1uayf$jrq%wr'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['tclip-production-5c82.up.railway.app', 'https://tclip-production-5c82.up.railway.app']
CSRF_TRUSTED_ORIGINS = ['https://tclip-production-5c82.up.railway.app']
# Replace 'HOME' with your actual app name


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'HOME',
	'cart',
	'payment',
	'whitenoise.runserver_nostatic'
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'FirstProject.urls'

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
				'HOME.context_processors.categories',
				'cart.context_processors.cart',
			],
		},
	},
]

WSGI_APPLICATION = 'FirstProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
	'default': {
		# 'ENGINE': 'django.db.backends.sqlite3',
		# 'NAME': BASE_DIR / 'db.sqlite3',
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'railway',
		'USER': 'postgres',
		'PASSWORD': os.environ['PASSWORD_YO'],
		'HOST': 'centerbeam.proxy.rlwy.net',
		'PORT': '57204'

	}
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True

USE_I18N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

import os

# URL to access static files
STATIC_URL = '/static/'

# Tell Django where to find static files
STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static"),
]
# whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
