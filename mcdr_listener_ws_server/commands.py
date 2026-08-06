from mcdreforged.api.all import (
    CommandSource,
    GreedyText,
    Literal,
    PluginServerInterface,
    RText,
    RColor,
    RStyle,
)

from .translator import reply_tr, tr


def register_commands(server: PluginServerInterface, image_handler) -> None:
    server.register_command(
        Literal("!!view_image").then(
            GreedyText("url").runs(
                lambda src, ctx: handle_view_image(
                    server, src, ctx["url"], image_handler
                )
            )
        )
    )


def register_help_messages(server: PluginServerInterface) -> None:
    server.register_help_message("!!view_image <url>", tr(server, "help.view_image"))


def handle_view_image(
    server: PluginServerInterface, source: CommandSource, url: str, image_handler
) -> None:
    if not source.is_player:
        reply_tr(server, source, "command.player_only")
        return

    player_name = source.player
    config = server.load_config_simple("config.yml")
    permission = config.get("view_image_permission", 0)
    whitelist = config.get("view_image_player_whitelist", [])

    # 检查权限：满足任一条件即可通过
    # 1. whitelist 不为空且玩家在白名单中
    # 2. permission > 0 且玩家权限等级达标
    # 3. 两者都为空/默认 -> 所有玩家可用
    in_whitelist = len(whitelist) > 0 and player_name in whitelist
    has_permission = permission > 0 and source.get_permission_level() >= permission

    if len(whitelist) > 0 and permission > 0:
        # 两者都配置 -> 满足任一条件即可
        if not in_whitelist and not has_permission:
            reply_tr(server, source, "command.no_permission")
            return
    elif len(whitelist) > 0:
        # 仅白名单
        if not in_whitelist:
            reply_tr(server, source, "command.no_permission")
            return
    elif permission > 0:
        # 仅权限等级
        if not has_permission:
            reply_tr(server, source, "command.no_permission")
            return

    server.logger.info(
        f"[handle_view_image] 玩家 {player_name} 请求查看图片: {url[:100]}..."
    )

    if image_handler:
        image_handler.view_image(player_name, url)
    else:
        reply_tr(server, source, "command.image_handler_not_initialized")
