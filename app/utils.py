# app/utils.py
from datetime import datetime

def get_timestamp():
    return datetime.now().isoformat()
