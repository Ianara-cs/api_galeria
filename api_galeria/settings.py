from pathlib import Path
from datetime import timedelta
import firebase_admin
from firebase_admin import credentials
from dj_database_url import config
import os
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'), overwrite=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get_value('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.get_value('DEBUG')

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])


# Application definition

THIRD_PACKAGES = [
    'rest_framework',
    'rest_framework_simplejwt',
    #'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'corsheaders',
]

APPS_CUSTOM = [
    'apps.autenticacao',
    'apps.core'
]

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = DEFAULT_APPS + APPS_CUSTOM + THIRD_PACKAGES

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_galeria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api_galeria.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.get_value('POSTGRES_DB'),
        'USER': env.get_value('POSTGRES_USER'),
        'PASSWORD': env.get_value('POSTGRES_PASSWORD'),
        'HOST': env.get_value('POSTGRES_HOST'),
        'PORT': env.get_value('POSTGRES_PORT'),
    }
}"""

if env('DEBUG'):
    DATABASES = {
        env('DB_ALIAS'): {
            'ENGINE': env('DB_ENGINE'),
            'NAME': env('DB_NAME'),
            'USER': env("DB_USER"),
            'PASSWORD': env("DB_PASSWORD"),
            'HOST': env("DB_HOST"),
        },
    }
else:
    DATABASES = {
        'default': config(
            default=env.get_value('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=False  # deixe False localmente, True na Railway
        )
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


SIMPLE_JWT = {
    #'BLACKLIST_AFTER_ROTATION': True,
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
}

CORS_ALLOW_ALL_ORIGINS = True

USE_FIREBASE_STORAGE = env.get_value('USE_FIREBASE_STORAGE')

#FIREBASE
FIREBASE_BUCKET_NAME = env.get_value('BUCKET_NAME')
FIREBASE_JSON = env.get_value('FIREBASE_CREDENTIAL_JSON')


firebase_dict = {
    "type": env.get_value("FIREBASE_TYPE"),
    "project_id": env.get_value("FIREBASE_PROJECT_ID"),
    "private_key_id": env.get_value("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": env.get_value("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": env.get_value("FIREBASE_CLIENT_EMAIL"),
    "client_id": env.get_value("FIREBASE_CLIENT_ID"),
    "auth_uri": env.get_value("FIREBASE_AUTH_URI"),
    "token_uri": env.get_value("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": env.get_value("FIREBASE_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": env.get_value("FIREBASE_CLIENT_CERT_URL"),
    "universe_domain": env.get_value("FIREBASE_UNIVERSE_DOMAIN"),
}

# Inicializar Firebase
if USE_FIREBASE_STORAGE and not firebase_admin._apps:
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred, {
        'storageBucket': FIREBASE_BUCKET_NAME
    })