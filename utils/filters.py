import cv2
import numpy as np

def filtro_paso_alto_gaussiano(img_gray, ksize=5):
    """
    Retorna la imagen de altas frecuencias (original - suavizada con Gaussiano).
    """
    suavizada = cv2.GaussianBlur(img_gray, (ksize, ksize), 0)
    altas_frec = cv2.subtract(img_gray, suavizada)
    return altas_frec

def filtro_paso_alto_media(img_gray, ksize=5):
    """
    Retorna la imagen de altas frecuencias (original - suavizada con filtro de media).
    """
    suavizada = cv2.blur(img_gray, (ksize, ksize))
    altas_frec = cv2.subtract(img_gray, suavizada)
    return altas_frec

def filtro_paso_alto_mediana(img_gray, ksize=5):
    """
    Retorna la imagen de altas frecuencias (original - suavizada con filtro de mediana).
    """
    suavizada = cv2.medianBlur(img_gray, ksize)
    altas_frec = cv2.subtract(img_gray, suavizada)
    return altas_frec

def medir_alta_frecuencia(img_gray, filtro_func, ksize=5):
    """
    Aplica el filtro de paso alto (filtro_func) y retorna la varianza de la imagen filtrada.
    """
    hf = filtro_func(img_gray, ksize=ksize)
    return np.var(hf)
