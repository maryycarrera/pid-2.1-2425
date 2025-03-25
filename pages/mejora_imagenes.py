import streamlit as st
import numpy as np
import cv2

def modificar_brillo(rgb, m0):
    """
    Modifica el brillo de una imagen RGB multiplicando cada canal por m0
    """
    return np.clip(rgb * m0, 0, 255).astype(np.uint8)

def calcular_b_promedio(imagen_rgb, ventana=20):
    # Convertir a espacio de color LAB
    lab = cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2LAB)
    # Extraer canal L (luminosidad)
    luminosidad = lab[:,:,0].astype(np.float32)
    # Calcular brillo promedio en el vecindario
    kernel = np.ones((ventana, ventana), np.float32) / (ventana * ventana)
    b_promedio = cv2.filter2D(luminosidad, -1, kernel)
    return b_promedio

def mejora_contraste(imagen_rgb, k, ventana=20):
    """
    Implementa la mejora de contraste preservando las coordenadas cromáticas
    """
    # Convertir a float para cálculos
    imagen_float = imagen_rgb.astype(np.float32) / 255.0
    
    # Convertir a espacio de color LAB
    lab_img = cv2.cvtColor(imagen_float, cv2.COLOR_RGB2LAB)
    
    # Extraer canal L (luminosidad)
    L = lab_img[:,:,0]
    
    # Calcular luminosidad promedio en el vecindario usando la imagen LAB
    b_promedio = calcular_b_promedio(lab_img, ventana)
    
    # Aplicar la fórmula de mejora de contraste
    epsilon = 1e-10
    ratio = np.maximum(L / (b_promedio + epsilon), 0)
    nuevo_L = b_promedio * np.power(ratio, k)
    
    # Limitar valores al rango válido
    nuevo_L = np.clip(nuevo_L, 0, 100)
    
    # Reemplazar canal L
    lab_img[:,:,0] = nuevo_L
    
    # Convertir de vuelta a RGB
    resultado = cv2.cvtColor(lab_img, cv2.COLOR_LAB2RGB) * 255.0
    
    # Retornar como uint8
    return np.clip(resultado, 0, 255).astype(np.uint8)

def main():
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
                min_value=0.0,
                max_value=5.0,
                value=1.0,
                step=0.1
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
            img_modificada = mejora_contraste(img_rgb, contraste)

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