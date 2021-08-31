import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID = int(os.environ.get("API_ID", 12345))
    API_HASH = os.environ.get("API_HASH", "")
    USERNAME = os.environ.get('CHANNEL_USERNAME')
    CAPTION = os.environ.get("DYNAMIC_CAPTION")
    CUSTOM_TAG = os.environ.get("CUSTOM_TAG")
    if CUSTOM_TAG:
        custom_tag = " {" + CUSTOM_TAG + "}"
    else:
        custom_tag = " "
