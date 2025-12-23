import re
from collections import Counter

from utils import format_day_ru

BAD_WORDS_PATTERNS = [
    r"\b(бля|блять|бляд|блядь)\w*\b",
    r"\b(хуй|хуе|хуё|хуя|хер)\w*\b",
    r"\b(пизд|пизда|пиздец)\w*\b",
    r"\b(еб|ёб|еба|ёба)\w*\b",
    r"\b(сука|сучк)\w*\b",
]

def extract_text(text):
    if isinstance(text, str):
        return text
    if isinstance(text, list):
        return "".join(t["text"] if isinstance(t, dict) else str(t) for t in text)
    return ""

def parse_data(data):
    messages = data["chats"]["list"][0]["messages"] if "chats" in data else data["messages"]

    days = Counter()
    users = Counter()
    bad = Counter()
    bad_days = Counter()

    for msg in messages:
        if not msg.get("from") or "text" not in msg:
            continue

        users[msg["from"]] += 1
        text = extract_text(msg["text"]).lower()

        date_raw = msg.get("date")
        if date_raw:
            day = format_day_ru(date_raw[:10])
            days[day] += 1

        bad_count_msg = 0

        for p in BAD_WORDS_PATTERNS:
            for m in re.finditer(p, text):
                bad[m.group(0)] += 1
                bad_count_msg += 1
        
        if bad_count_msg and date_raw:
            bad_days[day] += bad_count_msg

    photos = 0

    for msg in messages:
        if msg.get("photo"):
            photos += 1

    return {
        "messages": sum(users.values()),
        "photos": photos,
        "active_day": days.most_common(1)[0] if days else None,
        "top_users": users.most_common(5),
        "bad_words": sum(bad.values()),
        "top_bad_words": bad.most_common(3),
        "bad_day": bad_days.most_common(1)[0] if bad_days else None
    }