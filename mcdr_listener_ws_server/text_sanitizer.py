def sanitize_for_console_encoding(text: str) -> str:
    # The current Windows server environment still uses a GBK-compatible console path.
    # Replace characters that cannot be encoded there, such as many emoji, to avoid send failures.
    return text.encode('gbk', errors='replace').decode('gbk')
