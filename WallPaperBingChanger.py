"""
script en Python para establecer la imagen del día como fondo de pantalla en Windows
"""

import ctypes
import requests
import datetime
import json
import urllib
import os
import errno

#conseguimos el url de la imagen del día
respuesta = requests.get("https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US")

imagenDatos = json.loads(respuesta.text)

imagenUrl = imagenDatos["images"][0]["url"]
imagenUrl = imagenUrl.split("&")[0]
imagenUrlCompleta = "https://www.bing.com" + imagenUrl
#imagenUrlCompleta = "https://www.bing.com/th?id=OHR.SunSalutation_EN-US2164003866_1920x1080.jpg"

#definimos un nombre para la imagen basado en la fecha actual
nombreImagen = datetime.date.today().strftime("%Y%m%d")
extImagen = imagenUrl.split(".")[-1]
nombreImagen = nombreImagen + "." + extImagen

#descargamos y guardamos la imagen

#ruta donde se guardarán nuestras imagenes
ruta = "C:\\MARCXPLOIT\\img\\"
#si la ruta no existe se crea
try:
    os.makedirs(ruta)
except OSError as e:
    #print(e)
    if e.errno != errno.EEXIST:
        raise
        
rutaCompleta = ruta + nombreImagen
urllib.request.urlretrieve(imagenUrlCompleta, rutaCompleta)

#comando en Windows para establecer el fondo de pantalla
ctypes.windll.user32.SystemParametersInfoW(20, 0, rutaCompleta, 3)
