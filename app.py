import streamlit as st

def main():
    st.set_page_config(page_title="Filtro de Imágenes", layout="centered", initial_sidebar_state="collapsed")

    st.title("Comparación y Mejora de Imágenes en base a sus Hiperparámetros de Calidad")
    st.write(
        """
        ¡Bienvenid@ a nuestra aplicación!\n
        ¿No puedes elegir entre dos imágenes? ¿Quieres saber cuál de las dos tiene mayor calidad? ¿O simplemente quieres mejorar la calidad de una imagen? ¡No te preocupes! Esta aplicación te ayudará a comparar y mejorar imágenes en base a sus hiperparámetros de calidad.\n
        ¿A qué estás esperando? ¡Elige una herramienta!
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Comparación de imágenes"):
            st.switch_page("pages/comparacion_imagenes.py")
    with col2:
        if st.button("Mejora de imágenes"):
            st.switch_page("pages/mejora_imagenes.py")

if __name__ == "__main__":
    main()
