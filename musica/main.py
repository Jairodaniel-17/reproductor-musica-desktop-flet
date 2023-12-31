import random
import flet as ft
import flet_core as fc
import os
from PIL import Image
import time
from math import pi
from pydub import AudioSegment
import unicodedata
import requests
import os
import zipfile
import re
from pytube import YouTube

# crear carpetas si no existe (music, img)
if not os.path.exists("music"):
    os.makedirs("music")
if not os.path.exists("img"):
    os.makedirs("img")
if not os.path.exists("temp"):
    os.makedirs("temp")

# Carpeta donde guardar las canciones
music_path = os.getcwd() + "/music"
img_path = os.getcwd() + "/img"
temp_path = os.getcwd() + "/temp"


def save_img_change_name(titulo, logo):
    titulo_normalizado = unicodedata.normalize("NFKD", titulo)
    # Limpiar el título para usarlo como nombre de archivo
    caracteres_no_permitidos = r"[\"\'/\\:*?<>|,]"
    titulo_limpio = re.sub(caracteres_no_permitidos, "", titulo_normalizado)
    # print(titulo_limpio)
    response = requests.get(logo)
    new_name = f"{titulo_limpio}.jpg"
    with open(os.path.join(temp_path, new_name), "wb") as file:
        file.write(response.content)
    return titulo_limpio


