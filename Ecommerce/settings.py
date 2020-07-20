import os


ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'pwa',
    'django.contrib.postgres',
    'ckeditor',
    'phonenumber_field',
    'django.contrib.humanize',
    'allauth.socialaccount.providers.google',
]
SITE_ID = 1

LOGIN_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_brotli.middleware.BrotliMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'Ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static Files

# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_files')]
# STATIC_ROOT = '/home/nouman/STUDY/Project/JustDjango/django_project_boilerplate/static2/'
CKEDITOR_UPLOAD_PATH = os.path.join(BASE_DIR, 'media/ckeditor')
# STATICFILES_DIRS = [STATIC_DIR]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'd22q28ufavsb79',
    #     'USER': 'pszmxzwfagfpvq',
    #     'PASSWORD': 'b38376d2fad9429c11081fe98ed81b71650920771d2fb04b8d4ff1fe07fed17d',
    #     'HOST': 'ec2-54-246-87-132.eu-west-1.compute.amazonaws.com',
    #     'PORT': '5432',
    # }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'd5mqaeioampt9l',
    #     'USER': 'hxsefpbomubsqr',
    #     'PASSWORD': 'ad0ad9f23781136fe0db4144e8e468973278409b34003394c17285045d83610c',
    #     'HOST': 'ec2-54-234-44-238.compute-1.amazonaws.com',
    #     'PORT': '5432',
    # }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'E2',
    #     'USER': 'postgres',
    #     'PASSWORD': '112456',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # }
    # 3rd is below
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd2oa00jte90r0l',
        'USER': 'zzpowykeyckahs',
        'PASSWORD': '6499a36f36d1296009a9b3927bc948f85f2f84d99f4bf7181eef4893d4d92ce6',
        'HOST': 'ec2-52-202-66-191.compute-1.amazonaws.com',
        'PORT': '5432',
    }
    #     "default": {

    #         "ENGINE": "django.db.backends.sqlite3",
    #         "NAME": os.path.join(BASE_DIR, 'db.sqlite3')
    #     }
}

if ENVIRONMENT == 'production':
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'nouman.qurashi42544@gmail.com'
EMAIL_HOST_PASSWORD = 'eloiqtdnbgpyyqte'


ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = True

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = ''
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'None'


# Pwa Configurations
PWA_APP_NAME = 'Ecommerce Site'
PWA_APP_DESCRIPTION = "My app description"
PWA_APP_THEME_COLOR = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [{'src': '/static/images/c.png', 'sizes': '192x192'}]
PWA_APP_ICONS_APPLE = [
    {'src': '/static/images/b.png', 'sizes': '192x192'}]
PWA_APP_SPLASH_SCREEN = [{'src': '/static/images/icons/splash-640x1136.png',
                          'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'}]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
