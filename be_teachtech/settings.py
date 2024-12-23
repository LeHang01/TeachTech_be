# settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')

# Load environment variables from the corresponding .env file
dotenv_path = f'.env.{ENVIRONMENT}'
load_dotenv(dotenv_path=dotenv_path)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'images/')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#9wwkd9ru@n6su4=2*_v*klytr95()p!hx$ff^wuh4-qm08!4+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'app',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'be_teachtech.urls'

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

WSGI_APPLICATION = 'be_teachtech.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_NAME', 'teachtechdb'),  # Sửa tên cơ sở dữ liệu nếu cần
        'USER': os.environ.get('POSTGRES_USER', 'admin'),  # Đảm bảo đúng người dùng
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'Admin123'),  # Sửa mật khẩu
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5433'),  # Đảm bảo đúng cổng nếu bạn sử dụng cổng 5433
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'vi'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'app.User'

ZALOPAY_CONFIG = {
    "APP_ID": 2553,
    "KEY1": "PcY4iZIKFCIdgZvA6ueMcMHHUbRLYjPL",
    "KEY2": "kLtgPl8HHhfvMuDHPwKfgfsY4Ydm9eIz",
    "CREATE_ENDPOINT": "https://sb-openapi.zalopay.vn/v2/create",
    "STATUS_ENDPOINT": "https://sb-openapi.zalopay.vn/v2/query",
}


JAZZMIN_SETTINGS = {
    "site_title": "My Admin",
    "site_header": "My Admin",
    "site_brand": "My Admin",
    "welcome_sign": "Welcome to My Admin",
    "copyright": "Your Company Name",
    "search_model": "auth.User",
    "icons": {
        "auth": "fas fa-users",
        "contenttypes": "fas fa-tags",
        # Thêm các biểu tượng khác nếu cần
    },
    "topmenu_links": [
        {"name": "Site", "url": "http://example.com", "icon": "fas fa-home", "new_window": True},
        {"name": "Documentation", "url": "https://docs.djangoproject.com/en/stable/", "icon": "fas fa-book", "new_window": True},
    ],
}
# Celery Config
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', '')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', '')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# MongoDB Config
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://admin:Admin123@localhost:27017/')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'teach-tech')

# Pusher Config
PUSHER_APP_ID = os.environ.get('PUSHER_APP_ID', '')
PUSHER_KEY = os.environ.get('PUSHER_KEY', '')
PUSHER_SECRET = os.environ.get('PUSHER_SECRET', '')
PUSHER_CLUSTER = os.environ.get('PUSHER_CLUSTER', '')

# MinIO / S3 configuration
AWS_ACCESS_KEY_ID = 'U0lWJXs1CUEFEG3rEJJ2'
AWS_SECRET_ACCESS_KEY = 'sC9Hs6JpbcI1NN7NSAfJOvKgLMhY8outZUYyWFgN'
AWS_STORAGE_BUCKET_NAME = 'teachtech-bucket'
AWS_S3_ENDPOINT_URL = 'http://localhost:9000'  # MinIO's endpoint
AWS_S3_REGION_NAME = 'us-east-1'  # MinIO region
AWS_S3_SIGNATURE_VERSION = 's3v4'




