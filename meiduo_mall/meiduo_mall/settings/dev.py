"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8%wixw@#jfl0*&yo)nfl(#h$2rh*b$&0r9bb=7n@u(e7ypy4rn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.meiduo.site']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.users',
    'apps.contents',
    'apps.verifications',
    'apps.oauth',
    'apps.areas',
    'apps.goods',
    'apps.carts',
    'apps.orders',
    'apps.payment',
    'apps.meiduo_admin',
    'rest_framework',
    'corsheaders',

    'django_crontab',  # 定时任务
]

MIDDLEWARE = [
    # 跨域必须为第一
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',  # 1.jinja2模板引擎
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 2.模本文件夹路径
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 3.加载Jinja2模板引擎环境
            'environment': 'utils.jinja2_env.jinja2_environment',
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# MySQL读写不分离
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'tao',  # 数据库用户名
        'PASSWORD': '123456',  # 数据库用户密码
        'NAME': 'meiduo'  # 数据库名字
    },
}

# 实现MySQL读写分离 增加slave数据库的配置
# DATABASES = {
#     'default': {  # 写（主机）
#         'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
#         'HOST': '127.0.0.1',  # 数据库主机
#         'PORT': 3306,  # 数据库端口
#         'USER': 'root',  # 数据库用户名
#         'PASSWORD': 'mysql',  # 数据库用户密码
#         'NAME': 'meiduo'  # 数据库名字
#     },
#     'slave': { # 读（从机）
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST': '127.0.0.1',
#         'PORT': 8306,
#         'USER': 'root',
#         'PASSWORD': 'mysql',
#         'NAME': 'meiduo'
#     }
# }
# DATABASE_ROUTERS = ['utils.db_router.MasterSlaveDBRouter']

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
# 静态文件的路径
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

CACHES = {
    # 0
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 1
    "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 2
    "verify_image_code": {  # 保存图片验证码--2号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 3
    "sms_code": {  # 保存短信验证码--3号库
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/3",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    # 4
    "history": {  # 用户浏览记录--4号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 5
    "carts": {  # 购物车数据--5号
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/5",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },

}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# 日志文件
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/meiduo.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }

}
# 实例化日志对象
# 单例的设计模式：在整个运行项目中，有且只有一个 内存空间
import logging
logger = logging.getLogger('django')

# 自定义用户模型
AUTH_USER_MODEL = 'users.User'

# 配置自定义用户认证后端
AUTHENTICATION_BACKENDS = ['apps.users.utils.UsernameMobileAuthBackend']

# 重定向登陆路由
LOGIN_URL = '/login/'

# QQ登录参数
QQ_CLIENT_ID = '101518219'
QQ_CLIENT_SECRET = '418d84ebdc7241efb79536886ae95224'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8000/oauth_callback'

# 微博登陆参数
APP_KEY = '3305669385'
APP_SECRET = '74c7bea69d5fc64f5c3b80c802325276'
REDIRECT_URL = 'http://www.meiduo.site:8000/sina_callback'

# 配置邮件服务器
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 指定邮件后端
EMAIL_HOST = 'smtp.163.com'  # 发邮件主机
EMAIL_PORT = 25  # 发邮件端口
EMAIL_HOST_USER = 'hmmeiduo@163.com'  # 授权的邮箱
EMAIL_HOST_PASSWORD = 'hmmeiduo123'  # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = '美多商城<hmmeiduo@163.com>'  # 发件人抬头
EMAIL_ACTIVE_URL = 'http://www.meiduo.site:8000/emails/verification/'  # 激活地址

# 指定自定义的Django文件存储类
DEFAULT_FILE_STORAGE = 'utils.fastdfs.fastdfs_storage.FastDFSStorage'

# FastDFS相关参数
# FDFS_BASE_URL = 'http://172.16.211.129:8888/'
FDFS_BASE_URL = 'http://image.meiduo.site:8888/'

# 支付宝SDK配置参数
ALIPAY_APPID = '2016101400686577'  # 写自己的appid
ALIPAY_DEBUG = True
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'
ALIPAY_RETURN_URL = 'http://www.meiduo.site:8000/payment/status/'

# 定时任务
CRONJOBS = [
    # 每1分钟生成一次首页静态文件
    ('*/5 * * * *', 'apps.contents.crons.generate_static_index_html', '>> ' + os.path.join(BASE_DIR, 'logs/crontab.log'))
]
# 在定时任务中，如果出现非英文字符，会出现字符异常错误
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'

# CORS 添加白名单
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://www.meiduo.site:8080',
    'http://api.meiduo.site:8000',
)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (  # 身份验证的方式
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # jwt
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
}

# jwt 配置
import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
}
