# #TG-RECAP (https://mrkrk.me/projects/tg-recap)
# Copyright (C) 2025 Viktor K.

from dataclasses import dataclass
import tempfile
import os

from typing import Tuple
from PIL import Image, ImageDraw, ImageFont

from utils import inflect_with_num, resource_path

WIDTH, HEIGHT = 1080, 1920
FONT_NUM = resource_path("assets/KorinnablackcttBolditalic.ttf")
FONT_REG = resource_path("assets/ArialBlackPrimer.ttf")

temp_dir = tempfile.gettempdir()
my_temp_dir = os.path.join(temp_dir, "tg_recap")
os.makedirs(my_temp_dir, exist_ok=True)


@dataclass
class Text:
    font: ImageFont.ImageFont
    position: int
    fill: Tuple[int]
    value: str


def base_card(bg):
    img = Image.open(bg).resize((WIDTH, HEIGHT))
    return img, ImageDraw.Draw(img)


def draw(d, text):
    d.text(
        (WIDTH // 2, text.position),
        text.value,
        font=text.font,
        fill=text.fill,
        anchor="mm",
    )


def save(img, name):
    path = os.path.join(my_temp_dir, f"{name}.png")
    img.save(path)
    return path


def card_active_day(s):
    img, d = base_card(resource_path("assets/bg_day.png"))

    day, count = s["active_day"]

    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_NUM, 130),
            position=840,
            fill=(37, 179, 255),
            value=day,
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 55),
            position=975,
            fill=(224, 224, 224),
            value=f"было отправлено",
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 55),
            position=1060,
            fill=(224, 224, 224),
            value=f"{count:,} {inflect_with_num(count, ['сообщение', 'сообщений', 'сообщения'])}".replace(",", " "),
        ),
    )

    return save(img, "active_day")


def card_bad_day(s):
    img, d = base_card(resource_path("assets/bg_bad_day.png"))

    day, count = s["bad_day"]

    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_NUM, 130),
            position=840,
            fill=(191, 64, 255),
            value=day,
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 55),
            position=975,
            fill=(224, 224, 224),
            value=f"было использовано",
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 55),
            position=1060,
            fill=(224, 224, 224),
            value=f"{count:,} {inflect_with_num(count, ['нецензурное', 'нецензурных', 'нецензурных'])} {inflect_with_num(count, ['слово', 'слов', 'слова'])}".replace(",", " "),
        ),
    )

    return save(img, "bad_day")


def card_messages(s):
    img, d = base_card(resource_path("assets/bg_messages.png"))
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_NUM, 180),
            position=840,
            fill=(255, 64, 230),
            value=f"{s['messages']:,}".replace(",", " "),
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 60),
            position=980,
            fill=(224, 224, 224),
            value=inflect_with_num(
                s["messages"], ["сообщение", "сообщений", "сообщения"]
            ),
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 48),
            position=1065,
            fill=(224, 224, 224),
            value="было отправлено за год",
        ),
    )
    return save(img, "messages")


def card_photos(s):
    img, d = base_card(resource_path("assets/bg_photos.png"))
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_NUM, 180),
            position=840,
            fill=(64, 255, 236),
            value=f"{s['photos']:,}".replace(",", " "),
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 60),
            position=980,
            fill=(224, 224, 224),
            value=inflect_with_num(
                s["photos"], ["фотография", "фотографий", "фотографии"]
            ),
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 48),
            position=1065,
            fill=(224, 224, 224),
            value=f"{inflect_with_num(s['photos'], ['была', 'было', 'было'])} {inflect_with_num(s['photos'], ['отправлена', 'отправлено', 'отправлено'])} за год",
        ),
    )
    return save(img, "photos")


def card_videos(s):
    img, d = base_card(resource_path("assets/bg_videos.png"))
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_NUM, 180),
            position=840,
            fill=(255, 64, 68),
            value=f"{s['videos']:,}".replace(",", " "),
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 60),
            position=980,
            fill=(224, 224, 224),
            value=inflect_with_num(
                s["videos"], ["видеофайл", "видеофайлов", "видеофайла"]
            ),
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 48),
            position=1065,
            fill=(224, 224, 224),
            value=f"{inflect_with_num(s['videos'], ['был', 'было', 'было'])} {inflect_with_num(s['videos'], ['отправлен', 'отправлено', 'отправлено'])} за год",
        ),
    )
    return save(img, "videos")


def card_stickers(s):
    img, d = base_card(resource_path("assets/bg_stickers.png"))
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_NUM, 180),
            position=840,
            fill=(83, 67, 255),
            value=f"{s['stickers']:,}".replace(",", " "),
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 60),
            position=980,
            fill=(224, 224, 224),
            value=inflect_with_num(s["stickers"], ["стикер", "стикеров", "стикера"]),
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 48),
            position=1065,
            fill=(224, 224, 224),
            value=f"{inflect_with_num(s['stickers'], ['был', 'было', 'было'])} {inflect_with_num(s['stickers'], ['отправлен', 'отправлено', 'отправлено'])} за год",
        ),
    )
    return save(img, "stickers")


def card_audio(s):
    img, d = base_card(resource_path("assets/bg_audio.png"))
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_NUM, 180),
            position=840,
            fill=(255, 131, 64),
            value=f"{s['audio']:,}".replace(",", " "),
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 60),
            position=980,
            fill=(224, 224, 224),
            value=inflect_with_num(
                s["audio"], ["аудиофайл", "аудиофайлов", "аудиофайла"]
            ),
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 48),
            position=1065,
            fill=(224, 224, 224),
            value=f"{inflect_with_num(s['audio'], ['был', 'было', 'было'])} {inflect_with_num(s['audio'], ['отправлен', 'отправлено', 'отправлено'])} за год",
        ),
    )
    return save(img, "audio")


def card_users(s):
    img, d = base_card(resource_path("assets/bg_top_users.png"))
    y = 930 - 60 * (len(s["top_users"]) - 1)
    for _, (u, c) in enumerate(s["top_users"], 1):
        display_name = (u[: 2 - 3] + "…") if len(u) > 22 else u
        draw(
            d,
            Text(
                font=ImageFont.truetype(FONT_REG, 50),
                position=y,
                fill=(245, 255, 64),
                value=f"{display_name} — " + f"{c:,}".replace(',', ' '),
            ),
        )
        y += 120
    return save(img, "users")


def card_bad(s):
    img, d = base_card(resource_path("assets/bg_bad_words.png"))
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_NUM, 180),
            position=840,
            fill=(64, 255, 84),
            value=f"{s['bad_words']:,}".replace(",", " "),
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 60),
            position=980,
            fill=(224, 224, 224),
            value=f"{inflect_with_num(s['bad_words'], ['нецензурное', 'нецензурных', 'нецензурных'])} {inflect_with_num(s['bad_words'], ['слово', 'слов', 'слова'])}",
        ),
    )
    draw(
        d,
        Text(
            font=ImageFont.truetype(FONT_REG, 48),
            position=1065,
            fill=(224, 224, 224),
            value="было использовано за год",
        ),
    )
    return save(img, "bad")
