from pathlib import Path
import environ

# Initialize the environment variables
env = environ.Env()

# Read the .env file into the environment
environ.Env.read_env() # Make sure this is before reading env variables

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pr$#-sy@@-gk-xojh$1@4=crvm1#e6%7umdv!194-(u*rv5k2d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auth_app', # Your custom app
    # Allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
]

# Site ID for django-allauth
SITE_ID = 1

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Redirect URLs
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Google OAuth Configuration
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', # Required for allauth
    'django.middleware.csrf.CsrfViewMiddleware', # Make sure this is here

]

# URL Configuration
ROOT_URLCONF = 'auth_project.urls'

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # Required by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'auth_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # This sets MySQL as the database backend
        'NAME': 'authentication',              # Set your MySQL database name
        'USER': 'root',                        # Your MySQL username
        'PASSWORD': 'root',                    # Your MySQL password
        'HOST': 'localhost',                   # Database host (use the appropriate IP address if needed)
        'PORT': '3306',                        # Default MySQL port (use the correct one if it's different)
    }
}

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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email backend (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Google OAuth Config from .env
GOOGLE_OAUTH_CLIENT_ID = env('GOOGLE_OAUTH_CLIENT_ID')
GOOGLE_OAUTH_CLIENT_SECRET = env('GOOGLE_OAUTH_CLIENT_SECRET')
GOOGLE_OAUTH_URL = env('GOOGLE_OAUTH_URL')

LOGIN_REDIRECT_URL = '/dashboard/'  # Ensure redirection after successful login
LOGOUT_REDIRECT_URL = '/'

# Email backend configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'patildarshana712@gmail.com'
EMAIL_HOST_PASSWORD = 'divu@031886' 
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
