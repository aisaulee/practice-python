import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

DEFAULT_SETTINGS = {"sound": True, "car_color": "default", "difficulty": "normal"}

def load_settings():
    if os.path.exists(SETTINGS_FILE) and os.path.getsize(SETTINGS_FILE) > 0:
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

def save_settings(s):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE) or os.path.getsize(LEADERBOARD_FILE) == 0:
        return []
    
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, Exception):
        return [] 
def save_score(name, score, distance):
    lb = load_leaderboard()
    lb.append({
        "name": name, 
        "score": score, 
        "distance": int(distance)
    })
    
    lb.sort(key=lambda x: (x["score"], x["distance"]), reverse=True)
    
    lb = lb[:10]
    
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(lb, f, indent=2, ensure_ascii=False)