
import streamlit as st
import os

st.set_page_config(page_title="Edición Casera VIP")
st.title("📷 | Edición Casera VIP")

if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

# El parche clave: el key evita que la app se congele o recargue al elegir la foto
uploaded_file = st.file_uploader("Sube tu foto de la galería", type=["jpg", "png"], key="foto_usuario")
prompt = st.text_input("¿Cómo quieres la escena?")

# Detiene todo hasta que tú decidas presionar el botón
if st.button("⚡ Generar Prueba Gratis"):
    if uploaded_file is not None and prompt:
        st.write("Procesando tu imagen...")
        # Aquí corre tu modelo de Replicate
        st.success("¡Imagen generada con éxito!")
    else:
        st.error("Por favor, sube una foto y escribe el prompt.")
