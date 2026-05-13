import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Nfq | CIB Talent Hub", layout="wide")

# Estilo CSS corregido
st.markdown("""
<style>
    .main { background-color: #ffffff; }
    .stSidebar { background-color: #001529; color: white; }
    h1 { color: #001529; font-family: 'Inter', sans-serif; }
    .stButton>button { background-color: #ff6b00; color: white; width: 100%; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# 2. CONFIGURACIÓN DE LA IA
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # System Instruction
        instruction = """
        Actúa como el CIB Talent Manager de Nfq.
        Censo: Juan Pérez, Marta García, Carlos Ruiz, Marcos Fernández, Jorge Álvarez, Marina Sánchez, Elena Navarro, David López.
        Genera siempre la respuesta en formato Dashboard de Markdown con tablas.
        Colores: Sidebar Azul Nfq, alertas en Rojo Santander.
        """
        
        # CAMBIO CLAVE: Nombre del modelo compatible
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", 
            system_instruction=instruction
        )

        # 3. INTERFAZ
        st.sidebar.title("CIB Talent Portal")
        menu = st.sidebar.selectbox("Navegación", ["Dashboard", "Staff Directory", "Opportunities", "Training Log"])

        st.title(f"🚀 {menu}")

        if st.button("Sincronizar y Actualizar"):
            with st.spinner("Conectando con el motor de IA..."):
                # Enviamos el prompt según el menú
                response = model.generate_content(f"Muestra la pestaña de {menu} con los datos del staff actualizados.")
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Error de configuración: {e}")
            
else:
    st.warning("⚠️ Por favor, introduce tu API Key en la barra lateral.")
            
else:
    st.warning("⚠️ Introduce tu API Key de Gemini para activar la plataforma.")
    st.info("Obtenla en: https://aistudio.google.com/app/apikey")
