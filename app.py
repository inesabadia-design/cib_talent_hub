import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Nfq | CIB Talent Hub 3.1", layout="wide")

# Estilo Corporativo
st.markdown("""
<style>
    .main { background-color: #ffffff; }
    .stSidebar { background-color: #001529; color: white; }
    h1 { color: #001529; font-family: 'Inter', sans-serif; }
    .stButton>button { background-color: #ff6b00; color: white; width: 100%; border: none; height: 3em; font-weight: bold; }
    .stButton>button:hover { background-color: #e66000; border: none; }
</style>
""", unsafe_allow_html=True)

# 2. CONFIGURACIÓN DEL MOTOR GEMINI 3.1 PRO
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # System Instructions (Copiadas de tu configuración de AI Studio)
        instruction = """
        Actúa como el CIB Talent Manager de Nfq. Tu interfaz es un Dashboard ejecutivo.
        Censo Real: Juan Pérez, Marta García, Carlos Ruiz, Marcos Fernández, Jorge Álvarez, Marina Sánchez, Elena Navarro, David López.
        
        Lógica de Negocio:
        - Dashboard: Resumen de métricas (8 personas total).
        - Cohesión: Los estados [BLOQUEADO] (Rojo) y [DISPONIBLE] (Verde) deben ser consistentes entre pestañas.
        - Estética: Tablas limpias, fondo blanco, estilo profesional Santander CIB.
        """
        
        # ID TÉCNICO PARA GEMINI 3.1 PRO PREVIEW
        model = genai.GenerativeModel(
            model_name="gemini-3.1-pro-preview", 
            system_instruction=instruction
        )

        # 3. INTERFAZ
        st.sidebar.title("CIB Talent Portal")
        menu = st.sidebar.radio("Navegación:", ["Dashboard", "Staff Directory", "Opportunities", "Training Log"])

        st.title(f"🚀 {menu}")

        if st.button(f"Sincronizar {menu}"):
            with st.spinner("Consultando a Gemini 3.1 Pro..."):
                # Bajamos temperatura para máxima precisión
                response = model.generate_content(
                    f"Genera la vista de {menu} para el staff actual.",
                    generation_config={"temperature": 0.1}
                )
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Error de conexión con Gemini 3.1: {e}")
            
else:
    st.sidebar.warning("⚠️ Introduce tu API Key")
            
else:
    st.sidebar.warning("⚠️ Se requiere API Key")
    st.info("Introduce tu API Key en la barra lateral para visualizar el portal.")
