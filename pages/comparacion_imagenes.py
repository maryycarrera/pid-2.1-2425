import streamlit as st
import numpy as np
import cv2
from utils.filters import (
    filtro_paso_alto_gaussiano,
    filtro_paso_alto_media,
    filtro_paso_alto_mediana,
    filtro_paso_alto_wavelet,
    medir_alta_frecuencia
)

# Add BCH matrix constant
MATRIZ_BCH = np.array([[0.2053, 0.7125, 0.4670],
                       [1.8537, -1.2797, -0.4429],
                       [-0.3655, 1.0120, -0.6014]])

def main():
    st.title("Herramienta de comparación de imágenes")
    
    # Subida de imágenes para comparación
    imagenes_subidas = st.file_uploader(
        "Sube tus imágenes (mínimo 2) en formato PNG/JPG:",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="nitidez_uploader"
    )

    if imagenes_subidas:
        st.write(f"Has subido {len(imagenes_subidas)} archivo(s).")

        st.write("### Vista previa de imágenes subidas:")
        cols = st.columns(3)
        for i, archivo in enumerate(imagenes_subidas):
            bytes_data = archivo.read()
            with cols[i % 3]:
                st.image(bytes_data, caption=archivo.name, width=200)
            archivo.seek(0)

        # First, choose comparison type
        tipo_comparacion = st.radio(
            "¿Qué quieres comparar?",
            ("Nitidez", "Brillo")
        )

        if tipo_comparacion == "Nitidez":
            # Elección de filtro para nitidez
            filtro_seleccionado = st.radio(
                "Elige el filtro para estimar la nitidez:",
                ("Gaussiano", "Media", "Mediana", "Wavelet")
            )
            
            if st.button("Procesar y encontrar la imagen más nítida"):
                # Mapear la selección del usuario a la función de filtro
                if filtro_seleccionado == "Gaussiano":
                    filtro_func = filtro_paso_alto_gaussiano
                elif filtro_seleccionado == "Media":
                    filtro_func = filtro_paso_alto_media
                elif filtro_seleccionado == "Mediana":
                    filtro_func = filtro_paso_alto_mediana
                else:
                    filtro_func = filtro_paso_alto_wavelet

                mejor_valor = -1
                mejor_imagen = None
                mejor_nombre = None

                for archivo in imagenes_subidas:
                    archivo.seek(0)
                    file_bytes = np.asarray(bytearray(archivo.read()), dtype=np.uint8)
                    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

                    varianza = medir_alta_frecuencia(img_gray, filtro_func, ksize=5)

                    if varianza > mejor_valor:
                        mejor_valor = varianza
                        mejor_imagen = img_bgr
                        mejor_nombre = archivo.name

                if filtro_seleccionado == "Wavelet":
                    st.success(f"La imagen con mayor nitidez (según coeficiente medio) es: {mejor_nombre}")
                    st.image(cv2.cvtColor(mejor_imagen, cv2.COLOR_BGR2RGB), 
                            caption=f"{mejor_nombre} (coeficiente medio = {mejor_valor:.3f})")
                else:
                    st.success(f"La imagen con mayor nitidez (según varianza) es: {mejor_nombre}")
                    st.image(cv2.cvtColor(mejor_imagen, cv2.COLOR_BGR2RGB), 
                            caption=f"{mejor_nombre} (varianza = {mejor_valor:.3f})")

        else:  # Brillo selected
            st.write("Se utilizará el método BCH para estimar el brillo")
            if st.button("Procesar y encontrar la imagen más brillante (método BCH)"):
                mejor_brillo = -1
                mejor_imagen = None
                mejor_nombre = None

                for archivo in imagenes_subidas:
                    archivo.seek(0)
                    file_bytes = np.asarray(bytearray(archivo.read()), dtype=np.uint8)
                    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

                    # Split channels and calculate BCH brightness
                    R, G, B = cv2.split(img_rgb)
                    alto, ancho = R.shape
                    pixels_xyz = np.stack([R, G, B], axis=-1).reshape(-1, 3)
                    cohen = pixels_xyz @ MATRIZ_BCH.T
                    cohen = cohen.reshape(alto, ancho, 3)
                    D, E, F = cohen[:, :, 0], cohen[:, :, 1], cohen[:, :, 2]
                    brillo = np.sqrt(D**2 + E**2 + F**2).mean()

                    if brillo > mejor_brillo:
                        mejor_brillo = brillo
                        mejor_imagen = img_bgr
                        mejor_nombre = archivo.name

                st.success(f"La imagen con mayor brillo (método BCH) es: {mejor_nombre}")
                st.image(cv2.cvtColor(mejor_imagen, cv2.COLOR_BGR2RGB), 
                        caption=f"{mejor_nombre} (brillo BCH = {mejor_brillo:.3f})")

    else:
        st.warning("Sube al menos 2 imágenes para poder comparar.")

def run():
    main()

if __name__ == "__main__":
    run()