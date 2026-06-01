from typing import Any

from mcdreforged.api.all import CommandSource, PluginServerInterface


def tr(server: PluginServerInterface, key: str, *args: Any, **kwargs: Any):
    return server.rtr(f'mcdr_listener_ws_server.{key}', *args, **kwargs)


def reply_tr(server: PluginServerInterface, source: CommandSource, key: str, *args: Any, **kwargs: Any) -> None:
    source.reply(tr(server, key, *args, **kwargs))
