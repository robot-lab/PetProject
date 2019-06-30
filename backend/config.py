import os


class DevelopmentTemplate(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    MONGO_URI = ""


class ProductionTemplate(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    MONGO_URI = ""


try:
    from backend.local_config import Production, Development
except Exception:
    pass

app_config = {
    'development': Development,
    'production': Production,
}