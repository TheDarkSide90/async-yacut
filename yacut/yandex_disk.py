import os
import aiohttp
import urllib
from dotenv import load_dotenv

import settings


load_dotenv()

DISK_TOKEN = os.getenv('DISK_TOKEN')
AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}


async def get_upload_url(filename):
    async with aiohttp.ClientSession(headers=AUTH_HEADERS) as session:
        async with session.get(
            settings.REQUEST_UPLOAD_URL,
            params={
                "path": f"app: /{filename}",
                "overwrite": "true"
            }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data["href"]


async def upload_file(file, filename):
    upload_url = await get_upload_url(filename)

    file.stream.seek(0)
    file_data = file.stream.read()

    async with aiohttp.ClientSession() as session:
        async with session.put(
            upload_url,
            data=file_data
        ) as response:
            response.raise_for_status()
            location = response.headers['Location']
            location = urllib.parse.unquote(location)
            location = location.replace('/disk', '')
            return location


async def get_download_link(path):
    async with aiohttp.ClientSession(headers=AUTH_HEADERS) as session:
        async with session.get(
            settings.DOWNLOAD_LINK_URL,
            params={
                "path": path,
                "fields": "href"
            }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data["href"]
