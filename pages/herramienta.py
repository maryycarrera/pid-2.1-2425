import streamlit as st

def main():
    st.title("Herramienta de Comparación de Nitidez")

    st.markdown(
        """
        **Instrucciones**:  
        1. Selecciona **al menos 2** imágenes (arrástralas o selecciónalas manualmente).  
        2. Escoge el tipo de filtro que se aplicará para estimar la nitidez.  
        3. (En el futuro) Podrás procesar las imágenes para obtener cuál es la menos borrosa.
        """
    )
    
    # Selector de archivos (permite múltiples archivos)
    imagenes_subidas = st.file_uploader(
        "Sube tus imágenes (formato PNG o JPG):",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if imagenes_subidas:
        st.write(f"Has subido {len(imagenes_subidas)} archivo(s).")

    # Validar que se subieron al menos 2 imágenes
    if len(imagenes_subidas) < 2:
        st.warning("Necesitas subir al menos 2 imágenes para comparar.")
    else:
        # Selector de filtro (radio buttons o selectbox)
        filtro = st.radio(
            "Elige el filtro para estimar la nitidez:",
            ("Gaussiano", "Media", "Mediana")
        )

        # (Opcional) Mostramos las imágenes subidas como vista previa
        st.write("Vista previa de imágenes subidas:")
        cols = st.columns(2)  # 2 columnas para mostrar (puedes ajustar)

        for i, img in enumerate(imagenes_subidas):
            # Convertir a un formato legible por Streamlit
            # (no hace el filtrado, solo para mostrar la imagen original)
            bytes_data = img.read()
            cols[i % 2].image(bytes_data, caption=img.name)

        # Botón (en el futuro haría el procesamiento)
        if st.button("Procesar imágenes"):
            st.write(f"Aplicando filtro {filtro} a las imágenes...")
            st.info("Aquí irá la lógica de procesamiento en el futuro.")

def run():
    main()

if __name__ == "__main__":
    run()
