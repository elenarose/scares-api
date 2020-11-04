"""Load config from environment variables."""
from os import environ

class Config:
    # Database config
    PG_HOST = environ.get('DATABASE_HOST','localhost')
    PG_USER = environ.get('DATABASE_USERNAME','postgres')
    PG_PASSWORD = environ.get('DATABASE_PASSWORD','postgres')
    PG_PORT = environ.get('DATABASE_PORT','5432')
    PG_NAME = environ.get('DATABASE_NAME','scares')

    AUTH_TOKEN = environ.get('SCARES_AUTH')