import cv2
import numpy as np
import matplotlib.pyplot as plt

# ### 🖼️ Función para cargar imagen en RGB y escala de grises

# Esta función `cargar_imagen` recibe la ruta de una imagen como entrada y devuelve dos versiones de la imagen:

# 1. `img_rgb`: Imagen convertida al espacio de color RGB, ideal para mostrarla con `matplotlib`, ya que OpenCV carga las imágenes en formato BGR por defecto.
# 2. `img_gray`: Imagen convertida a escala de grises, que es útil para aplicar filtros como el gaussiano (más eficiente en una sola capa de intensidad que en las 3 del color).

# También incluye una verificación para asegurarse de que la imagen fue cargada correctamente.

def cargar_imagen(ruta_imagen):
    """
    Carga una imagen desde la ruta dada en BGR y la convierte a RGB para 
    visualizar con Matplotlib, además de la escala de grises.
    Retorna:
        - img_rgb: Imagen en formato RGB
        - img_gray: Imagen original en escala de grises
    """
    img_bgr = cv2.imread(ruta_imagen)
    if img_bgr is None:
        raise ValueError(f"No se pudo cargar la imagen en la ruta: {ruta_imagen}")

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    return img_rgb, img_gray


# ### 🖼️ Función para mostrar imágenes con Matplotlib

# La función `mostrar_imagen` muestra una imagen RGB utilizando `matplotlib.pyplot`.

# - Se le pasa una imagen (generalmente en formato RGB) y un título opcional.
# - Se desactivan los ejes (`axis("off")`) para una visualización más limpia.
# - Esta función es útil para comprobar visualmente los resultados de los filtros o transformaciones aplicadas a la imagen.

# Es importante mostrar las imágenes en RGB porque `matplotlib` no interpreta correctamente el formato BGR de OpenCV.

def mostrar_imagen(img_rgb, titulo="Imagen"):
    """
    Muestra una imagen en RGB con Matplotlib.
    """
    plt.imshow(img_rgb)
    plt.title(titulo)
    plt.axis("off")
    plt.show()


# ### 📏 Medición de contenido de alta frecuencia

# La función `medir_alta_frecuencia` evalúa el nivel de detalle o "energía" presente en una imagen procesada con un filtro de paso alto, calculando la **varianza** de la imagen resultante.

# **¿Cómo funciona?**
# - Aplica una función de filtrado (pasada como argumento) sobre una imagen en escala de grises.
# - Calcula la **varianza** de la imagen filtrada, que representa la dispersión de los valores de píxeles.

# **¿Qué representa la varianza en este contexto?**
# - Una **varianza alta** indica que hay muchos detalles, bordes o ruido (alta frecuencia).
# - Una **varianza baja** sugiere una imagen más uniforme o desenfocada (baja frecuencia).

# **Ventaja:**  
# Esta función es versátil porque permite medir la alta frecuencia con distintos filtros (Gaussiano, media, etc.) simplemente pasándolos como parámetro.

def medir_alta_frecuencia(img_gray, funcion_filtro, ksize=5):
    """
    Calcula una medida de 'energía' (varianza) de la imagen de alta frecuencia.
    Retorna la varianza resultante.
    """
    hf = funcion_filtro(img_gray, ksize=ksize)
    return np.var(hf)