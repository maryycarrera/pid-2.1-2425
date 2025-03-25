import cv2
import numpy as np
import pywt

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

def filtro_paso_alto_wavelet(img_gray, ksize=5):  # ksize is ignored but kept for compatibility
    """
    Retorna el coeficiente medio de alta frecuencia usando transformada wavelet.
    """
    # Aplicar la transformada wavelet
    coeficientes = pywt.wavedec2(img_gray, wavelet='db1', level=1)
    
    # Obtener los coeficientes de alta frecuencia
    coefs_alta_frecuencia = coeficientes[1:]
    
    # Calcular coeficiente medio
    n_coef = 0
    total_coef = 0
    
    for i in coefs_alta_frecuencia:
        for j in i:
            n_coef += j.size
            total_coef += np.sum(np.abs(j))
    
    # Evitar división por cero
    if n_coef == 0:
        return 0.0
        
    # Retornar directamente el coeficiente medio
    return total_coef / n_coef

def medir_alta_frecuencia(img_gray, filtro_func, ksize=5):
    """
    Aplica el filtro de paso alto (filtro_func) y retorna:
    - Para wavelet: el coeficiente medio directamente
    - Para otros filtros: la varianza de la imagen filtrada
    """
    hf = filtro_func(img_gray, ksize=ksize)
    
    # Si es el filtro wavelet, ya devuelve el coeficiente medio
    if filtro_func == filtro_paso_alto_wavelet:
        return hf
    
    # Para el resto de filtros, calcular la varianza como antes
    return np.var(hf)
