import streamlit as st
import replicate
import os

# Configuración de la página para que se vea chida en celulares
st.set_page_config(page_title="Edición Casera VIP", page_icon="📸", layout="centered")

st.title("📸 | Edición Casera VIP")
st.write("### **Tus fotos con estilo natural y real de celular**")

# Subir la foto del cliente
uploaded_file = st.file_uploader("Sube tu foto aquí", type=["jpg", "jpeg", "png"])
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
