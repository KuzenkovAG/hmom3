import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DEBUG').lower() == 'true'

ALLOWED_HOSTS = [
    'www.momonline.pythonanywhere.com',
    'momonline.pythonanywhere.com',
    '127.0.0.1:8000',
    '127.0.0.1',
    'localhost',
    '158.181.139.38',
]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'apps.towns.apps.TownsConfig',
    'apps.users.apps.UsersConfig',
    'apps.core.apps.CoreConfig',
    'apps.stats.apps.StatsConfig',
    'apps.about.apps.AboutConfig',
    'apps.market.apps.MarketConfig',
    'apps.webhooks.apps.WebhooksConfig'
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda x: DEBUG,
}

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'hmom3.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'hmom3.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# ToDo: It's commented for simple password. After development uncomment it.
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Internationalization
LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATIC_ROOT = os.path.join('/home/momonline/static/')

# Login
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'towns:index'
LOGOUT_REDIRECT_URL = 'users:login'


"""Game balance settings."""
# Resources
DEF_GOLD_AMOUNT = 1000
DEF_WOOD_AMOUNT = 25
DEF_STONE_AMOUNT = 25
DEF_GOLD_INCOME = 50
DEF_WOOD_INCOME = 3
DEF_STONE_INCOME = 3
DEF_GOLD_LIMIT = 1000
DEF_STONE_LIMIT = 300
DEF_WOOD_LIMIT = 300

# Change icon depend on building level
CHANGE_IMAGE_PER_LEVEL = 5  # image of building will change each this level
BUILDINGS_WITH_CHANGE_IMAGE = {
    'castle': lambda lvl: 2 if lvl > 10 else lvl // CHANGE_IMAGE_PER_LEVEL,
    'hall': lambda lvl: 3 if lvl > 15 else lvl // CHANGE_IMAGE_PER_LEVEL,
    'mage': lambda lvl: 3 if lvl > 15 else lvl // CHANGE_IMAGE_PER_LEVEL,
}

# trade coefficients
GOLD_PER_WOOD = 50
GOLD_PEF_STONE = 50
WOOD_PER_GOLD = 150
STONE_PER_GOLD = 150
WOOD_PER_STONE = 10
STONE_PER_WOOD = 10
