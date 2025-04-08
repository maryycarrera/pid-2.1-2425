import streamlit as st
import numpy as np
import cv2
from utils.contrast import calcular_varianza_histograma
from utils.filters import (
    filtro_paso_alto_gaussiano,
    filtro_paso_alto_media,
    filtro_paso_alto_mediana,
    obtener_calidad_imagen,
    medir_alta_frecuencia
)

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
            ("Nitidez", "Contraste")
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
                    filtro_func = obtener_calidad_imagen

                mejor_valor = -1
                mejor_imagen = None
                mejor_nombre = None

                for archivo in imagenes_subidas:
                    archivo.seek(0)
                    file_bytes = np.asarray(bytearray(archivo.read()), dtype=np.uint8)
                    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                    if filtro_seleccionado == "Wavelet":
                        img_YCbCr = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
                        varianza = medir_alta_frecuencia(img_YCbCr, filtro_func)
                    else: 
                        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
                        varianza = medir_alta_frecuencia(img_gray, filtro_func, ksize=5)

                    if varianza > mejor_valor:
                        mejor_valor = varianza
                        mejor_imagen = img_bgr
                        mejor_nombre = archivo.name

                if filtro_seleccionado == "Wavelet":
                    st.success(f"La imagen con mayor puntuación de calidad es: {mejor_nombre}")
                    st.image(cv2.cvtColor(mejor_imagen, cv2.COLOR_BGR2RGB), 
                            caption=f"{mejor_nombre} (Puntuación de calidad = {mejor_valor:.3f})")
                else:
                    st.success(f"La imagen con mayor nitidez (según varianza) es: {mejor_nombre}")
                    st.image(cv2.cvtColor(mejor_imagen, cv2.COLOR_BGR2RGB),
                            caption=f"{mejor_nombre} (varianza = {mejor_valor:.3f})")

        else:  # Contraste selected
            # Elección de objetivo para contraste
            objetivo_seleccionado = st.radio(
                "Elige si quieres obtener la imagen con mayor o con menor contraste:",
                ("Mayor", "Menor")
            )
            st.write("Se calculará la varianza de los histogramas de las imágenes en escala de grises para calcular el contraste.")
            if st.button(f"Procesar y encontrar la imagen con {objetivo_seleccionado.lower()} contraste"):
                if objetivo_seleccionado == "Mayor":
                    mejor_contraste = -1
                else:
                    mejor_contraste = float('inf')
                mejor_imagen = None
                mejor_nombre = None

                for archivo in imagenes_subidas:
                    archivo.seek(0)
                    file_bytes = np.asarray(bytearray(archivo.read()), dtype=np.uint8)
                    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

                    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
                    contraste = calcular_varianza_histograma(img_gray)

                    if objetivo_seleccionado == "Mayor":
                        if contraste > mejor_contraste:
                            mejor_contraste = contraste
                            mejor_imagen = img_bgr
                            mejor_nombre = archivo.name
                    else:
                        if contraste < mejor_contraste:
                            mejor_contraste = contraste
                            mejor_imagen = img_bgr
                            mejor_nombre = archivo.name

                st.success(f"La imagen con {objetivo_seleccionado.lower()} contraste (según varianza) es: {mejor_nombre}")
                st.image(cv2.cvtColor(mejor_imagen, cv2.COLOR_BGR2RGB),
                        caption=f"{mejor_nombre} (varianza = {mejor_contraste:.3f})")

    else:
        st.warning("Sube al menos 2 imágenes para poder comparar.")

def run():
    main()

if __name__ == "__main__":
    run()