import string

import os

REGEX = r'^[A-Za-z0-9]+$'
CHARS = string.ascii_letters + string.digits
CUSTOM_ID_MAX_LENGTH = 16
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