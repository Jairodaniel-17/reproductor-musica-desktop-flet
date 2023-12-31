import flet as ft
import flet_core as fc
from math import pi


def main(page: ft.Page):
    volumen_actual = ft.Text(
        "Volumen: 100.00%",
        text_align=ft.TextAlign.CENTER,
        size=14,
    )

    def slider_changed(e):
        volumen_actual.value = f"Volumen: {round(e.control.value*100, 2)}%"
        page.update()

    def reproductor():
        items = []
        # crear 4 filas, fila 1 contiene 1 boton, fila 2 contiene 2 botones, fila 3 contiene 1 boton, fila 4 contiene 3 boton
        # fila 1
        items.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(
                            "Nombre de la canción...",
                            text_align=ft.TextAlign.CENTER,
                            size=20,
                        ),
                        width=700,
                        height=70,
                        padding=20,
                        bgcolor=ft.colors.BLUE_GREY_800,
                        theme_mode=ft.ThemeMode.DARK,
                        border_radius=20,
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        # fila 2
        items.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.icons.IMAGE_ROUNDED),
                        width=250,
                        height=250,
                        bgcolor=ft.colors.DEEP_PURPLE_300,
                        theme_mode=ft.ThemeMode.DARK,
                        padding=20,
                        border_radius=20,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(
                                    volumen_actual,
                                    width=300,
                                    height=70,
                                    theme_mode=ft.ThemeMode.DARK,
                                    padding=20,
                                ),
                                ft.Container(
                                    ft.Slider(
                                        rotate=fc.transform.Rotate(-pi / 2),
                                        value=1.0,
                                        min=0.0,
                                        max=1.0,
                                        divisions=20,
                                        on_change=slider_changed,
                                    ),
                                    width=300,
                                    height=250,
                                    theme_mode=ft.ThemeMode.DARK,
                                    padding=20,
                                    expand=True,
                                ),
                            ],
                        ),
                        width=230,
                        height=250,
                        bgcolor=ft.colors.PINK_300,
                        theme_mode=ft.ThemeMode.DARK,
                        padding=20,
                        border_radius=20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        # fila 3
        items.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Slider(),
                        width=300,
                        height=50,
                        bgcolor=ft.colors.BLUE_600,
                        theme_mode=ft.ThemeMode.DARK,
                        padding=20,
                        border_radius=20,
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        # fila 4
        items.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.icons.SKIP_PREVIOUS_ROUNDED),
                        width=50,
                        height=50,
                        bgcolor=ft.colors.ORANGE_300,
                        theme_mode=ft.ThemeMode.DARK,
                        # padding=20,
                        border_radius=20,
                        # expand=True,
                    ),
                    ft.Container(
                        content=ft.Icon(ft.icons.PAUSE_ROUNDED),
                        width=50,
                        height=50,
                        bgcolor=ft.colors.RED_300,
                        theme_mode=ft.ThemeMode.DARK,
                        # padding=20,
                        border_radius=20,
                        # expand=True,
                    ),
                    ft.Container(
                        content=ft.Icon(ft.icons.PLAY_ARROW_ROUNDED),
                        width=50,
                        height=50,
                        bgcolor=ft.colors.PURPLE_300,
                        theme_mode=ft.ThemeMode.DARK,
                        # padding=20,
                        border_radius=20,
                        # expand=True,
                    ),
                    ft.Container(
                        content=ft.Icon(ft.icons.SKIP_NEXT_ROUNDED),
                        width=50,
                        height=50,
                        bgcolor=ft.colors.TEAL_ACCENT_700,
                        theme_mode=ft.ThemeMode.DARK,
                        # padding=20,
                        border_radius=20,
                        # expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        return items

    page.add(
        ft.Container(
            content=ft.Column(
                reproductor(),
            ),
            theme=ft.Theme(color_scheme_seed=ft.colors.LIGHT_GREEN_100),
            bgcolor=ft.colors.BROWN_400,
            theme_mode=ft.ThemeMode.DARK,
            padding=20,
            border_radius=20,
            alignment=ft.alignment.center,
            expand=True,
        )
    )
    # def items(count):
    #     items = []
    #     for i in range(1, count + 1):
    #         items.append(
    #             ft.Container(
    #                 content=ft.Text(value=str(i)),
    #                 alignment=ft.alignment.center,
    #                 width=50,
    #                 height=50,
    #                 bgcolor=ft.colors.AMBER_500,
    #             )
    #         )
    #         items.append(
    #             ft.Container(
    #                 content=ft.Text(value=str(i)),
    #                 alignment=ft.alignment.center,
    #                 width=50,
    #                 height=50,
    #                 bgcolor=ft.colors.BROWN_600,
    #             )
    #         )
    #     return items

    # def row_with_alignment(align: ft.MainAxisAlignment):
    #     return ft.Column(
    #         [
    #             ft.Text(str(align), size=16),
    #             ft.Container(
    #                 content=ft.Row(reproductor(), alignment=align),
    #                 bgcolor=ft.colors.AMBER_100,
    #             ),
    #         ]
    #     )

    # page.add(
    #     row_with_alignment(ft.MainAxisAlignment.START),
    #     row_with_alignment(ft.MainAxisAlignment.CENTER),
    #     row_with_alignment(ft.MainAxisAlignment.END),
    #     row_with_alignment(ft.MainAxisAlignment.SPACE_BETWEEN),
    #     row_with_alignment(ft.MainAxisAlignment.SPACE_AROUND),
    #     row_with_alignment(ft.MainAxisAlignment.SPACE_EVENLY),
    # )


ft.app(target=main)
