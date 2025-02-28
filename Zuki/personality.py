# personality.py
import os
import datetime

DATA_FOLDER = "ZukiUserData"
LAST_GREET_FILE = os.path.join(DATA_FOLDER, "last_greet.txt")

def ensure_data_folder():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

def load_last_greet_time():
    """Load the last greeting timestamp from file, or use 'now' if file doesn't exist."""
    ensure_data_folder()
    if os.path.isfile(LAST_GREET_FILE):
        with open(LAST_GREET_FILE, "r", encoding="utf-8") as f:
            ts_str = f.read().strip()
            try:
                return float(ts_str)  # timestamp as float
            except:
                pass
    # Default to 'now' if file is missing or corrupt
    return datetime.datetime.now().timestamp()

def save_last_greet_time():
    """Update the greeting time in the file to 'now'."""
    ensure_data_folder()
    with open(LAST_GREET_FILE, "w", encoding="utf-8") as f:
        f.write(str(datetime.datetime.now().timestamp()))

def time_since_last_greet():
    """Return seconds elapsed since the last greeting."""
    last_ts = load_last_greet_time()
    last_greet = datetime.datetime.fromtimestamp(last_ts)
    elapsed = (datetime.datetime.now() - last_greet).total_seconds()
    return elapsed

def greet_zuki():
    """User greets Zuki, reset the timer and return a message."""
    save_last_greet_time()
    return "Hello to you too! I missed you!"

# OPTIONAL: You could define different mood thresholds
MOOD_THRESHOLDS = {
    "lonely": 120,   # seconds (2 minutes)
    "sad": 300       # seconds (5 minutes)
}

def check_mood():
    """Check how long it's been, and return a mood message or None if fine."""
    elapsed = time_since_last_greet()
    if elapsed > MOOD_THRESHOLDS["sad"]:
        return "Zuki is sad. You haven’t greeted me in a long time…"
    elif elapsed > MOOD_THRESHOLDS["lonely"]:
        return "Zuki feels lonely. Say 'hello zuki' to brighten my day!"
    else:
        return None