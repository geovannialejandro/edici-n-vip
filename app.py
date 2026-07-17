import streamlit as st
import replicate
import os

# Configuración de la página para que se vea chida en celulares
st.set_page_config(page_title="Edición Casera VIP", page_icon="📸", layout="centered")

st.title("📸 | Edición Casera VIP")
st.write("### **Tus fotos con estilo natural y real de celular**")

# Subir la foto del cliente
import streamlit as st

st.title("📸 | Edición Casera VIP")

# Creamos una opción para que elija cómo quiere subir la foto
opcion = st.radio("¿Cómo quieres subir tu foto?", ("Elegir de mi galería", "Tomar una foto nueva"))

foto = None

if opcion == "Elegir de mi galería":
    # El file_uploader para elegir archivos
    foto = st.file_uploader("Sube tu foto de la galería", type=['jpg', 'jpeg', 'png'])
else:
    # La cámara para tomar una foto nueva
    foto = st.camera_input("Tómate una foto")

# Si hay una foto, la mostramos
if foto is not None:
    st.image(foto, caption="Foto lista para procesar")
prompt = st.text_input("¿Cómo quieres la escena?", placeholder="Ej: En la sala con playera gris...")

if st.button("⚡ Generar Prueba Gratis", type="primary"):
    if uploaded_file is not None and prompt:
        with st.spinner("La IA está trabajando en tu foto... ⏳"):
            try:
                # El modelo ultra-realista que hace magia
                output = replicate.run(
                    "sg161222/realvisxl-v4.0:22a0b32c",
                    input={
                        "image": uploaded_file,
                        "prompt": f"A realistic raw phone selfie, look-alike face of the person, {prompt}, amateur snapshot, indoors, cozy home, natural lighting, casual, authentic skin texture",
                        "negative_prompt": "3d render, cartoon, studio lighting, plastic skin, fake, luxury, professional",
                        "num_inference_steps": 30,
                        "guidance_scale": 7.5
                    }
                )
                if output:
                    st.image(output[0], caption="Resultado Casero", use_container_width=True)
                    st.success("¡Tu prueba gratis está lista! 🚀")
            except Exception as e:
                st.error(f"Hubo un detalle: {e}")
    else:
        st.warning("Por favor, sube una foto y escribe qué quieres en la escena.")
