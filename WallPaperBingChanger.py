import ctypes
import requests
import datetime
import json
import urllib
from pathlib import Path

# Función para obtener la imagen del día desde Bing
def obtener_imagen_del_dia():
    try:
        print('Conectando...')
        respuesta = requests.get("https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US")
        respuesta.raise_for_status()  # Verifica si hay errores en la solicitud
        print('Conexión exitosa...')
        imagenDatos = respuesta.json()
        imagenUrl = imagenDatos["images"][0]["url"].split("&")[0]
        return "https://www.bing.com" + imagenUrl
    except requests.RequestException as e:
        print(f"Error al conectar con la API de Bing: {e}")
        return None

# Función para descargar la imagen
def descargar_imagen(imagenUrl, ruta):
    try:
        nombreImagen = datetime.date.today().strftime("%Y%m%d") + "." + imagenUrl.split(".")[-1]
        rutaCompleta = ruta / nombreImagen
        urllib.request.urlretrieve(imagenUrl, rutaCompleta)
        print('Descarga exitosa...')
        return rutaCompleta
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")
        return None

# Función para establecer la imagen como fondo de pantalla en Windows
def establecer_fondo(rutaCompleta):
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(rutaCompleta), 3)
        print('Fondo de pantalla establecido correctamente.')
    except Exception as e:
        print(f"Error al establecer el fondo de pantalla: {e}")

# Función para limpiar imágenes viejas (opcional)
def limpiar_imagenes_viejas(ruta, dias_a_conservar=7):
    limite = datetime.datetime.now() - datetime.timedelta(days=dias_a_conservar)
    for img in ruta.glob("*.jpg"):  # Cambia la extensión si es necesario
        if datetime.datetime.fromtimestamp(img.stat().st_mtime) < limite:
            img.unlink()
            print(f"Imagen eliminada: {img.name}")

if __name__ == "__main__":
    # Ruta donde se guardarán las imágenes
    ruta_imagenes = Path("C:/marcxploit/img/")
    # Verificar si la ruta existe, y si no, crearla
if not ruta_imagenes.exists():
    ruta_imagenes.mkdir(parents=True, exist_ok=True)
    print(f"Directorio creado: {ruta_imagenes}")
else:
    print(f"El directorio de descarga ya existe")

    # Obtener URL de la imagen
    imagenUrlCompleta = obtener_imagen_del_dia()

    if imagenUrlCompleta:
        # Descargar la imagen
        ruta_imagen = descargar_imagen(imagenUrlCompleta, ruta_imagenes)

        if ruta_imagen:
            # Establecer el fondo de pantalla
            establecer_fondo(ruta_imagen)
            # Limpiar imágenes viejas
            ###limpiar_imagenes_viejas(ruta_imagenes)
