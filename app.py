
import streamlit as st
import replicate
import os

# Configuración de la página
st.set_page_config(page_title="Edición Casera VIP")

st.title("📸 | Edición Casera VIP")
st.write("### **Tus fotos con estilo natural y real de celular**")

# Selector de origen de foto para evitar reinicios en el cel
opcion = st.radio("¿Cómo quieres subir tu foto?", ("Elegir de mi galería", "Tomar una foto nueva"))

if opcion == "Elegir de mi galería":
    uploaded_file = st.file_uploader("Sube tu foto de la galería", type=['jpg', 'jpeg', 'png'])
else:
    uploaded_file = st.camera_input("Tómate una foto")

# Mostrar la foto si ya se cargó
if uploaded_file is not None:
    st.image(uploaded_file, caption="Foto lista para procesar")

prompt = st.text_input("¿Cómo quieres la escena?", placeholder="Ej: En la sala con playera gris...")

if st.button("⚡ Generar Prueba Gratis"):
    if uploaded_file is not None and prompt:
        with st.spinner("La IA está trabajando..."):
            try:
                # El modelo ultra-realista de Replicate
                output = replicate.run(
                    "sg161222/realvisxl-v4.0-lightning:5f24084160c908950a6ff357bb57c4f6ab7998f95d4ed792d375c7b74ec1dca0",
                    input={
                        "image": uploaded_file,
                        "prompt": f"A raw, natural cell phone picture, {prompt}, highly detailed, realistic skin texture",
                        "negative_prompt": "luxury, glamour, fake, deformed, extra limbs, studio lighting",
                        "num_inference_steps": 7,
                        "guidance_scale": 1.5
                    }
                )
                if output:
                    st.image(output[0], caption="Resultado final")
                    st.success("¡Tu foto está lista!")
            except Exception as e:
                st.error(f"Hubo un detalle con la generación: {e}")
    else:
        st.warning("Por favor, sube una foto y escribe una escena primero.")
