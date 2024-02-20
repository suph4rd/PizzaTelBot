from os import getenv

TOKEN = getenv("BOT_TOKEN")


try:
    from .local_settings import *
except ImportError:
    pass
