import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILO CORPORATIVO
st.set_page_config(page_title="Nfq | CIB Talent Hub", layout="wide")

# Inyectar CSS personalizado
st.markdown("""
<style>
    .main { background-color: #ffffff; }
    .stSidebar { background-color: #001529; color: white; }
    h1 { color: #001529; font-family: 'Inter', sans-serif; }
    .stButton>button { background-color: #ff6b00; color: white; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# 2. CONFIGURACIÓN DE LA IA (BACKEND)
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Instrucciones de Sistema corregidas
    system_instruction = """
    Actúa como el CIB Talent Manager de Nfq.
    Censo Real del Staff:
    1. Juan Pérez (Senior Consultant - Funcional)
    2. Marta García (Consultant - Técnico)
    3. Carlos Ruiz (Manager - Funcional)
    4. Marcos Fernández (Associate - Funcional)
    5. Jorge Álvarez (Senior Manager - Técnico)
    6. Marina Sánchez (Senior Consultant - Técnico)
    7. Elena Navarro (Manager - Técnico)
    8. David López (Associate - Técnico)

    Reglas:
    - Fondo blanco en tablas, Sidebar Azul Nfq (#001529).
    - Columna de estado: [BLOQUEADO] en rojo para evaluados, [DISPONIBLE] en verde para libres.
    - El Dashboard debe resumir estas métricas exactamente.
    """
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=system_instruction,
        generation_config={"temperature": 0.2}
    )

    # 3. INTERFAZ DE USUARIO (FRONTEND)
    st.sidebar.title("CIB Talent Hub")
    menu = st.sidebar.radio("Navegación", ["Dashboard", "Staff Directory", "Opportunities", "Training Log"])

    st.title(f"🚀 {menu}")

    # Prompt dinámico según la pestaña
    if menu == "Dashboard":
        prompt = "Muestra el Dashboard principal sincronizado con los 8 miembros del staff y métricas de Support/Training."
    elif menu == "Staff Directory":
        prompt = "Muestra la tabla del Staff Directory con los 8 nombres, sus rangos y el estado [BLOQUEADO]/[DISPONIBLE]."
    elif menu == "Opportunities":
        prompt = "Muestra las oportunidades de proyecto en Santander CIB con prioridad en Rojo Santander."
    else:
        prompt = "Muestra el log de formación y certificaciones realizadas por el staff."

    if st.button("Actualizar Vista"):
        with st.spinner("Sincronizando..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            
else:
    st.warning("⚠️ Introduce tu API Key de Gemini para activar la plataforma.")
    st.info("Obtenla en: https://aistudio.google.com/app/apikey")
