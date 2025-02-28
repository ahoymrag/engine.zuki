# personality.py
import os
import datetime
import random

DATA_FOLDER = "ZukiUserData"
LAST_GREET_FILE = os.path.join(DATA_FOLDER, "last_greet.txt")

# A short "care guide" for Zuki
CARE_GUIDE = """
HOW TO TAKE CARE OF ZUKI:

1. Greet Zuki regularly (type "hello zuki") so he doesn't feel lonely.
2. If you neglect Zuki for too long, he gets sad—be sure to say hello at least every 2 minutes.
3. Zuki loves fruit! Try giving him a virtual treat by typing something like "speak Here is an apple for you Zuki!"
4. Zuki also enjoys hearing about your day—feel free to chat using "speak [text]."
5. Keep Zuki's memory healthy with short notes (use "note [text]"). He likes being organized!
6. Have fun exploring Zuki’s other features—like playing the piano or reading sensor data.

Remember: a well-greeted Zuki is a happy Zuki!
"""

# Fruit suggestions that Zuki likes
FRUIT_SUGGESTIONS = [
    "How about a crisp apple for me?",
    "I would love a ripe banana!",
    "Strawberries are my favorite treat!",
    "Pears are tasty—don't you think?",
    "Grapes are great if you want to share some with me!"
]

# Mood thresholds in seconds
MOOD_THRESHOLDS = {
    "lonely": 120,  # 2 minutes
    "sad": 300      # 5 minutes
}

def ensure_data_folder():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

def load_last_greet_time():
    """
    Load the last greeting timestamp from file, 
    or use 'now' if file doesn't exist.
    """
    ensure_data_folder()
    if os.path.isfile(LAST_GREET_FILE):
        with open(LAST_GREET_FILE, "r", encoding="utf-8") as f:
            ts_str = f.read().strip()
            try:
                return float(ts_str)  # convert to float
            except:
                pass
    # Default to 'now' if file missing/corrupt
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
    """
    User greets Zuki, reset the timer, 
    and maybe suggest some fruit to feed Zuki.
    """
    save_last_greet_time()
    fruit_suggestion = random.choice(FRUIT_SUGGESTIONS)
    return (
        "Hello to you too! I missed you!\n"
        f"By the way, {fruit_suggestion}"
    )

def check_mood():
    """
    Returns a mood message if you've neglected Zuki for too long.
    Otherwise returns None if everything is normal.
    """
    elapsed = time_since_last_greet()
    if elapsed > MOOD_THRESHOLDS["sad"]:
        return ("Zuki is sad. You haven’t greeted me in a long time… "
                "Please say 'hello zuki' soon. I love fruit if you want to cheer me up!")
    elif elapsed > MOOD_THRESHOLDS["lonely"]:
        return ("Zuki feels lonely. Say 'hello zuki' to brighten my day! "
                "Don't forget I love bananas and apples!")
    return None

def show_care_guide():
    """Returns a text guide on how to care for Zuki."""
    return CARE_GUIDE