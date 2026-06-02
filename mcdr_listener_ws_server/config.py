import shutil
from pathlib import Path

from mcdreforged.api.all import PluginServerInterface, Serializable


class ImageHostEntry(Serializable):
    host: str
    proxy: str = ""


class PluginConfig(Serializable):
    # WebSocket listen address
    host: str = "0.0.0.0"

    # WebSocket listen port
    port: int = 60601

    # WebSocket connection token, empty string means no verification
    ws_token: str = ""

    # Enable remote command execution
    enable_remote_exec_command: bool = False

    # Allowed command prefixes, empty list means no restriction
    remote_exec_command_whitelist: list[str] = []

    # Command execution timeout in seconds
    remote_exec_command_timeout_sec: int = 10

    # Maximum length of command result
    remote_exec_result_max_length: int = 4000

    # Image cache directory, relative or absolute
    cache_dir: str = "./cache/mcdr_listener_ws_server/images/"

    # Maximum side length of rendered images
    image_max_side_length: int = 64

    # How long rendered images stay in the world
    image_duration_sec: int = 10

    # How long cached images stay on disk, in seconds
    image_cache_ttl_sec: int = 180

    # Allowed image hosts, each entry can optionally specify a proxy for that host
    image_host_whitelist: list[ImageHostEntry] = [
        ImageHostEntry(host="multimedia.nt.qq.com.cn"),
        ImageHostEntry(host="gxh.vip.qq.com"),
        ImageHostEntry(host="cdn.discordapp.com", proxy="http://127.0.0.1:7890"),
        ImageHostEntry(host="media.discordapp.net", proxy="http://127.0.0.1:7890"),
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
