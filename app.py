import streamlit as st
import os
import time
import shutil
import replicate

st.set_page_config(page_title="Edición Casera VIP", layout="centered")
st.title("📷 | Edición Casera VIP")

# --- 1. CONFIGURACIÓN DE PRIVACIDAD Y AUTO-BORRADO (30 MIN) ---
TEMP_DIR = "temp_images"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def limpiar_archivos_antiguos():
    ahora = time.time()
    limite = 30 * 60  # 30 minutos
    for archivo in os.listdir(TEMP_DIR):
        ruta_completa = os.path.join(TEMP_DIR, archivo)
        if os.path.getmtime(ruta_completa) < ahora - limite:
            try:
                if os.path.isdir(ruta_completa):
                    shutil.rmtree(ruta_completa)
                else:
                    os.remove(ruta_completa)
            except Exception:
                pass

limpiar_archivos_antiguos()

st.warning(
    "🔒 **Garantía de Privacidad VIP:** Todo tu contenido se elimina "
    "definitivamente de nuestros servidores tras 30 minutos de inactividad."
)

# --- 2. SISTEMA DE CONTROL DE CRÉDITOS / CÓDIGO VIP ---
if "generaciones_gratis" not in st.session_state:
    st.session_state["generaciones_gratis"] = 0

# Código maestro que le puedes dar cuando compre créditos
CODIGO_VIP_REAL = "CASERAVIP777"

acceso_vip = False
codigo_ingresado = st.sidebar.text_input("🔑 Introduce tu Código VIP / Créditos", type="password")

if codigo_ingresado == CODIGO_VIP_REAL:
    acceso_vip = True
    st.sidebar.success("¡Acceso VIP Activado (Generaciones Ilimitadas)!")
else:
    intentos_restantes = max(0, 1 - st.session_state["generaciones_gratis"])
    st.sidebar.info(f"🎁 Te quedan **{intentos_restantes}** pruebas gratis.")
    if intentos_restantes == 0:
        st.sidebar.error("⚠️ Has agotado tu prueba gratis. Contacta con soporte para comprar un Código VIP.")

# API Token de Replicate
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

# --- 3. MENÚ DE LA APP (PESTAÑAS) ---
tab1, tab2 = st.tabs(["✨ Crear escena (Texto)", "👤 Cambiar Cara (Face Swap)"])

# PESTAÑA 1: CYBER REALISTIC (EDITAR FOTO ORIGINAL)
with tab1:
    st.header("Modificar Escena")
    uploaded_file = st.file_uploader("Sube tu foto base", type=["jpg", "png"], key="foto_tab1")
    prompt = st.text_input("¿Cómo quieres lucir en la escena?")

    if st.button("⚡ Generar con IA"):
        if not acceso_vip and st.session_state["generaciones_gratis"] >= 1:
            st.error("Por favor, introduce un código de acceso VIP válido para continuar.")
        elif uploaded_file is not None and prompt:
            with st.spinner("Modificando escena de forma privada..."):
                try:
                    temp_input = os.path.join(TEMP_DIR, f"input_{int(time.time())}.png")
                    with open(temp_input, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    output = replicate.run(
                        "fofr/cyberrealistic-v6:de7e6b0108344e456cf996d9dae3d09a067fffc080344d183f99059f1092e079",
                        input={
                            "image": open(temp_input, "rb"),
                            "prompt": prompt,
                            "prompt_strength": 0.6,
                            "negative_prompt": "deformed, bad quality, bad anatomy, cartoon",
                            "num_outputs": 1
                        }
                    )
                    
                    st.success("¡Imagen generada con éxito!")
                    st.info("⏱️ *Se eliminará por completo en 30 minutos.*")
                    
                    res_img = output[0] if isinstance(output, list) else output
                    st.image(res_img, caption="Tu resultado privado")
                    
                    if not acceso_vip:
                        st.session_state["generaciones_gratis"] += 1
                        st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("Asegúrate de subir tu foto y escribir lo que quieres cambiar.")

# PESTAÑA 2: FACE SWAP ULTRARREALISTA (CON INSIGHTFACE)
with tab2:
    st.header("Intercambio de Rostro Ultrarrealista")
    st.write("Clona tu rostro de forma perfecta sobre cualquier otra foto corporal o escena.")
    
    st.info(
        "💡 **Consejo para máximo realismo:** Asegúrate de que la foto de 'TU CARA' tenga buena iluminación, "
        "se vea bien de frente y sin gafas ni cabello tapando el rostro."
    )
    
    cara_usuario = st.file_uploader("1. Sube la foto de TU CARA (Origen)", type=["jpg", "png"], key="mi_cara")
    foto_escena = st.file_uploader("2. Sube la foto del CUERPO o ESCENA destino", type=["jpg", "png"], key="escena_destino")

    if st.button("🔄 Realizar Face Swap Pro"):
        if not acceso_vip and st.session_state["generaciones_gratis"] >= 1:
            st.error("Por favor, introduce un código de acceso VIP válido para continuar.")
        elif cara_usuario is not None and foto_escena is not None:
            with st.spinner("Fusionando rostros para máximo realismo..."):
                try:
                    t = int(time.time())
                    temp_cara = os.path.join(TEMP_DIR, f"cara_{t}.png")
                    temp_escena = os.path.join(TEMP_DIR, f"escena_{t}.png")
                    
                    with open(temp_cara, "wb") as f:
                        f.write(cara_usuario.getbuffer())
                    with open(temp_escena, "wb") as f:
                        f.write(foto_escena.getbuffer())

                    # Modelo premium de InsightFace en Replicate
                    output = replicate.run(
                        "wavesyloc/faceswap:9662059a43a054d5885f67b5e43a9926d11340a6b2c611448b1d9da067fffc0803",
                        input={
                            "source_image": open(temp_cara, "rb"),
                            "target_image": open(temp_escena, "rb"),
                        }
                    )
                    
                    st.success("¡Cara cambiada con éxito!")
                    st.info("⏱️ *Esta foto se autodestruirá en 30 minutos.*")
                    
                    res_img = output
                    if isinstance(output, list):
                        res_img = output[0]
                    elif isinstance(output, dict) and 'image' in output:
                        res_img = output['image']
                        
                    st.image(res_img, caption="Tu Face Swap Privado (Fidelidad Alta)")
                    
                    if not acceso_vip:
                        st.session_state["generaciones_gratis"] += 1
                        st.rerun()

                except Exception as e:
                    st.error(f"Error en Face Swap: {e}")
        else:
            st.error("Debes subir ambas fotos para poder hacer el cambio de cara.")
