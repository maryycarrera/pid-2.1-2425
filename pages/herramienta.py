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

def main():
    st.title("Herramienta de Comparación de Nitidez")

    # Subida de imágenes
    imagenes_subidas = st.file_uploader(
        "Sube tus imágenes (mínimo 2) en formato PNG/JPG:",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    # Mostrar cuántos archivos se han subido
    if imagenes_subidas:
        st.write(f"Has subido {len(imagenes_subidas)} archivo(s).")

    # Si quieres mostrar una "previsualización" de cada imagen, hazlo aquí
    # (y luego rebobina el archivo para cuando se procese al hacer clic en el botón).
    if imagenes_subidas:
        st.write("### Vista previa de imágenes subidas:")
        cols = st.columns(3)  # 3 columnas
        for i, archivo in enumerate(imagenes_subidas):
            bytes_data = archivo.read()
            with cols[i % 3]:  # Cambiamos de columna cada 3 imágenes
                st.image(bytes_data, caption=archivo.name, width=200)
            archivo.seek(0)  # IMPORTANTE: rebobinar para que se pueda procesar más tarde

    # Necesitamos al menos 2 imágenes para comparar
    if not imagenes_subidas or len(imagenes_subidas) < 2:
        st.warning("Sube al menos 2 imágenes para poder comparar.")
        return

    # Elección de filtro
    filtro_seleccionado = st.radio(
        "Elige el filtro para estimar la nitidez:",
        ("Gaussiano", "Media", "Mediana", "Wavelet")
    )

    # Botón para procesar
    if st.button("Procesar y encontrar la menos borrosa"):
        # Mapear la selección del usuario a la función de filtro
        if filtro_seleccionado == "Gaussiano":
            filtro_func = filtro_paso_alto_gaussiano
        elif filtro_seleccionado == "Media":
            filtro_func = filtro_paso_alto_media
        elif filtro_seleccionado == "Mediana":
            filtro_func = filtro_paso_alto_mediana
        else:
            filtro_func = filtro_paso_alto_wavelet

        # Aquí almacenaremos la mayor varianza y la imagen "ganadora"
        mejor_varianza = -1
        mejor_imagen = None
        mejor_nombre = None

        for archivo in imagenes_subidas:
            # IMPORTANTE: rebobinar otra vez porque file_uploader "pierde" el cursor 
            # si ya lo leíste antes en la sección de previsualización.
            archivo.seek(0)

            # Leer en OpenCV
            file_bytes = np.asarray(bytearray(archivo.read()), dtype=np.uint8)
            img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

            # Calcular varianza de alta frecuencia
            varianza = medir_alta_frecuencia(img_gray, filtro_func, ksize=5)

            # Comprobamos si es la mejor hasta ahora
            if varianza > mejor_varianza:
                mejor_varianza = varianza
                mejor_imagen = img_bgr
                mejor_nombre = archivo.name

        # Mostramos la imagen con mayor valor (menos borrosa)
        if filtro_seleccionado == "Wavelet":
            st.success(f"La imagen con mayor nitidez (según coeficiente medio) es: {mejor_nombre}")
            st.image(cv2.cvtColor(mejor_imagen, cv2.COLOR_BGR2RGB), 
                    caption=f"{mejor_nombre} (coeficiente medio = {mejor_varianza:.3f})")
        else:
            st.success(f"La imagen con mayor nitidez (según varianza) es: {mejor_nombre}")
            st.image(cv2.cvtColor(mejor_imagen, cv2.COLOR_BGR2RGB), 
                    caption=f"{mejor_nombre} (varianza = {mejor_varianza:.3f})")

def run():
    main()

if __name__ == "__main__":
    run()
