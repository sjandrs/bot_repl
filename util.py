import re

def sanitize(text):
    # Replace all single quotes with two single quotes to escape them
    text = text.replace("'", "''")

    # Replace all backslashes with two backslashes to escape them
    text = text.replace("\\", "\\\\")

    # Remove any non-printable characters except for space, tab, and newline
    text = re.sub(r'[^\x20-\x7E\r\n\t]+', '', text)

    return text
