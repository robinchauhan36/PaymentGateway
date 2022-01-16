import os

from payment_gateway.settings import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'payment_gateway',
        'USER': 'payment_gateway_user',
        'PASSWORD': 'Password@123',
        'HOST': '127.0.0.1',
        'PORT': '',
        # 'OPTIONS': {
        #     'autocommit': True,
        # },
        # 'TEST': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # },
    }
}