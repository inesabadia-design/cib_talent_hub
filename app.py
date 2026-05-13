import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN VISUAL
st.set_page_config(page_title="Nfq | CIB Talent Hub", layout="wide")

st.markdown("""
<style>
    .main { background-color: #ffffff; }
    .stSidebar { background-color: #001529; color: white; }
    h1 { color: #001529; font-family: 'Inter', sans-serif; }
    .stButton>button { background-color: #ff6b00; color: white; width: 100%; border-radius: 5px; border: none; }
    .stButton>button:hover { background-color: #e66000; color: white; }
</style>
""", unsafe_allow_html=True)

# 2. CONFIGURACIÓN DE LA IA
api_key = st.sidebar.text_input("Introduce tu Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # System Instruction detallada
        instruction = """
        Eres el CIB Talent Manager de Nfq. Tu salida debe ser un Dashboard ejecutivo en Markdown.
        Censo de Staff: Juan Pérez, Marta García, Carlos Ruiz, Marcos Fernández, Jorge Álvarez, Marina Sánchez, Elena Navarro, David López.
        Reglas estéticas: 
        - Usa tablas limpias con fondo blanco.
        - Indica estados: [BLOQUEADO] en rojo para los evaluados, [DISPONIBLE] en verde para libres.
        - Branding: Sidebar Azul Nfq (#001529), acentos Naranja (#ff6b00) y alertas en Rojo Santander (#ec0000).
        """
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=instruction
        )

        # 3. INTERFAZ Y NAVEGACIÓN
        st.sidebar.title("CIB Talent Portal")
        menu = st.sidebar.radio("Menú", ["Dashboard", "Staff Directory", "Opportunities", "Training Log"])

        st.title(f"🚀 {menu}")

        # Botón de ejecución
        if st.button(f"Cargar datos de {menu}"):
            with st.spinner("Sincronizando con el motor de IA..."):
                response = model.generate_content(f"Muestra la pestaña de {menu} actualizada.")
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Hubo un error con la API: {e}")
            
else:
    st.sidebar.warning("⚠️ Se requiere API Key")
    st.info("Introduce tu API Key en la barra lateral para visualizar el portal.")
