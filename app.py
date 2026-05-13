import streamlit as st
import google.generativeai as genai
import os

# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILO CORPORATIVO (NFQ x SANTANDER)
st.set_page_config(page_title="Nfq | CIB Talent Hub", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stSidebar { background-color: #001529; color: white; }
    h1 { color: #001529; font-family: 'Montserrat', sans-serif; }
    .stButton>button { background-color: #ff6b00; color: white; border-radius: 5px; }
    .santander-card { border-left: 5px solid #ec0000; padding: 10px; background-color: #fcfcfc; margin-bottom: 10px; }
    </style>
   """, unsafe_allow_html=True)

# 2. CONFIGURACIÓN DE LA IA (BACKEND)
# En GitHub/Streamlit Cloud, deberás añadir tu API_KEY en "Secrets"
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Instrucciones de Sistema (Tus System Instructions)
   system_instruction = """
    Actúa como el CIB Talent Manager de Nfq.
    Censo Real del Staff (6 perfiles obligatorios):
    1. Juan Pérez (Senior Consultant - Funcional)
    2. Marta García (Consultant - Técnico)
    3. Carlos Ruiz (Manager - Funcional)
    4. Marcos Fernández (Associate - Funcional)
    5. Jorge Álvarez (Senior Manager - Técnico)
    6. Marina Sánchez (Senior Consultant - Técnico)
    7. Elena Navarro (Manager - Técnico)
    8. David López (Associate - Técnico)

    Reglas de la Interfaz:
    - Fondo blanco en tablas, Sidebar Azul Nfq (#001529).
    - Columna de estado: [BLOQUEADO] para evaluados, [DISPONIBLE] para libres.
    - El Dashboard debe resumir estas métricas exactamente.
    """
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=system_instruction,
        generation_config={"temperature": 0.2}
    )

    # 3. INTERFAZ DE USUARIO (FRONTEND)
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/b/b8/Banco_Santander_Logotipo.png", width=150) # Logo Santander Ejemplo
    st.sidebar.title("CIB Talent Hub")
    menu = st.sidebar.radio("Navegación", ["Dashboard", "Staff Directory", "Opportunities", "Training Log"])

    st.title(f"🚀 {menu}")

    # Prompt dinámico según la pestaña
    if menu == "Dashboard":
        prompt = "Muestra el Dashboard principal con las métricas de las 6 personas de staff y el resumen de oportunidades recientes."
    elif menu == "Staff Directory":
        prompt = "Muestra la tabla completa del Staff Directory (6 personas) con rangos, perfiles y la columna de estado [BLOQUEADO]/[DISPONIBLE]."
    elif menu == "Opportunities":
        prompt = "Muestra la tabla de Oportunidades de Proyecto en Santander CIB con prioridad en Rojo Santander."
    elif menu == "Training Log":
        prompt = "Muestra el log de formación y cursos realizados por el staff."

    if st.button("Actualizar Datos"):
        with st.spinner("Sincronizando con CIB Talent Engine..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            
else:
    st.warning("⚠️ Introduce tu API Key de Google AI Studio en el lateral para empezar.")
    st.info("Puedes obtener tu clave en: https://aistudio.google.com/app/apikey")