def recortar_y_ajustar_imagenes(carpeta_img, tamaño_cuadrado):
    # Obtener lista de archivos en la carpeta
    archivos = os.listdir(carpeta_img)
    for archivo in archivos:
        if archivo.startswith("_"):
            continue  # Saltar la imagen ya procesada
        ruta_completa = os.path.join(carpeta_img, archivo)
        if archivo.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            imagen = Image.open(ruta_completa)
            ancho, alto = imagen.size
            if ancho == alto:
                imagen_ajustada = imagen.resize((tamaño_cuadrado, tamaño_cuadrado))
            else:
                izquierda = max(0, (ancho - tamaño_cuadrado) // 2)
                arriba = max(0, (alto - tamaño_cuadrado) // 2)
                derecha = min(ancho, (ancho + tamaño_cuadrado) // 2)
                abajo = min(alto, (alto + tamaño_cuadrado) // 2)

                imagen_ajustada = imagen.crop(
                    (izquierda, arriba, derecha, abajo)
                ).resize((tamaño_cuadrado, tamaño_cuadrado))
            ruta_guardado = os.path.join(carpeta_img, f"_{archivo}")
            imagen_ajustada.save(ruta_guardado)
    # print("Proceso de recorte y redimensionamiento completado.")


def obtener_duracion_cancion(ruta):
    audio = AudioSegment.from_file(ruta)
    duracion_segundos = len(audio)  # Convertir milisegundos a segundos
    return duracion_segundos


def main(page: ft.Page):
    page.title = """Personal Songs 🎧❤️"""
    # campo input de entrada de texto
    entrada_texto = ft.TextField(
        label="Ingrese la URL de la canción de Youtube",
        # on_change=lambda e: print(f"Cambiando texto...{e.control.value}"),
        on_submit=lambda e: download_mp3(e.control.value),
        on_focus=lambda _: limpiar_entrada_texto(),
    )

    def limpiar_entrada_texto():
        entrada_texto.value = ""
        page.update()

    # función para descargar musica de youtube en formato mp3
    def download_mp3(url_del_usuario: str):
        # print(f"Descargando desde la URL: {url_del_usuario}")
        # obtenemos la url correctamente pasamos a lo siguiente
        # obtener la url de la cancion
        url = url_del_usuario
        # obtener el titulo de la cancion
        yt = YouTube(url)
        titulo = yt.title
        # descargar la cancion en la carpeta temp
        yt.streams.filter(only_audio=True).first().download(temp_path)
        # descargar logo de la cancion (imagen) en la carpeta temp
        logo = yt.thumbnail_url
        new_name = save_img_change_name(titulo, logo)
        # buscar el archivo descargado en la carpeta temp
        for file in os.listdir(temp_path):
            if file.endswith(".mp4"):
                # cambiar el nombre de la cancion descargada en la carpeta temp
                os.rename(
                    os.path.join(temp_path, file),
                    os.path.join(temp_path, f"{new_name}.mp4"),
                )
        # convertir a mp3
        for file in os.listdir(temp_path):
            if file.endswith(".mp4"):
                os.rename(
                    os.path.join(temp_path, file),
                    os.path.join(temp_path, file.replace(".mp4", ".mp3")),
                )
        # mover la cancion descargada a la carpeta music
        os.rename(
            os.path.join(temp_path, f"{new_name}.mp3"),
            os.path.join(music_path, f"{new_name}.mp3"),
        )
        # mover la imagen descargada a la carpeta img
        os.rename(
            os.path.join(temp_path, f"{new_name}.jpg"),
            os.path.join(img_path, f"{new_name}.jpg"),
        )
        entrada_texto.value = "Se descargó la canción exitosamente."
        page.update()
        time.sleep(4)
        limpiar_entrada_texto()

    def primera_cancion_en_existencia():
        url_primera_cancion = "https://www.youtube.com/watch?v=c9vA2WC8590"
        # traer la lista de canciones de la carpeta music
        songs = os.listdir(music_path)
        if "Bumble bee - speed up.mp3" not in songs:
            download_mp3(url_primera_cancion)
        return "./music/Bumble bee - speed up.mp3"

    tamaño_deseado = 530
    recortar_y_ajustar_imagenes(img_path, tamaño_deseado)

    ###########################################################################################
    url = primera_cancion_en_existencia()
    # llenar la url con la primera cancion que encuentre en la carpeta music
    for song in os.listdir(music_path):
        url = os.path.join(music_path, song)
        break
    src_image = ""
    # llenar la src_image con la canción de la url menos la extensión -4 y cambiar a jpg
    for song in os.listdir(music_path):
        src_image = "./img/_" + song[:-4] + ".jpg"
        break
    name_song = ""
    for song in os.listdir(music_path):
        name_song = str(song[:-4])
        break
    nombre_cancion_actual = ft.Text(
        f"{name_song}",
        size=20,
        text_align=ft.TextAlign.CENTER,
        color=ft.colors.WHITE,
    )

    image_control = ft.Image(
        src=src_image,  # Inicialmente sin imagen
        width=tamaño_deseado,
        height=tamaño_deseado,
        border_radius=ft.border_radius.all(30),
        # visible=False,  # Inicialmente invisible
    )
    # print(f"Imagen de {src_image} cargada exitosamente.")
    audio1 = ft.Audio(
        src=url,
        autoplay=False,
        volume=1,
        balance=0,
        # on_loaded=lambda _: print("Loaded"),
        on_duration_changed=lambda e: actualizar_duracion(e.data),
        on_position_changed=lambda e: actualizar_posicion(e.data),
        # on_state_changed=lambda e: print("Cambió de estado:", e.data),
        on_state_changed=lambda e: reproducir_aleatorio_song(e.data),
        # on_seek_complete=lambda _: print("Buscar completo"),
    )

    def reproducir_aleatorio_song(estado: str):
        # estado: playing, paused, completed
        if "completed" == estado:
            # crear un arreglo con las canciones de la carpeta music
            songs = os.listdir(music_path)
            # elegir una canción aleatoria
            song = random.choice(songs)
            # llenar la url con la canción elegida
            url = os.path.join(music_path, song)
            # llenar la src_image con la canción de la url menos la extensión -4 y cambiar a jpg
            src_image = "./img/_" + song[:-4] + ".jpg"
            # llenar la src_image con la canción de la url menos la extensión -4 y cambiar a jpg
            name_song = str(song[:-4])
            # necesito url, src_image, name_song
            nombre_cancion_actual.value = f"{name_song}"
            image_control.src = src_image
            image_control.visible = True
            image_control.width = tamaño_deseado
            image_control.height = tamaño_deseado
            # print(f"Imagen de {src_image} cargada exitosamente.")
            audio1.src = url
            audio1.autoplay = True
            audio1.update()
            # print(f"Cambiando audio a {url}...")
            page.update()
            audio1.play()
            audio1.autoplay = True
            audio1.update()
            page.update()
        else:
            pass

    page.overlay.append(audio1)
    volumen_actual = ft.Text(
        "Volumen: 100.00%",
        text_align=ft.TextAlign.CENTER,
        size=14,
    )

    def convertir_value(value):
        minutos = int(value) // 60
        segundos = int(value) % 60
        mili_segundo_actual = f"{minutos}:{segundos:02d}"
        return mili_segundo_actual

    def actualizar_duracion(duracion):
        sl_audio.max = duracion
        page.update()

    def actualizar_posicion(posicion):
        sl_audio.value = posicion
        page.update()

    sl_audio = ft.Slider(
        min=0,
        max=obtener_duracion_cancion(url),
        on_change_start=lambda e: slider_changed(e),
        label=lambda e: convertir_value(e.control.value),
        disabled=True,
    )

    # crear un slider con la posición de la canción audio1
    def slider_changed(e):
        if audio1.state == ft.AudioState.PLAYING:
            audio1.play()
        audio1.seek(e.control.value)
        audio1.update()
        sl_audio.value = e.control.value
        page.update()

    def avanzar_10s():
        # obtener la posición actual de la canción
        posicion_actual = audio1.get_current_position()
        # sumarle 2 segundos a la posición actual
        nueva_posicion = posicion_actual + 10000
        # buscar en la canción la nueva posición
        audio1.seek(nueva_posicion)
        # actualizar el slider
        sl_audio.value = nueva_posicion
        # actualizar la página
        page.update()

    def retroceder_10s():
        # obtener la posición actual de la canción
        posicion_actual = audio1.get_current_position()
        if posicion_actual >= 5000:
            # restarle 5 segundos a la posición actual
            nueva_posicion = posicion_actual - 5000
            # buscar en la canción la nueva posición
            audio1.seek(nueva_posicion)
            # actualizar el slider
            sl_audio.value = nueva_posicion
            # actualizar la página
            page.update()

    def slider_changed(e):
        volumen_actual.value = f"Volumen: {round(e.control.value*100, 2)}%"
        nuevo_volumen = round(e.control.value, 1)
        audio1.volume = nuevo_volumen
        audio1.update()
        page.update()

    def reproductor():
        items = []
        # crear 4 filas, fila 1 contiene 1 boton, fila 2 contiene 2 botones, fila 3 contiene 1 boton, fila 4 contiene 3 boton
        # fila 1
        items.append(
            ft.Row(
                [
                    ft.Container(
                        content=entrada_texto,
                        width=700,
                        height=90,
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
        altura = 300
        items.append(
            ft.Row(
                [
                    ft.Container(
                        content=image_control,
                        width=500,
                        height=altura,
                        bgcolor=ft.colors.DEEP_PURPLE_300,
                        theme_mode=ft.ThemeMode.DARK,
                        padding=30,
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
                                    height=altura,
                                    theme_mode=ft.ThemeMode.DARK,
                                    padding=20,
                                    expand=True,
                                ),
                            ],
                        ),
                        width=250,
                        height=altura,
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
                        content=sl_audio,
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
                        content=ft.Icon(ft.icons.REPLAY_10),
                        width=50,
                        height=50,
                        bgcolor=ft.colors.RED_300,
                        theme_mode=ft.ThemeMode.DARK,
                        border_radius=20,
                        on_click=lambda _: retroceder_10s(),
                    ),
                    ft.Container(
                        content=ft.Icon(ft.icons.PAUSE_CIRCLE_OUTLINE),
                        width=50,
                        height=50,
                        bgcolor=ft.colors.RED_300,
                        theme_mode=ft.ThemeMode.DARK,
                        border_radius=20,
                        on_click=lambda _: audio1.pause(),
                    ),
                    ft.Container(
                        content=ft.Icon(ft.icons.PLAY_ARROW_ROUNDED),
                        width=50,
                        height=50,
                        bgcolor=ft.colors.PURPLE_300,
                        theme_mode=ft.ThemeMode.DARK,
                        border_radius=20,
                        on_click=lambda _: audio1.play(),
                    ),
                    ft.Container(
                        content=ft.Icon(ft.icons.PLAY_CIRCLE_OUTLINE),
                        width=50,
                        height=50,
                        bgcolor=ft.colors.TEAL_ACCENT_700,
                        theme_mode=ft.ThemeMode.DARK,
                        border_radius=20,
                        on_click=lambda _: audio1.resume(),
                    ),
                    ft.Container(
                        content=ft.Icon(ft.icons.FORWARD_10),
                        width=50,
                        height=50,
                        bgcolor=ft.colors.TEAL_ACCENT_700,
                        theme_mode=ft.ThemeMode.DARK,
                        border_radius=20,
                        on_click=lambda _: avanzar_10s(),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        return items

    def clic_nombre_cancion(event: fc.ControlEvent, image_control: ft.Image):
        song = event.control.key  # Obtener la clave (nombre de la canción) del botón
        cambiar_imagen(song, image_control)
        actualizar_imagen(e=event)
        actualizar_nombre_cancion(e=event)
        cambiar_audio_src(song)
        # reproducir la canción
        page.update()
        audio1.play()
        audio1.update()
        # actualizar la página
        # page.update()

    # Función para cambiar imagen en base al nombre de la canción
    def cambiar_imagen(song, image_control):
        song = "_" + song[:-4] + ".jpg"
        img = os.path.join(img_path, song)
        if os.path.exists(img):
            image_control.src = img
            image_control.visible = True
            image_control.width = tamaño_deseado
            image_control.height = tamaño_deseado
            # print(f"Imagen de {img} cargada exitosamente.")
        else:
            pass

    # funcion para cambiar el audio src
    def cambiar_audio_src(song):
        audio1.src = os.path.join(music_path, song)
        audio1.autoplay = True
        audio1.update()
        # print(f"Cambiando audio a {song}...")

    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.LIGHT_BLUE_600,
    )
    page.auto_scroll = True
    page.add(
        ft.Container(
            nombre_cancion_actual,
            page.update(),
            theme=ft.Theme(color_scheme_seed=ft.colors.BLUE_GREY_50),
            bgcolor=ft.colors.SURFACE_VARIANT,
            theme_mode=ft.ThemeMode.DARK,
            alignment=ft.alignment.center,
            height=75,
            padding=20,
            border_radius=20,
        )
    )

    cl = ft.Column(
        spacing=5,
        alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO,
    )

    # traer la lista de canciones de la carpeta music
    songs = os.listdir(music_path)

    for song in songs:
        cl.controls.append(
            ft.TextButton(
                song,
                key=song,
                width=3000,
                # Clic en la canción
                on_click=lambda event, img_control=image_control: clic_nombre_cancion(
                    event, img_control
                ),
            )
        )

    def actualizar_nombre_cancion(e):
        # print("Actualizando nombre de la canción...")
        nombre_cancion_actual.value = f"{e.control.key[:-4]}"
        page.update()

    def actualizar_imagen(e):
        # print("Actualizando imagen...")
        image_control.update()

    page.add(
        ft.Row(
            [
                ft.Container(
                    cl,
                    theme=ft.Theme(color_scheme_seed=ft.colors.LIGHT_GREEN_100),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    theme_mode=ft.ThemeMode.DARK,
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=fc.padding.symmetric(horizontal=25, vertical=20),
                    border_radius=20,
                ),
                ft.VerticalDivider(),
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
                ),
            ],
            spacing=0,
            expand=True,
        ),
    )


ft.app(main)
