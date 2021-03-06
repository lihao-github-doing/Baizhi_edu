"""
Django settings for edu_api project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 需要将修改后的子应用的目录设置为全局的导包路径
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_*pp@v9u7(g^5kmauhaaz&3&92^jc$nv+4cb152!(edv*)z4xk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    # 以后可以将域名换成真实的
    "api.baizhiedu.com"
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    # xadmin配置
    'xadmin',
    'crispy_forms',
    'reversion',
    'django_filters',

    'home',
    'user',
    "course",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'edu_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'edu_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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



LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 日志配置
LOGGING = {
    # 版本
    'version': 1,
    # 是否禁用已存在的日志器
    'disable_existing_loggers': False,
    # 格式化日志信息
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    # 日志的过滤信息
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理日志的方法
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            # 记录到文件中的日志登记
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置 日志的文件名 日志的保存目录
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/lesson_api.log"),
            # 日志的文件大小  100M
            'maxBytes': 100 * 1024 * 1024,
            # 日志的文件数量
            'backupCount': 10,
            # 日志的格式
            'formatter': 'verbose'
        },
    },
    # 日志对象
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}

# 允许跨域请求访问
CORS_ORIGIN_ALLOW_ALL = True

# DRF相关配置
REST_FRAMEWORK = {
    # 全局异常配置
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',

    # 认证方式
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

AUTH_USER_MODEL = "user.UserInfo"

# jwt相关配置
JWT_AUTH = {

    # token的有效时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3000),

    # jwt返回数据的格式
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'user.service.jwt_response_payload_handler',
}

# 自定义多条件登录
AUTHENTICATION_BACKENDS = [
    'user.service.UserAuthentication',
]# redis相关配置
CACHES = {
    # 默认库
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 验证码储存位置
    "sms_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

CKEDITOR_UPLOAD_PATH = ''  # 使用fdfs分布系统
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 完整工具条
        'height': 300,  # 编辑高度
        'width': 1000
    },
    # 'default': {
    #     'toolbar': 'Custom',
    #     'toolbar_Custom': [
    #         ['Bold', 'Italic', 'Underline'],
    #         ['NumberedList', 'BulletedList', '-', 'table', 'image2', 'Outdent', 'Indent',
    #          '-', 'JustifyLeft', 'JustifyCenter',
    #          'JustifyRight', 'JustifyBlock'],
    #         ['Link', 'Unlink'],
    #         ['RemoveFormat', 'Source']
    #     ]
    # }
}
# 支付宝配置信息
ALIAPY_CONFIG = {
    # "gateway_url": "https://openapi.alipay.com/gateway.do?", # 真实支付宝网关地址
    "gateway_url": "https://openapi.alipaydev.com/gateway.do?",  # 沙箱支付宝网关地址
    "appid": "2016102200738366",
    "app_notify_url": None,
    "app_private_key_path": open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read(),
    "alipay_public_key_path": open(os.path.join(BASE_DIR, "apps/payments/keys/alipay_public_key.pem")).read(),
    "sign_type": "RSA2",
    "debug": False,
    "return_url": "http://localhost:8080/result",  # 同步回调地址
    "notify_url": "http://api.baizhiedu.com:8000/payments/result",  # 异步结果通知
}
