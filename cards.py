from PIL import Image, ImageDraw, ImageFont

from utils import inflect_with_num

WIDTH, HEIGHT = 1080, 1350
BLACK = (20, 20, 20)
GRAY = (120, 120, 120)

FONT_BOLD = "assets/Inter-Bold.ttf"
FONT_REG = "assets/Inter-Regular.ttf"

def base_card(bg):
    img = Image.open(bg).resize((WIDTH, HEIGHT))
    return img, ImageDraw.Draw(img)

def draw_title(d, title):
    font = ImageFont.truetype(FONT_BOLD, 80)
    d.text((WIDTH // 2, 200), title, font=font, fill=BLACK, anchor="mm")

def draw_big(d, value, label):
    big = ImageFont.truetype(FONT_BOLD, 188)
    reg = ImageFont.truetype(FONT_REG, 60)
    d.text((WIDTH // 2, 580), value, font=big, fill=BLACK, anchor="mm")
    d.text((WIDTH // 2, 740), label, font=reg, fill=GRAY, anchor="mm")

def save(img, name):
    path = f"output/{name}.png"
    img.save(path)
    return path

def card_active_day(s):
    img, d = base_card("assets/bg_day.png")
    draw_title(d, "Самый активный день")

    day, count = s["active_day"]
    draw_big(d, day, f"Отправлено {count} {inflect_with_num(count, ['сообщение', 'сообщений', 'сообщения'])}")

    return save(img, "active_day")

def card_bad_day(s):
    img, d = base_card("assets/bg_bad_day.png")
    draw_title(d, "Самый токсичный день")

    day, count = s["bad_day"]
    cmp1 = inflect_with_num(count, ['нецензурное', 'нецензурных', 'нецензурных'])
    draw_big(d, day, f"{count} {cmp1} {inflect_with_num(count, ['слово', 'слов', 'слова'])}")

    return save(img, "bad_day")

def card_messages(s):
    img, d = base_card("assets/bg_messages.png")
    draw_big(d, f"{s['messages']}", f"{inflect_with_num(s['messages'], ['сообщение', 'сообщений', 'сообщения'])} за год отправлено")
    return save(img, "messages")

def card_photos(s):
    img, d = base_card("assets/bg_photos.png")
    draw_big(d, str(s["photos"]), f"{inflect_with_num(s['photos'], ['фотография', 'фотографий', 'фотографии'])} отправлено")
    return save(img, "photos")

def card_users(s):
    img, d = base_card("assets/bg_top_users.png")
    f = ImageFont.truetype(FONT_REG, 60)
    y = 420
    for i, (u, c) in enumerate(s["top_users"], 1):
        d.text((WIDTH // 2, y), f"{i}. {u[:22]} — {c}", font=f, fill=BLACK, anchor="mm")
        y += 120
    return save(img, "users")

def card_bad(s):
    img, d = base_card("assets/bg_bad_words.png")
    draw_big(d, str(s["bad_words"]), f"нецензурных {inflect_with_num(s['bad_words'], ['слово', 'слов', 'слова'])} использовано")
    return save(img, "bad")