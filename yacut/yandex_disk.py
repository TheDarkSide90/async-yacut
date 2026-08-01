import os
import aiohttp
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv

import settings


load_dotenv()

DISK_TOKEN = os.getenv('DISK_TOKEN')
AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}


async def get_upload_url(filename):
    async with aiohttp.ClientSession(headers=AUTH_HEADERS) as session:
        suffix = Path(filename).suffix
        disk_path = f"app:/{uuid4().hex}{suffix}"
        async with session.get(
            settings.REQUEST_UPLOAD_URL,
            params={
                "path": disk_path,
                "overwrite": "true"
            }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data["href"], disk_path


async def upload_file(file, filename):
    upload_url, disk_path = await get_upload_url(filename)

    file.stream.seek(0)
    file_data = file.stream.read()

    async with aiohttp.ClientSession() as session:
        async with session.put(
            upload_url,
            data=file_data
        ) as response:
            response.raise_for_status()
            return disk_path


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
