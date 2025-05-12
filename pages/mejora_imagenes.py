import streamlit as st
import numpy as np
import cv2

MATRIZ_toDEF = np.array([[0.2053, 0.7125, 0.4670],
                        [1.8537, -1.2797, -0.4429],
                        [-0.3655, 1.0120, -0.6014]])
MATRIZ_toXYZ = np.array([[0.6712, 0.4955, 0.1540],
                        [0.7061, 0.0248, 0.5223],
                        [0.7689, -0.2556, -0.8645]])

def calc_metricas_cohen(X, Y, Z):
    alto, ancho = X.shape
    # Stack y reshape en una matriz (N, 3)
    pixels_xyz = np.stack([X, Y, Z], axis=-1).reshape(-1, 3)
    # Aplicar la matriz DEF
    cohen = pixels_xyz @ MATRIZ_toDEF.T  # Resultado (N, 3)
    return cohen.reshape(alto, ancho, 3)

def calc_bch_to_xyz(B, C, H):
    alto, ancho = B.shape
    # Stack y reshape en una matriz (N, 3)
    pixels_bch = np.stack([B, C, H], axis=-1).reshape(-1, 3)
    # Aplicar la matriz XYZ
    xyz = pixels_bch @ MATRIZ_toXYZ.T  # Resultado (N, 3)
    return xyz.reshape(alto, ancho, 3)

def obtener_brillo_valores_def(X, Y, Z):
    cohen = calc_metricas_cohen(X, Y, Z)
    D, E, F = cohen[:, :, 0], cohen[:, :, 1], cohen[:, :, 2]
    B = np.sqrt(D**2 + E**2 + F**2)
    return B.mean(), D, E, F

def obtener_def_imagen(imagen_rgb):
    imagen_float = imagen_rgb.astype(np.float32) / 255.0

    X, Y, Z = cv2.split(cv2.cvtColor(imagen_float, cv2.COLOR_RGB2XYZ))
    
    _, D, E, F = obtener_brillo_valores_def(X, Y, Z)
    return D, E, F

def modificar_brillo(imagen_rgb, ev,):
    """
    Implementa la mejora de brillo preservando las coordenadas cromáticas
    según la fórmula (5) del paper
    """
    # Obtener componentes D, E, F
    D, E, F = obtener_def_imagen(imagen_rgb)
    
    # Calcular brillo como la norma euclidiana de D, E, F
    epsilon = 1e-10
    brillo = np.sqrt(D**2 + E**2 + F**2)
    
    # Calcular C y H según las fórmulas del modelo BCH
    # C = arccos(D/B)
    C = np.arccos(np.clip(D / (brillo + epsilon), -1.0, 1.0))
    
    # H = arctan2(F, E) - Usando arctan2 para obtener el ángulo completo en el rango [-π, π]
    sin_C = np.sin(C)
    # Evitar división por cero
    mask = sin_C > epsilon
    H = np.zeros_like(C)
    
    # E = B*sin(C)*cos(H),  F = B*sin(C)*sin(H)
    # tan(H) = F/E  →  H = arctan2(F, E)
    # Usar arctan2 para determinar el ángulo correctamente en todos los cuadrantes
    H[mask] = np.arctan2(F[mask], E[mask])
        
    # Aplicar la fórmula de mejora de brillo
    nuevo_B = np.power(2, ev) * brillo
    
    # Limitar valores al rango válido
    nuevo_B = np.clip(nuevo_B, 0, 255)
    
    # Reconstruir D, E, F usando las fórmulas del modelo BCH
    # D = B * cos(C)
    nuevo_D = nuevo_B * np.cos(C)
    # E = B * sin(C) * cos(H)
    nuevo_E = nuevo_B * np.sin(C) * np.cos(H)
    # F = B * sin(C) * sin(H)
    nuevo_F = nuevo_B * np.sin(C) * np.sin(H)
    
    # Convertir de DEF a XYZ
    nuevoXYZ = calc_bch_to_xyz(nuevo_D, nuevo_E, nuevo_F)
    
    # Asegurar que nuevoXYZ esté en el formato correcto
    nuevoXYZ = nuevoXYZ.astype(np.float32)
    
    # Convertir de vuelta a RGB
    resultado = cv2.cvtColor(nuevoXYZ, cv2.COLOR_XYZ2RGB) * 255
    
    # Retornar como uint8
    return np.clip(resultado, 0, 255).astype(np.uint8)

def calcular_b_promedio(imagen_rgb, ventana=15):
    """
    Calcula el brillo promedio en un vecindario para cada píxel
    
    Args:
        imagen_rgb: Imagen en formato RGB
        ventana: Tamaño de la ventana para el promediado (ventana x ventana)
    
    Returns:
        Matriz con el brillo promedio para cada píxel
    """
    # Obtener componentes D, E, F
    D, E, F = obtener_def_imagen(imagen_rgb)
    
    # Calcular brillo como la norma euclidiana de D, E, F
    brillo = np.sqrt(D**2 + E**2 + F**2)
    
    # Aplicar filtro de promedio con la ventana especificada
    kernel = np.ones((ventana, ventana), np.float32) / (ventana * ventana)
    b_promedio = cv2.filter2D(brillo, -1, kernel)
    
    return b_promedio

