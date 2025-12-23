import flet as ft
import json
import os
import shutil

from utils import inflect_with_num
from parser import *
from cards import *


def main(page: ft.Page):
    page.window_width = 430
    page.window_height = 900
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    os.makedirs("output", exist_ok=True)

    images = []
    index = 0
    drag_dx = 0
    stats_cache = {}

    def on_export_result(r):
        if not r.path:
            return

        folder = r.path
        for img in images:
            shutil.copy(img, folder)

        page.snack_bar = ft.SnackBar(ft.Text("Все карточки экспортированы"))
        page.snack_bar.open = True
        page.update()

    export_picker = ft.FilePicker(on_result=on_export_result)
    page.overlay.append(export_picker)


    def build_image():
        return ft.Image(
            src=images[index],
            width=360,
            height=450,
            fit=ft.ImageFit.CONTAIN,
        )

    switcher = ft.AnimatedSwitcher(
        content=ft.Container(),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=300,
    )

    dots = ft.Row(width=140, alignment=ft.MainAxisAlignment.CENTER)

    def update():
        switcher.content = build_image()
        dots.controls = [
            ft.Text("●" if i == index else "○", size=16)
            for i in range(len(images))
        ]
        page.update()

    def prev_card(e=None):
        nonlocal index
        index = (index - 1) % len(images)
        update()

    def next_card(e=None):
        nonlocal index
        index = (index + 1) % len(images)
        update()

    def on_pan_update(e):
        nonlocal drag_dx
        drag_dx += e.delta_x

    def on_pan_end(e):
        nonlocal drag_dx
        if drag_dx > 80:
            prev_card()
        elif drag_dx < -80:
            next_card()
        drag_dx = 0

    def on_double_tap(e):
        if images[index].endswith("bad.png"):
            top = stats_cache.get("top_bad_words", [])
            if not top:
                text = "😎 Вы очень крутой"
            else:
                text = "\n".join(f"{w} — {c}" for w, c in top)
            page.dialog = ft.AlertDialog(
                title=ft.Text("🔥 Пасхалка"),
                content=ft.Text(text),
                actions=[ft.TextButton("Ок", on_click=lambda _: close_dialog())],
            )
            page.dialog.open = True
            page.update()

    def close_dialog():
        page.dialog.open = False
        page.update()

    gesture = ft.GestureDetector(
        content=switcher,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        on_double_tap=on_double_tap,
    )

    def export_all(e):
        export_picker.get_directory_path(
            dialog_title="Выбери папку для экспорта карточек"
        )

    def load_json(e):
        nonlocal images, index, stats_cache
        with open(e.files[0].path, encoding="utf-8") as f:
            stats_cache = parse_data(json.load(f))

        images = [card_messages(stats_cache)]

        if len(stats_cache["top_users"]) > 1:
            images.append(card_users(stats_cache))

        images += [
            card_photos(stats_cache),
            card_active_day(stats_cache),
            card_bad(stats_cache)
        ]

        if stats_cache.get("bad_day"):
            images.append(card_bad_day(stats_cache))

        index = 0
        page.controls.clear()
        page.add(cards_view)
        update()

    picker = ft.FilePicker(on_result=load_json)
    page.overlay.append(picker)

    welcome = ft.Column(
        [
            ft.Icon(ft.icons.AUTO_AWESOME, size=72),
            ft.Text("Telegram Итоги Года", size=30, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Загрузи экспорт чата и получи красивые карточки",
                color=ft.colors.GREY,
            ),
            ft.Text(
                "1. Экспортируй чат из Telegram за последний год\n"
                "2. Выбери result.json\n"
                "3. Листай и сохраняй карточки",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.ElevatedButton(
                "Начать",
                icon=ft.icons.UPLOAD_FILE,
                on_click=lambda _: picker.pick_files(allowed_extensions=["json"]),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        spacing=16,
    )

    cards_view = ft.Column(
        [
            gesture,
            dots,
            ft.Row(
                [
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=prev_card),
                    ft.IconButton(ft.icons.SAVE, on_click=export_all),
                    ft.IconButton(ft.icons.ARROW_FORWARD, on_click=next_card),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    page.add(welcome)

ft.app(target=main)
