import re

from mcdreforged.api.all import RColor, RStyle, RText, RTextList

from .text_sanitizer import sanitize_for_console_encoding


def _strip_whitespace(text: str) -> str:
    for ch in ("\r\n", "\n", "\r", "\t"):
        text = text.replace(ch, " ")
    return re.sub(r" +", " ", text).strip()


def format_platform_message(
    group_id: str, group_name: str, nickname: str, message: str, strip_ws: bool = True
) -> RTextList:
    group_name = sanitize_for_console_encoding(group_name)
    nickname = sanitize_for_console_encoding(nickname)
    message = sanitize_for_console_encoding(message)
    if strip_ws:
        group_name = _strip_whitespace(group_name)
        nickname = _strip_whitespace(nickname)
        message = _strip_whitespace(message)
    return RTextList(
        RText("[", RColor.gold, RStyle.bold),
        RText(group_name, RColor.gold, RStyle.bold),
        RText("] ", RColor.gold, RStyle.bold),
        RText(f"({group_id}) ", RColor.aqua),
        RText(nickname, RColor.green, RStyle.italic),
        RText(": ", RColor.white),
        RText(message, RColor.white),
    )
