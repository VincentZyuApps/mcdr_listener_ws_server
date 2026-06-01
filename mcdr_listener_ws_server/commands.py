from mcdreforged.api.all import CommandSource, GreedyText, Literal, PluginServerInterface

from .translator import reply_tr, tr

def register_commands(server: PluginServerInterface, image_handler) -> None:
    server.register_command(
        Literal('!!view_image')
        .then(
            GreedyText('url')
            .runs(lambda src, ctx: handle_view_image(server, src, ctx['url'], image_handler))
        )
    )


def register_help_messages(server: PluginServerInterface) -> None:
    server.register_help_message('!!view_image <url>', tr(server, 'help.view_image'))


def handle_view_image(server: PluginServerInterface, source: CommandSource, url: str, image_handler) -> None:
    if not source.is_player:
        reply_tr(server, source, 'command.player_only')
        return

    player_name = source.player
    server.logger.info(f'[handle_view_image] 玩家 {player_name} 请求查看图片: {url[:100]}...')

    if image_handler:
        image_handler.view_image(player_name, url)
    else:
        reply_tr(server, source, 'command.image_handler_not_initialized')