def modificar_contraste(imagen_rgb, k, ventana=15):
    """
    Implementa la mejora de contraste preservando las coordenadas cromáticas
    según la fórmula (9) del paper
    """
    # Obtener componentes D, E, F
    D, E, F = obtener_def_imagen(imagen_rgb)
    
    # Calcular brillo como la norma euclidiana de D, E, F
    epsilon = 1e-10
    brillo = np.sqrt(D**2 + E**2 + F**2)
    
    # Calcular C y H según las fórmulas del modelo BCH
    # C = arccos(D/B)
    C = np.arccos(np.clip(D / (brillo + epsilon), -1.0, 1.0))
    
    # H = arctan2(F, E) - Usando arctan2 para obtener el ángulo completo en el rango [-π, π]
    sin_C = np.sin(C)
    # Evitar división por cero
    mask = sin_C > epsilon
    H = np.zeros_like(C)
    
    # E = B*sin(C)*cos(H),  F = B*sin(C)*sin(H)
    # tan(H) = F/E  →  H = arctan2(F, E)
    # Usar arctan2 para determinar el ángulo correctamente en todos los cuadrantes
    H[mask] = np.arctan2(F[mask], E[mask])
    
    # Calcular luminosidad promedio en el vecindario
    b_promedio = calcular_b_promedio(imagen_rgb, ventana)
    
    # Aplicar la fórmula de mejora de contraste
    ratio = brillo / (b_promedio + epsilon)
    nuevo_B = b_promedio * np.power(ratio, k)
    
    # Limitar valores al rango válido
    nuevo_B = np.clip(nuevo_B, 0, 255)
    
    # Reconstruir D, E, F usando las fórmulas del modelo BCH
    # D = B * cos(C)
    nuevo_D = nuevo_B * np.cos(C)
    # E = B * sin(C) * cos(H)
    nuevo_E = nuevo_B * np.sin(C) * np.cos(H)
    # F = B * sin(C) * sin(H)
    nuevo_F = nuevo_B * np.sin(C) * np.sin(H)
    
    # Convertir de DEF a XYZ
    nuevoXYZ = calc_bch_to_xyz(nuevo_D, nuevo_E, nuevo_F)
    
    # Asegurar que nuevoXYZ esté en el formato correcto
    nuevoXYZ = nuevoXYZ.astype(np.float32)
    
    # Convertir de vuelta a RGB
    resultado = cv2.cvtColor(nuevoXYZ, cv2.COLOR_XYZ2RGB) * 255
    
    # Retornar como uint8
    return np.clip(resultado, 0, 255).astype(np.uint8)

def main():
    st.set_page_config(page_title="Mejora de Imágenes")
    st.title("Herramienta de mejora de imágenes")
    
    # Subida de imagen para mejora
    imagen_mejora = st.file_uploader(
        "Sube una imagen para mejorar:",
        type=["png", "jpg", "jpeg"],
        key="mejora_uploader"
    )

    if imagen_mejora:
        # Read image
        file_bytes = np.asarray(bytearray(imagen_mejora.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        # Create two columns for original and processed image
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Imagen Original")
            st.image(img_rgb)

        # Select adjustment type
        tipo_ajuste = st.radio(
            "¿Qué quieres ajustar?",
            ("Brillo", "Contraste")
        )

        if tipo_ajuste == "Brillo":
            # Brightness adjustment
            brillo = st.slider(
                "Ajuste de Brillo",
                min_value=-1.0,
                max_value=1.0,
                value=0.0,
                step=0.05
            )
            img_modificada = modificar_brillo(img_rgb, brillo)
        else:  # Contraste
            # Contrast adjustment
            contraste = st.slider(
                "Ajuste de Contraste",
                min_value=0.1,
                max_value=5.0,
                value=1.0,
                step=0.1
            )
            img_modificada = modificar_contraste(img_rgb, contraste)

        with col2:
            st.subheader("Imagen Modificada")
            st.image(img_modificada)

        # Modify download button to download directly
        img_save = cv2.cvtColor(img_modificada, cv2.COLOR_RGB2BGR)
        _, buffer = cv2.imencode('.png', img_save)
        st.download_button(
            label="Descargar imagen modificada",
            data=buffer.tobytes(),
            file_name=f"modificada_{imagen_mejora.name}",
            mime="image/png"
        )

    else:
        st.warning("Sube una imagen para empezar.")

def run():
    main()

if __name__ == "__main__":
    run()