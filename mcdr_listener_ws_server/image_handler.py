"""图片处理模块 - 下载、转换、展示图片"""

import time
from typing import Any
from urllib.parse import urlparse
from mcdreforged.api.all import *

from .image_cache import ImageCache
from .image_message import replace_image_markers
from .image_renderer import ImageRenderer
from .translator import tr


class ImageHandler:
    """处理图片下载、转换和展示"""

    def __init__(
        self,
        server: PluginServerInterface,
        cache_dir="./cache/mcdr_listener_ws_server/images/",
        image_max_side_length: int = 64,
        image_duration_sec: int = 10,
        image_cache_ttl_sec: int = 180,
        image_host_whitelist: list[Any] | None = None,
        view_image_cooldown_ms: int = 5555,
    ):
        self.server = server
        self.cache_dir = cache_dir
        self.image_max_side_length = image_max_side_length
        self.image_duration_sec = image_duration_sec
        self.image_cache_ttl_sec = image_cache_ttl_sec
        self.pending_images = {}  # {player_name: {idx: image_data}}
        self.view_image_cooldown_ms = view_image_cooldown_ms
        self._last_view_image_time: float = 0.0
        self.image_cache = ImageCache(
            server,
            cache_dir,
            ttl_sec=image_cache_ttl_sec,
            host_whitelist=image_host_whitelist,
        )
        self.image_renderer = ImageRenderer(
            server,
            image_max_side_length=image_max_side_length,
            image_duration_sec=image_duration_sec,
        )

    def _make_image_blocked_message(self, host: str) -> RTextBase:
        return RTextList(
            RText("[", RColor.dark_red),
            RText("Blocked", RColor.red, RStyle.bold),
            RText("] ", RColor.dark_red),
            tr(self.server, "image.blocked_by_whitelist_prefix").set_color(RColor.red),
            RText(host, RColor.gold, RStyle.bold),
        )

    def process_message_with_images(
        self, message: str, images: list, player_name: str
    ) -> str:
        if not images:
            return message

        if player_name not in self.pending_images:
            self.pending_images[player_name] = {}

        for img_info in images:
            idx = img_info.get("idx", 0)
            url = img_info.get("url", "")
            self.pending_images[player_name][idx] = {
                "url": url,
                "summary": img_info.get(
                    "summary", str(tr(self.server, "image.default_summary"))
                ),
            }

        # 图片标记的实际替换在发送阶段统一处理
        return message

    def register_image(
        self, player_name: str, idx: int, url: str, summary: str = "图片"
    ):
        """
        为玩家注册图片信息

        Args:
            player_name: 玩家名称
            idx: 图片索引
            url: 图片URL
            summary: 图片描述
        """
        if player_name not in self.pending_images:
            self.pending_images[player_name] = {}

        self.pending_images[player_name][idx] = {"url": url, "summary": summary}
        self.server.logger.info(
            f"【 Image registered 】 {player_name} #{idx}: {url[:50]}..."
        )

    def replace_image_markers(self, message: str, images: list) -> str:
        return replace_image_markers(self.server, message, images)

    def view_image(self, player_name: str, url: str):
        """
        玩家点击查看图片

        Args:
            player_name: 玩家名称
            url: 图片URL
        """

        now = time.time()
        elapsed_ms = (now - self._last_view_image_time) * 1000
        if elapsed_ms < self.view_image_cooldown_ms:
            remaining = self.view_image_cooldown_ms - elapsed_ms
            cd_msg = RTextList(
                RText("[", RColor.dark_red),
                RText("CD", RColor.red, RStyle.bold),
                RText("] ", RColor.dark_red),
                tr(
                    self.server, "image.cooldown", remaining=f"{remaining / 1000:.2f}"
                ).set_color(RColor.gold),
            )
            self.server.tell(player_name, cd_msg)
            return
        self._last_view_image_time = now

        # 发送加载提示
        self.server.tell(player_name, tr(self.server, "image.loading"))
        self.server.logger.info(f"【 Image request 】 {player_name}: {url}")

        # 异步下载和展示图片
        def download_and_display():
            try:
                # 下载图片
                image_data = self.download_image(url)
                if not image_data:
                    self.server.tell(
                        player_name, tr(self.server, "image.download_failed")
                    )
                    return

                image = self.image_renderer.open_image(image_data)
                if self.image_renderer.last_open_was_animated:
                    self.server.tell(
                        player_name, tr(self.server, "image.gif_first_frame")
                    )
                self.image_renderer.display_image_to_player(player_name, image)

            except Exception as e:
                self.server.logger.error(
                    f"【 Image error 】 failed to process image: {e}"
                )
                import traceback

                self.server.logger.error(traceback.format_exc())
                if isinstance(
                    e, ValueError
                ) and "Image host is not in whitelist:" in str(e):
                    host = urlparse(url).hostname or "unknown"
                    self.server.tell(
                        player_name, self._make_image_blocked_message(host)
                    )
                else:
                    self.server.tell(
                        player_name,
                        tr(self.server, "image.process_failed", error=str(e)),
                    )

        # 在新线程中执行
        import threading

        threading.Thread(target=download_and_display, daemon=True).start()

    def download_image(self, url: str, timeout=10) -> bytes:
        return self.image_cache.download_image(url, timeout=timeout)
