import os

class BaseConfig(object):
    """Base config class"""
    SECRET_KEY = 'sdoi3209jfw909jfwd09oidjfgodfgcjdoijdofijd'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/blog'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_ECHO = True


class ProductionConfig(BaseConfig):
    """Production specific config"""
    DEBUG = False
    # SECRET_KEY = open('/path/to/secret/file').read()
    SECRET_KEY = 'sldkfjwodkdnvlsksmlqoapamckdld'
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(BaseConfig):
    """Development specific config"""
    TESTING = True
    SECRET_KEY = 'cmvo30fdmd1skf8304jf0q-'
    SQLALCHEMY_ECHO = False