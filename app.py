import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN VISUAL CORPORATIVA (Fondo Blanco, Sidebar Azul Nfq)
st.set_page_config(page_title="Nfq | CIB Talent Hub 3.1", layout="wide")

st.markdown("""
<style>
    .main { background-color: #ffffff; }
    .stSidebar { background-color: #001529; color: white; }
    h1 { color: #001529; font-family: 'Inter', sans-serif; }
    .stButton>button { 
        background-color: #ff6b00; 
        color: white; 
        width: 100%; 
        border-radius: 5px; 
        border: none; 
        height: 3em; 
        font-weight: bold; 
    }
    .stButton>button:hover { background-color: #e66000; color: white; }
</style>
""", unsafe_allow_html=True)

# 2. CONFIGURACIÓN CONEXIÓN GOOGLE AI STUDIO (GEMINI 3.1)
api_key = st.sidebar.text_input("Introduce tu Gemini API Key", type="password")

if api_key:
    try:
        # Vinculamos tu llave de API
        genai.configure(api_key=api_key)
        
        # System Instructions para el rol de CIB Talent Manager
        instruction = """
        Actúa como el CIB Talent Manager de Nfq. Tu interfaz es un Dashboard ejecutivo en Markdown.
        Censo Oficial del Staff (8 Consultores):
        1. Juan Pérez (Senior Consultant - Analista Funcional) -> Estado: [BLOQUEADO] | Skills: Pagos
        2. Marta García (Consultant - Desarrolladora Python) -> Estado: [EN EVALUACIÓN] | Skills: Python
        3. Carlos Ruiz (Manager - Jefe de Proyecto) -> Estado: [BLOQUEADO] | Skills: Gestión, Riesgos
        4. Marcos Fernández (Associate - Consultor Funcional) -> Estado: [DISPONIBLE] | Skills: Capital Markets, Regulatorio
        5. Jorge Álvarez (Senior Manager - Arquitecto Java) -> Estado: [DISPONIBLE] | Skills: Java, Microservicios
        6. Marina Sánchez (Senior Consultant - Data Analyst) -> Estado: [DISPONIBLE] | Skills: SQL, Power BI
        7. Elena Navarro (Manager - Tech Lead) -> Estado: [DISPONIBLE] | Skills: React, TypeScript
        8. David López (Associate - Data Scientist) -> Estado: [DISPONIBLE] | Skills: Python, Machine Learning

        Reglas estéticas de salida:
        - Transforma las listas en tablas limpias de Markdown con fondo blanco (estilo Excel Premium).
        - Usa el color Rojo Santander (#ec0000) para destacar perfiles [BLOQUEADO] o alertas críticas.
        - Usa el color Verde para destacar perfiles [DISPONIBLE].
        - Las métricas del Dashboard numérico deben calcularse basándose estrictamente en estos 8 perfiles.
        """
        
        # IDENTIFICADOR TÉCNICO OFICIAL DE GEMINI 3.1 PRO PREVIEW EN SDK
        model = genai.GenerativeModel(
            model_name="gemini-3.1-pro-preview-0513",
            system_instruction=instruction
        )

        # 3. INTERFAZ Y NAVEGACIÓN
        st.sidebar.title("CIB Talent Portal")
        menu = st.sidebar.radio("Navegación:", ["Dashboard", "Staff Directory", "Opportunities", "Training Log"])

        st.title(f"🚀 {menu}")

        # Botón de ejecución conectado a la IA de Google
        if st.button(f"Sincronizar Vista con Gemini 3.1 Pro"):
            with st.spinner("Conectando con el motor Gemini 3.1 Pro Preview..."):
                # Fijamos temperatura 0.1 para que sea estricto con los datos
                response = model.generate_content(
                    f"Muestra la pestaña de {menu} estructurada según tus instrucciones de sistema.",
                    generation_config={"temperature": 0.1}
                )
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Error técnico en el motor 3.1: {e}")
        st.info("Tip: Si el error persiste, comprueba que tu llave tiene habilitado el modelo 3.1 Pro Preview en Google AI Studio.")
            
else:
    st.sidebar.warning("⚠️ Se requiere API Key")
    st.info("Introduce tu API Key en la barra lateral para conectar Streamlit con Gemini 3.1 Pro Preview.")
