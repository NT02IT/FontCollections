import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "../log.txt")

def new_logger(log_name):
    open(LOG_FILE, "w").close()
    now = datetime.now()
    formatted_time = now.strftime("%d-%m-%y %H:%M:%S")
    log_message(f"{formatted_time} > {log_name}")

def log_message(message):
    print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(message + "\n")