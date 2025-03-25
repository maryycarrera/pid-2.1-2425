import streamlit as st

def main():
    st.set_page_config(page_title="Filtro de Imágenes", layout="centered", initial_sidebar_state="collapsed")

    st.title("Selector de herramientas")
    st.write(
        """
        Esta aplicación te ofrece dos herramientas:
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
