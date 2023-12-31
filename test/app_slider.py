import flet as ft
import flet_core as fc
from math import pi


def main(page):
    def slider_changed(e):
        t.value = f"Slider with 'on_change' event: {e.control.value}"
        page.update()

    slider_audio = ft.Slider(
        thumb_color="#F7A141",  # color anaranjado
        active_color="#dcdcde",  # color negro suave
        inactive_color="#7221A1",
        on_change_start=lambda _: print("Cambiando..."),
        on_change_end=lambda _: print("Cambiado!"),
        on_change=lambda e: print(f"Valor: {e.control.value}"),
    )
    t = ft.Text("Slider with 'on_change' event: ")
    page.add(
        ft.Text("Slider with value:"),
        ft.Slider(value=0.0),
        slider_audio,
        ft.Text("Slider with a custom range and label:"),
        ft.Slider(min=0, max=100, divisions=10, label="{value}%"),
        ft.Slider(
            min=0, max=100, divisions=99, label="{value}%", on_change=slider_changed
        ),
        t,
        ft.Container(
            ft.Slider(
                rotate=fc.transform.Rotate(-pi / 2),
                value=1.0,
                min=0.0,
                max=1.0,
                divisions=20,
                on_change=slider_changed,
            ),
            margin=20,
            padding=20,
            # tamaño 200 x 200
            width=200,
            height=200,
            bgcolor="#F7A141",
        ),
    )


ft.app(target=main)
