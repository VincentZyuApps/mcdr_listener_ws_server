import hashlib
import os
import time
from typing import Any
from urllib.parse import urlparse

import requests
from mcdreforged.api.all import PluginServerInterface


class ImageCache:
    def __init__(
        self,
        server: PluginServerInterface,
        cache_dir: str,
        ttl_sec: int = 180,
        host_whitelist: list[Any] | None = None,
    ):
        self.server = server
        self.cache_dir = cache_dir
        self.ttl_sec = ttl_sec
        self.host_map: dict[str, str] = {}  # hostname -> proxy_url (empty = direct)
        self._build_host_map(host_whitelist or [])

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            server.logger.info(
                f"【-- Image cache --】 created cache directory: {cache_dir}"
            )

    def _build_host_map(self, whitelist: list[Any]) -> None:
        for entry in whitelist:
            if isinstance(entry, str):
                host = entry.lower()
                self.host_map[host] = ""
            elif isinstance(entry, dict):
                host = entry.get("host", "").lower()
                if host:
                    self.host_map[host] = entry.get("proxy", "") or ""
            else:
                host = getattr(entry, "host", "")
                if host:
                    self.host_map[host.lower()] = getattr(entry, "proxy", "") or ""

    def _get_proxy_for_host(self, hostname: str) -> dict[str, str] | None:
        proxy_url = self.host_map.get(hostname.lower(), None)
        if proxy_url is None:
            return None
        if not proxy_url:
            return None
        return {"http": proxy_url, "https": proxy_url}

    def cleanup_expired(self) -> None:
        if self.ttl_sec <= 0 or not os.path.isdir(self.cache_dir):
            return

        now = time.time()
        removed = 0
        for entry in os.scandir(self.cache_dir):
            if not entry.is_file():
                continue
            try:
                if now - entry.stat().st_mtime > self.ttl_sec:
                    os.remove(entry.path)
                    removed += 1
            except OSError as error:
                self.server.logger.warning(
                    f"【-- Image cache --】 failed to remove expired cache file {entry.path}: {error}"
                )
        if removed > 0:
            self.server.logger.info(
                f"【-- Image cache --】 removed {removed} expired cache file(s)"
            )

    def is_url_allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False
        return hostname.lower() in self.host_map

    def download_image(self, url: str, timeout: int = 10) -> bytes:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        if not self.is_url_allowed(url):
            raise ValueError(f"Image host is not in whitelist: {hostname}")

        self.cleanup_expired()

        cache_key = hashlib.md5(url.encode()).hexdigest()
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.jpg")

        if os.path.exists(cache_path):
            self.server.logger.info(f"【-- Image cache --】 hit cache: {cache_key}")
            with open(cache_path, "rb") as f:
                return f.read()

        proxies = self._get_proxy_for_host(hostname)
        proxy_info = f" via proxy {proxies['http']}" if proxies else " (direct)"
        self.server.logger.info(f"【-- Image download --】 {url[:100]}...{proxy_info}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
        response.raise_for_status()

        image_data = response.content
        with open(cache_path, "wb") as f:
            f.write(image_data)

        return image_data
