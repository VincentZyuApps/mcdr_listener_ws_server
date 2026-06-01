import re


def create_clickable_image_text(idx: int, url: str, summary: str = '图片') -> str:
    display_url = url[:50] + '...' if len(url) > 50 else url
    summary_escaped = summary.replace("'", "\\'").replace('\n', '\\n')
    display_url_escaped = display_url.replace("'", "\\'")
    url_escaped = url.replace("'", "\\'")

    return (
        '{text:"[图片#' + str(idx) + ']",'
        'color:"gold",'
        'bold:true,'
        'underlined:true,'
        'hover_event:{action:"show_text",value:\'点击查看图片\\n' + summary_escaped + '\\n\\nURL: ' + display_url_escaped + '\'},'
        'click_event:{action:"suggest_command",command:"!!view_image ' + url_escaped + '"}}'
    )


def sanitize_for_tellraw(text: str) -> str:
    text = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    text = text.replace('\t', ' ')
    text = ''.join(c if (ord(c) >= 0x20 and ord(c) != 0x7F) else ' ' for c in text)
    text = re.sub(r' +', ' ', text)
    return text.strip()


def replace_image_markers(message: str, images: list) -> str:
    message = sanitize_for_tellraw(message)

    if not images:
        message_escaped = message.replace('\\', '\\\\').replace('"', '\\"')
        return f'{{text:"{message_escaped}"}}'

    image_map = {img['idx']: img for img in images}
    pattern = r'<img:(\d+)>'
    parts = []
    last_end = 0

    for match in re.finditer(pattern, message):
        if match.start() > last_end:
            text_before = message[last_end:match.start()]
            if text_before:
                text_before = sanitize_for_tellraw(text_before)
                text_before = text_before.replace('\\', '\\\\').replace('"', '\\"')
                parts.append(f'{{text:"{text_before}"}}')

        idx = int(match.group(1))
        if idx in image_map:
            img_info = image_map[idx]
            parts.append(create_clickable_image_text(
                idx,
                img_info['url'],
                img_info.get('summary', '图片')
            ))
        else:
            parts.append(f'{{text:"[图片#{idx}]",color:"gray"}}')

        last_end = match.end()

    if last_end < len(message):
        text_after = message[last_end:]
        if text_after:
            text_after = sanitize_for_tellraw(text_after)
            text_after = text_after.replace('\\', '\\\\').replace('"', '\\"')
            parts.append(f'{{text:"{text_after}"}}')

    if not parts:
        message_escaped = message.replace('\\', '\\\\').replace('"', '\\"')
        return f'{{text:"{message_escaped}"}}'

    return ','.join(parts)
