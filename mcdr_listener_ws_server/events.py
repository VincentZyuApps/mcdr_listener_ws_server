import re

from mcdreforged.api.all import Info, PluginServerInterface

from .translator import tr


def on_info(server: PluginServerInterface, info: Info) -> None:
    if not info.is_user and re.fullmatch(r'Starting Minecraft server on \S*', info.content):
        server.logger.info('【 Server starting 】 {}'.format(info.content.rsplit(' ', 1)[1]))


def on_user_info(server: PluginServerInterface, info: Info, ws_handler) -> None:
    server.logger.info(f"【 Player chat 】 {info.player}: {info.content}")
    if ws_handler is None:
        server.logger.warning("【 WS skipped 】 player chat broadcast skipped because handler is not initialized")
        return
    ws_handler.broadcast({
        'type': 'player_msg',
        'player_name': info.player,
        'content': info.content,
    })


def on_player_joined(server: PluginServerInterface, player: str, info: Info, ws_handler, player_logger) -> None:
    server.logger.info(f"【 Player joined 】 {player}")
    player_logger.log_event(data={'type': 'player_join', 'player_name': player})

    if ws_handler is None:
        server.logger.warning("【 WS skipped 】 join broadcast skipped because handler is not initialized")
        return
    ws_handler.broadcast({
        'type': 'player_join',
        'player_name': player,
    })


def on_player_left(server: PluginServerInterface, player: str, ws_handler, player_logger) -> None:
    server.say(tr(server, 'player.leave_broadcast', player=player))
    server.logger.info(f"【 Player left 】 {player}")
    player_logger.log_event(data={'type': 'player_leave', 'player_name': player})

    if ws_handler is None:
        server.logger.warning("【 WS skipped 】 leave broadcast skipped because handler is not initialized")
        return
    ws_handler.broadcast({
        'type': 'player_leave',
        'player_name': player,
    })
