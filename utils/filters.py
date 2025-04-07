import cv2
import numpy as np
import pywt
from scipy.ndimage import uniform_filter


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

def medir_alta_frecuencia(img, filtro_func, ksize=5):
    """
    Aplica el filtro de paso alto (filtro_func) y retorna:
    - Para wavelet: la puntuación de calidad
    - Para otros filtros: la varianza de la imagen filtrada
    """ 
    # Si es el filtro wavelet, devuelve la puntuacion de calidad

    if filtro_func == obtener_calidad_imagen:
        hf = filtro_func(img)
        return hf
    else:
        hf = filtro_func(img, ksize=ksize)
    # Para el resto de filtros, calcular la varianza como antes
    return np.var(hf)

################################################################################################
###Para wavelet, solo es necesario importar obtener_calidad_imagen(), el resto son auxiliares###
################################################################################################

def obtener_calidad_imagen(imagen_ycbcr, block_size = 8, epsilon=1e-6, alpha=1, wavelet='db1'):
    
    SubbandasDiagonales = obtener_subbandas_diagonales(imagen_ycbcr, wavelet)
    TY, TCb, TCr = obtener_matrices_T(SubbandasDiagonales, block_size , alpha)
    T_S = calcular_estimulo_total(TY, TCb, TCr, alpha)
    Smap = calcular_Smap(T_S, epsilon)
    BSmap = obtener_BSmap(Smap, block_size=8)
    Qs = np.max(BSmap)
    return Qs

def obtener_BSmap(Smap, block_size=8):
    """
    Elimina el borde del mapa de nitidez (Smap) en función del tamaño del bloque.
    """
    # El tamaño del borde a eliminar es block_size - 1 en cada dirección
    border_size = block_size - 1
    # Recortar el borde del Smap
    BSmap = Smap[border_size:-border_size, border_size:-border_size] if border_size > 0 else Smap

    return BSmap

def calcular_Smap(T_S, epsilon=1e-6):
    """
    Calcula la matriz Smap (mapa de nitidez) utilizando la ecuación dada:
    Smap(i, j) = abs[log(ε) + ε] / (abs[log(T_S(i, j)) + ε] + ε)
    """
    # Numerador: abs(log(epsilon) + epsilon)
    numerador = np.abs(np.log(epsilon) + epsilon)
    denominador = np.abs(np.log(T_S + epsilon)+ epsilon) # Denominador: abs(log(T_S) + epsilon) + epsilon
    # Calcular Smap
    Smap = numerador / denominador
    return Smap


def calcular_estimulo_total(TY, TCb, TCr, alpha=1):
    """
    Calcula el total stimulus T_S de la imagen usando la ecuación dada.
    """
    suma = (TY + TCb + TCr) / 3     # Sumar las matrices de los tres canales
    T_S = np.power(suma, 1/alpha)   # Calcular el total stimulus T_S
    
    return T_S

def obtener_matrices_T(SubbandasDiagonales, block_size = (8, 8), alpha=1):
    """
    Aplica la fórmula a cada canal para obtener TY, TCb, TCr.
    """
    T_out = []
    for i in range(3):
        #HH_subbandas[i] = HH_i.astype(np.float32)
        MH_i = obtener_MH_i(SubbandasDiagonales[i], block_size) # 1) Calcular MH (bloques no ) 
        S_i = obtener_S_i(SubbandasDiagonales[i], block_size)   # 2) Calcular S (bloques superpuestos)      
        T_i = calcular_matriz_T(MH_i, S_i, alpha)               # 3) Calcular T
        T_out.append(T_i)

    return T_out[0], T_out[1], T_out[2]  #Devuelve Ty, Tcb, Tcr
def calcular_matriz_T(MH_I, S_I, alpha=1):
    """Calcula la matriz T dada MH_I y S_I"""
    numerador = (MH_I ** alpha) * S_I
    denominador = np.sum(S_I) if np.sum(S_I) != 0 else 1.0

    return numerador / (denominador + 1e-8)  # evitar división por cero

def obtener_S_i(HH_i, block_size):
    """Calcula la desviación estándar local de bloques solapados."""
    media = uniform_filter(HH_i, size=block_size)  
    media_sq = uniform_filter(HH_i**2, size=block_size)
    return np.sqrt(np.maximum(media_sq - media**2, 0))

def blockwise_mean(HH_i, block_size):
    """Calcula la media por bloques no solapados."""
    h, w = HH_i.shape
    bs = block_size
    # Recortar imagen para que encaje con múltiplos del block size
    h_crop, w_crop = h - h % bs, w - w % bs
    img_cropped = HH_i[:h_crop, :w_crop]
    # Redimensionar y calcular la media por bloque
    blocks = img_cropped.reshape(h_crop // bs, bs, w_crop // bs, bs).mean(axis=(1, 3))
    # Expandir cada valor a su bloque original
    expanded = np.kron(blocks, np.ones((bs, bs)))  # expandir para restar luego
    # Rellenar para igualar tamaño original (útil en caso de que el tamaño de la imagen no sea dibisible por el tamaño del bloque)
    block_mean_full = np.zeros_like(HH_i)
    block_mean_full[:h_crop, :w_crop] = expanded
    return block_mean_full

def obtener_MH_i(HH_i, block_size):
    """ Calcula MH para una subbanda de alta frecuencia H, restando la media de bloques NO solapados."""
    block_mean = blockwise_mean(HH_i, block_size)
    return np.abs(HH_i - block_mean)

def obtener_subbandas_diagonales(imagen_ycbcr, wavelet='db1'):
    """
    Aplica la transformada wavelet a cada canal de la imagen YCbCr y extrae las subbandas diagonales (HH).
    """
    subbandas_HH = []
    canales = cv2.split(imagen_ycbcr)                                # Separar los canales Y, Cb, Cr 
    for canal in canales:                                            #Recorro los canales 
        coeficientes = pywt.wavedec2(canal, wavelet=wavelet, level=1)# Wavedec2 descompone la imagen en coeficientes de aproximación (LL), horizontal(HL), vertical(LH) y diagonal (HH)
        _, *detalles = coeficientes                                  # Extraer la subbanda diagonal (HH) en el nivel deseado
        HH = detalles[0][2]                                          # Accedemos a la subbanda HH en el nivel seleccionado
        subbandas_HH.append(HH)
    
    return subbandas_HH
