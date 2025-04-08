import cv2
import numpy as np

def calcular_varianza_histograma(img_gray):
    """
    Calcula la varianza en el histograma para saber el contraste de la imagen 
    Retorna:
        - Varianza (dispersión de intensidades).
    """
       
    # Calcular histograma
    hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256]).flatten()
    
    total_pixeles = img_gray.size
    valores = np.arange(256) # Valores posibles de intensidad (0-255)
    media = np.sum(valores * hist) / total_pixeles
    varianza = np.sum(((valores - media) ** 2) * hist) / total_pixeles

    return varianza