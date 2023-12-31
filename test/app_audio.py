import flet as ft
from pydub import AudioSegment

url = (
    "C:/Users/jairo/OneDrive/2022/Escritorio/fletMusica/musica/music/Alastors Game.mp3"
)


def obtener_duracion_cancion(ruta):
    audio = AudioSegment.from_file(ruta)
    duracion_segundos = len(audio)  # Convertir milisegundos a segundos
    return duracion_segundos


def main(page: ft.Page):
    def volume_down(_):
        audio1.volume -= 0.1
        audio1.update()

    def volume_up(_):
        audio1.volume += 0.1
        audio1.update()

    def balance_left(_):
        audio1.balance -= 0.1
        audio1.update()

    def balance_right(_):
        audio1.balance += 0.1
        audio1.update()

    audio1 = ft.Audio(
        src=url,
        autoplay=False,
        volume=1,
        balance=0,
        on_loaded=lambda _: print("Loaded"),
        on_duration_changed=lambda e: actualizar_duracion(e.data),
        on_position_changed=lambda e: actualizar_posicion(e.data),
        on_state_changed=lambda e: print("Cambió de estado:", e.data),
        on_seek_complete=lambda _: print("Buscar completo"),
    )
    page.overlay.append(audio1)

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

    print(f"Duración de la canción: {obtener_duracion_cancion(url)} segundos")

    # crear un slider con la posición de la canción audio1
    def slider_changed(e):
        if audio1.state == ft.AudioState.PLAYING:
            audio1.play()
        audio1.seek(e.control.value)
        audio1.update()
        sl_audio.value = e.control.value
        page.update()

    def avanzar_5s():
        # obtener la posición actual de la canción
        posicion_actual = audio1.get_current_position()
        # sumarle 2 segundos a la posición actual
        nueva_posicion = posicion_actual + 5000
        # buscar en la canción la nueva posición
        audio1.seek(nueva_posicion)
        # actualizar el slider
        sl_audio.value = nueva_posicion
        # actualizar la página
        page.update()

    def retroceder_5s():
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

    page.add(
        ft.ElevatedButton("Play", on_click=lambda _: audio1.play()),
        ft.ElevatedButton("Pause", on_click=lambda _: audio1.pause()),
        ft.ElevatedButton("Resume", on_click=lambda _: audio1.resume()),
        ft.ElevatedButton("Release", on_click=lambda _: audio1.release()),
        ft.ElevatedButton("Avanzar 5s", on_click=lambda _: avanzar_5s()),
        ft.ElevatedButton("Retroceder 5s", on_click=lambda _: retroceder_5s()),
        ft.Row(
            [
                ft.ElevatedButton("Bajar volumen", on_click=volume_down),
                ft.ElevatedButton("Subir volumen", on_click=volume_up),
            ]
        ),
        ft.Row(
            [
                ft.ElevatedButton(
                    "Balance a la izquierda de la canción", on_click=balance_left
                ),
                ft.ElevatedButton(
                    "Balance a la derecha de la canción", on_click=balance_right
                ),
            ]
        ),
        ft.ElevatedButton(
            "Get duration",
            on_click=lambda _: print("Duración:", audio1.get_duration()),
        ),
        ft.ElevatedButton(
            "Get current position",
            on_click=lambda _: print("Posición actual:", audio1.get_current_position()),
        ),
        sl_audio,
    )


ft.app(target=main)
