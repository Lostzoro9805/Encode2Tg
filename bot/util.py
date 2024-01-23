import string

import country_converter as coco
import requests

from . import *
from .funcn import VERSION2, WORKING

SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]


def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return "0B"
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f"{round(size_in_bytes, 2)}{SIZE_UNITS[index]}"
    except IndexError:
        return "File too large"

async def custcap(name, fname):
    caption = f"**{ot}**\n**✨Encoded By @DenjiXD17**"
    return caption
