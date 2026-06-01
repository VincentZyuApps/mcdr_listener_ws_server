import hashlib
import os
from urllib.parse import urlparse

import requests
from mcdreforged.api.all import PluginServerInterface


class ImageCache:
    def __init__(self, server: PluginServerInterface, cache_dir: str, host_whitelist: list[str] | None = None):
        self.server = server
        self.cache_dir = cache_dir
        self.host_whitelist = {host.lower() for host in (host_whitelist or [])}

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            server.logger.info(f'【 Image cache 】 created cache directory: {cache_dir}')

    def is_url_allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False
        return hostname.lower() in self.host_whitelist

    def download_image(self, url: str, timeout: int = 10) -> bytes:
        if not self.is_url_allowed(url):
            raise ValueError(f'Image host is not in whitelist: {urlparse(url).hostname}')

        cache_key = hashlib.md5(url.encode()).hexdigest()
        cache_path = os.path.join(self.cache_dir, f'{cache_key}.jpg')

        if os.path.exists(cache_path):
            self.server.logger.info(f'【 Image cache 】 hit cache: {cache_key}')
            with open(cache_path, 'rb') as f:
                return f.read()

        self.server.logger.info(f'【 Image download 】 {url[:100]}...')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        image_data = response.content
        with open(cache_path, 'wb') as f:
            f.write(image_data)

        return image_data
