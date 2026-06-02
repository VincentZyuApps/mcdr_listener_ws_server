from mcdreforged.api.all import *

from . import ws_server
from .commands import register_commands, register_help_messages
from .config import load_config
from .events import on_info as handle_info_event
from .events import on_player_joined as handle_player_joined_event
from .events import on_player_left as handle_player_left_event
from .events import on_user_info as handle_user_info_event
from .log_utils import PlayerLogger, ServerStatusLogger
from .image_handler import ImageHandler

ws_handler = None
image_handler = None

plugin_config = None
player_logger = None
server_status_logger = None


def on_load(server: PluginServerInterface, old_module):
    """Plugin loaded"""

    global plugin_config, player_logger, server_status_logger, image_handler
    plugin_config = load_config(server)
    player_logger = PlayerLogger(server)
    # server_status_logger = ServerStatusLogger(server)

    image_handler = ImageHandler(
        server,
        cache_dir=plugin_config.cache_dir,
        image_max_side_length=plugin_config.image_max_side_length,
        image_duration_sec=plugin_config.image_duration_sec,
        image_cache_ttl_sec=plugin_config.image_cache_ttl_sec,
        image_host_whitelist=plugin_config.image_host_whitelist,
    )

    global ws_handler
    ws_handler = ws_server.WebSocketHandler(
        server,
        image_handler,
        host=plugin_config.host,
        port=plugin_config.port,
        ws_token=plugin_config.ws_token,
        enable_remote_exec_command=plugin_config.enable_remote_exec_command,
        remote_exec_command_whitelist=plugin_config.remote_exec_command_whitelist,
        remote_exec_command_timeout_sec=plugin_config.remote_exec_command_timeout_sec,
        remote_exec_result_max_length=plugin_config.remote_exec_result_max_length,
        strip_message_whitespace=plugin_config.strip_message_whitespace,
    )
    ws_handler.start()

    register_commands(server, image_handler)
    register_help_messages(server)

    # server.register_event_listener(
    #     "mcdr.user_info",
    #     on_user_info,
    #     priority=500
    # )


def on_unload(server: PluginServerInterface):
    """
    Do some clean up when your plugin is being unloaded. Note that it might be a reload
    """
    server.logger.info("【 Plugin unloading 】")

    global ws_handler
    if ws_handler is not None:
        ws_handler.stop()


def on_info(server: PluginServerInterface, info: Info):
    handle_info_event(server, info)


def on_user_info(server: PluginServerInterface, info: Info):
    handle_user_info_event(server, info, ws_handler)


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    handle_player_joined_event(server, player, info, ws_handler, player_logger)


def on_player_left(server: PluginServerInterface, player: str):
    handle_player_left_event(server, player, ws_handler, player_logger)


def on_server_start(server: PluginServerInterface):
    """
    When the server begins to start
    """
    server.logger.info("【 Server start event 】")


def on_server_startup(server: PluginServerInterface):
    """
    When the server is fully startup
    """
    server.logger.info("【 Server startup done 】")


def on_server_stop(server: PluginServerInterface, return_code: int):
    """
    When the server process is stopped, go do some clean up
    If the server is not stopped by a plugin, this is the only chance for plugins to restart the server, otherwise MCDR
    will exit too
    """
    server.logger.info("【 Server stopped 】 return code = {}".format(return_code))


def on_mcdr_start(server: PluginServerInterface):
    """
    When MCDR just launched
    """
    server.logger.info("【 MCDR start event 】")


def on_mcdr_stop(server: PluginServerInterface):
    """
    When MCDR is about to stop, go do some clean up
    MCDR will wait until all on_mcdr_stop event call are finished before exiting
    """
    server.logger.info("【 MCDR stop event 】")
