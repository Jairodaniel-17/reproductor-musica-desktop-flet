import numpy as np
from PIL import Image


def obtener_color_complementario(ruta_imagen):
    # Abre la imagen
    image = Image.open(ruta_imagen)
    # Convierte la imagen a un arreglo NumPy
    image_array = np.array(image)
    # Obtiene los colores y sus frecuencias
    colors, counts = np.unique(
        image_array.reshape(-1, image_array.shape[-1]), axis=0, return_counts=True
    )
    # Obtiene el color que más se repite
    most_common_color = colors[np.argmax(counts)]
    # Obtiene el complementario del color que más se repite
    complementary_color = np.array([255, 255, 255]) - most_common_color
    # obtener el codigo de color que mas se repite
    most_common_color = "#{:02x}{:02x}{:02x}".format(*most_common_color)
    # Obtiene el código hexadecimal del color complementario
    hex_color_complementario = "#{:02x}{:02x}{:02x}".format(*complementary_color)
    return most_common_color, hex_color_complementario


# Ejemplo de uso
ruta_imagen = (
    "C:/Users/jairo/OneDrive/2022/Escritorio/fletMusica/musica/img/_7 Días (Audio).jpg"
)

color_mas_repite, hex_color_complementario = obtener_color_complementario(ruta_imagen)

print("El color que más se repite es:", color_mas_repite)
print(f"El código hexadecimal del color complementario es: {hex_color_complementario}")
