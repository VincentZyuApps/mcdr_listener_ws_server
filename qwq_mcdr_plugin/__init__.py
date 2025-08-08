# __init__.py
import re
from mcdreforged.api.all import *

# from qwq_mcdr_plugin import qwq_lib, ws_server
from . import qwq_lib, ws_server
from .log_utils import PlayerLogger, ServerStatusLogger

ws_handler = None

# variant for functionality demo
counter = 0
# player_count = 0

player_logger = None
server_status_logger = None


def on_load(server: PluginServerInterface, old_module):
    """
	Do some clean up when your plugin is being loaded
	Like migrating data, reading config file or adding help messages
	old_module is the previous plugin instance. If the plugin is freshly loaded it will be None
	"""
    if old_module is not None:
        counter = old_module.counter + 1
    else:
        counter = 1
    msg = f'This is the {counter} time to load the plugin'
    server.logger.info(msg)
    qwq_lib.register(server)

    global player_logger, server_status_logger
    player_logger = PlayerLogger(server)
    # server_status_logger = ServerStatusLogger(server)

    global ws_handler
    ws_handler = ws_server.WebSocketHandler(server)
    ws_handler.start()

    # server.register_event_listener(
    #     "mcdr.user_info",
    #     on_user_info,
    #     priority=500
    # )


def on_unload(server: PluginServerInterface):
    """
	Do some clean up when your plugin is being unloaded. Note that it might be a reload
	"""
    server.logger.info('Bye')

    global ws_handler
    if ws_handler is not None:
        ws_handler.stop()


def on_info(server: PluginServerInterface, info: Info):
    """
	Handler for general server output event
	Recommend to use on_user_info instead if you only care about info created by users
	"""
    if not info.is_user and re.fullmatch(r'Starting Minecraft server on \S*', info.content):
        server.logger.info('Minecraft is starting at address {}'.format(info.content.rsplit(' ', 1)[1]))


def on_user_info(server: PluginServerInterface, info: Info):
    server.logger.info(f"info.content = {info.content}")
    if ws_handler is None:
        server.logger.info("ws_handler is none")
    else:
        ws_handler.broadcast({
            'type': 'player_msg',
            'player_name': info.player,
            "content": info.content
        })

def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    """
	A new player joined game, welcome!
	"""
    # server.tell(player, 'qwq!')
    # server.say('【mcdr_listener_ws_server】, 你好呀，{}！'.format(player))

    server.logger.info(f"player come:{player}")

    player_logger.log_event(
        data={
            "type": "player_join",
            "player_name": player
        }
    )

    if ws_handler is None:
        server.logger.info("ws_handler is none")
    else:
        ws_handler.broadcast({
            'type': 'player_join',
            'player_name': player
        })


def on_player_left(server: PluginServerInterface, player: str):
    """
	A player left the game, do some cleanup!
	"""
    server.say('Bye {}'.format(player))

    server.logger.info(f"player leave:{player}")

    player_logger.log_event(
        data={
            "type": "player_leave",
            "player_name": player
        }
    )

    if ws_handler is None:
        server.logger.info("ws_handler is none")
    else:
        ws_handler.broadcast({
            'type': 'player_leave',
            'player_name': player
        })


def on_server_start(server: PluginServerInterface):
    """
	When the server begins to start
	"""
    server.logger.info('Server is starting')


def on_server_startup(server: PluginServerInterface):
    """
	When the server is fully startup
	"""
    server.logger.info('Server has started')


def on_server_stop(server: PluginServerInterface, return_code: int):
    """
	When the server process is stopped, go do some clean up
	If the server is not stopped by a plugin, this is the only chance for plugins to restart the server, otherwise MCDR
	will exit too
	"""
    server.logger.info('Server has stopped and its return code is {}'.format(return_code))


def on_mcdr_start(server: PluginServerInterface):
    """
	When MCDR just launched
	"""
    server.logger.info('Another new launch for MCDR')


def on_mcdr_stop(server: PluginServerInterface):
    """
	When MCDR is about to stop, go do some clean up
	MCDR will wait until all on_mcdr_stop event call are finished before exiting
	"""
    server.logger.info('See you next time~')


