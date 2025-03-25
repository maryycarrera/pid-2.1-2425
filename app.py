import streamlit as st

def main():
    st.set_page_config(page_title="Filtro de Imágenes", layout="centered", initial_sidebar_state="collapsed")

    # Center the title using markdown with HTML
    st.title("Selector de imágenes")
    st.write(
        """
        Esta aplicación te permite hacer una comparación de imágenes a partir de un parámetro de calidad para quedarte con la mejor de todas. 
        """
    )

    # Center align the button using columns
    if st.button("Prueba nuestra herramienta"):
        st.switch_page("pages/herramienta.py")

if __name__ == "__main__":
    main()
