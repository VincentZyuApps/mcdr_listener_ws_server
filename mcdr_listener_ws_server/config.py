import shutil
from pathlib import Path

from mcdreforged.api.all import PluginServerInterface, Serializable


class PluginConfig(Serializable):
    # WebSocket listen address
    host: str = "0.0.0.0"

    # WebSocket listen port
    port: int = 60601

    # Image cache directory, relative or absolute
    cache_dir: str = "./cache/mcdr_listener_ws_server/images/"

    # Maximum side length of rendered images
    image_max_side_length: int = 64

    # How long rendered images stay in the world
    image_duration_sec: int = 10

    # How long cached images stay on disk, in seconds
    image_cache_ttl_sec: int = 180

    # Allowed image hosts
    image_host_whitelist: list[str] = [
        "multimedia.nt.qq.com.cn",
        "gxh.vip.qq.com",
        # "127.0.0.1",
    ]


_CONFIG_FILE_NAME = "config.yml"
_DEFAULT_CONFIG_BUNDLED_PATH = "resources/default_config.yml"


def _get_config_path(server: PluginServerInterface) -> Path:
    return Path(server.get_data_folder()) / _CONFIG_FILE_NAME


def _release_default_config(server: PluginServerInterface, config_path: Path) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with server.open_bundled_file(_DEFAULT_CONFIG_BUNDLED_PATH) as source:
        with config_path.open("wb") as target:
            shutil.copyfileobj(source, target)
    server.logger.info(f"【 Config 】 released default config to {config_path}")


def ensure_config_file(server: PluginServerInterface) -> Path:
    config_path = _get_config_path(server)

    if not config_path.exists():
        _release_default_config(server, config_path)

    return config_path


def load_config(server: PluginServerInterface) -> PluginConfig:
    ensure_config_file(server)
    return server.load_config_simple(_CONFIG_FILE_NAME, target_class=PluginConfig)
