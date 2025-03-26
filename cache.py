import os
from platformdirs import user_cache_dir
from datetime import datetime
from zoneinfo import ZoneInfo

import ZODB, ZODB.FileStorage
import persistent
import transaction

APP_NAME = "arxiv_api_client"

CACHE_DIR = user_cache_dir(APP_NAME)

def getNYTime():
    return datetime.now(ZoneInfo("America/New_York"))

# os.makedirs(cache_dir, exist_ok=True)
