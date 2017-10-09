"""
Django settings for myproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# SECURITY WARNING: don't run with debug turned on in production!

import os

# a setting to determine whether we are running on OpenShift
DEBUG = True
ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True
    DEBUG = False
    
if ON_OPENSHIFT:
    DJ_PROJECT_DIR = os.path.dirname(__file__)
    BASE_DIR = os.path.dirname(DJ_PROJECT_DIR)
    WSGI_DIR = os.path.dirname(BASE_DIR)
    REPO_DIR = os.path.dirname(WSGI_DIR)
    DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)
    
    LOG_DIR = os.environ.get('OPENSHIFT_LOG_DIR')
    
    LOGGING = {
      'version': 1,
      'disable_existing_loggers': False,
      'handlers': {
        'file': {
          'level': 'WARNING',
          'class': 'logging.FileHandler',
          'filename': os.path.join(LOG_DIR, 'django.log'),
        },
      },
      'loggers': {
        'django.request': {
          'handlers': ['file'],
          'level': 'WARNING',
          'propagate': True,
        },
      }
    }
    
    import sys
    sys.path.append(os.path.join(REPO_DIR, 'libs'))
    import secrets
    SECRETS = secrets.getter(os.path.join(DATA_DIR, 'secrets.json'))
    
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
    
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = SECRETS['secret_key']
    
    
    from socket import gethostname
    ALLOWED_HOSTS = [
        gethostname(), # For internal OpenShift load balancer security purposes.
        os.environ.get('OPENSHIFT_APP_DNS'), # Dynamically map to the OpenShift gear name.
        #'example.com', # First DNS alias (set up in the app)
        #'www.example.com', # Second DNS alias (set up in the app)
    ]
    
    
    # Application definition
    
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.humanize',
        'flowerpower',
        'fertilize',
        'tasks'
    )
    
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
    
    # GETTING-STARTED: change 'myproject' to your project name:
    ROOT_URLCONF = 'myproject.urls'
    
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
    
    WSGI_APPLICATION = 'myproject.wsgi.application'
    
    
    # Database
    # https://docs.djangoproject.com/en/1.8/ref/settings/#databases
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # GETTING-STARTED: change 'db.sqlite3' to your sqlite3 database:
            'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
        }
    }
    
    #CACHE
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': os.path.join(BASE_DIR, 'cache'),
        }
    }
    
    # Internationalization
    # https://docs.djangoproject.com/en/1.8/topics/i18n/
    
    LANGUAGE_CODE = 'pt_PT'
    
    TIME_ZONE = 'Europe/Lisbon'
    
    USE_I18N = True
    
    USE_L10N = True
    
    USE_TZ = True
    
    
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.8/howto/static-files/
    
    LOGIN_URL = 'login'
    LOGIN_REDIRECT_URL = '/'
    
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(WSGI_DIR, 'static')

else:

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
    
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '85lbd87k1gk72+(m9qfe9o1k4kzaf!z7@pn5lo1@mqo2yh9j!#'
    
    # SECURITY WARNING: don't run with debug turned on in production!
    
    ALLOWED_HOSTS = []
    
    
    # Application definition
    
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.humanize',
    	'flowerpower',
    	'fertilize',
    	'tasks'
    ]
    
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    ROOT_URLCONF = 'myproject.urls'
    
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
    
    
    
    WSGI_APPLICATION = 'myproject.wsgi.application'
    
    
    # Database
    # https://docs.djangoproject.com/en/1.10/ref/settings/#databases
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    
    #CACHE
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': os.path.join(BASE_DIR, 'cache'),
        }
    }
    
    
    # Password validation
    # https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
    
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
    
    LOGIN_URL = 'login'
    LOGIN_REDIRECT_URL = '/'
    
    # Internationalization
    # https://docs.djangoproject.com/en/1.10/topics/i18n/
    
    LANGUAGE_CODE = 'pt_PT'
    
    TIME_ZONE = 'Europe/Lisbon'
    
    USE_I18N = True
    
    USE_L10N = True
    
    USE_TZ = True
    

    
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.10/howto/static-files/
    
    STATIC_URL = '/static/'
    STATIC_ROOT = 'staticfiles'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )



