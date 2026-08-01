import os

SHORT_MAX_LENGTH = 16
GENERATE_SHORT_MAX_LENGTH = 6
GENERATE_RANGE = 500
API_HOST = os.getenv(
    'API_HOST',
    'https://cloud-api.yandex.net'
)
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = (
    f'{API_HOST}/{API_VERSION}/disk/resources/upload'
)
DOWNLOAD_LINK_URL = (
    f'{API_HOST}/{API_VERSION}/disk/resources/download'
)


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
