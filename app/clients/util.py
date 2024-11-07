import os
from functools import lru_cache

import json
from dotenv import load_dotenv


@lru_cache
def util_get_cols():
    """read categorical columns from dotenv file"""
    load_dotenv()
    return json.loads(os.getenv('FEATURE_COLS_IN_SEQ'))
