import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILO NFQ
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

# 2. CONFIGURACIÓN DEL MOTOR GEMINI
api_key = st.sidebar.text_input("Introduce tu Gemini API Key", type="password")

if api_key:
    try:
        # Configurar la llave
        genai.configure(api_key=api_key)
        
        # System Instructions calcadas a tus perfiles reales de la imagen
        instruction = """
        Actúa como el CIB Talent Manager de Nfq. Tu interfaz es un Dashboard ejecutivo en Markdown.
        Censo Real del Staff (Basado estrictamente en el equipo oficial):
        1. Juan Pérez (Senior Consultant - Analista Funcional) -> Estado: [BLOQUEADO] | Skills: Pagos
        2. Marta García (Consultant - Desarrolladora Python) -> Estado: [EN EVALUACIÓN] | Skills: Python
        3. Carlos Ruiz (Manager - Jefe de Proyecto) -> Estado: [BLOQUEADO] | Skills: Gestión, Riesgos
        4. Marcos Fernández (Associate - Consultor Funcional) -> Estado: [DISPONIBLE] | Skills: Capital Markets, Regulatorio
        5. Jorge Álvarez (Senior Manager - Arquitecto Java) -> Estado: [DISPONIBLE] | Skills: Java, Microservicios
        6. Marina Sánchez (Senior Consultant - Data Analyst) -> Estado: [DISPONIBLE] | Skills: SQL, Power BI
        7. Elena Navarro (Manager - Tech Lead) -> Estado: [DISPONIBLE] | Skills: React, TypeScript
        8. David López (Associate - Data Scientist) -> Estado: [DISPONIBLE] | Skills: Python, Machine Learning

        Reglas de la interfaz dinámica:
        - Transforma las listas en columnas limpias y estructuradas tipo tabla de Excel Premium con fondo blanco.
        - Usa el color Rojo Santander (#ec0000) para destacar elementos [BLOQUEADO] o alertas críticas.
        - Usa el color Verde para los perfiles que marquen [DISPONIBLE].
        - Los datos numéricos de métricas del Dashboard deben depender directamente de este censo de 8 personas.
        """
        
        # SOLUCIÓN EXPLICITA AL 404: Usamos la nomenclatura de modelo adaptada a la API 3.1
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",  # Forzamos la entrada más compatible globalmente para endpoints API
            system_instruction=instruction
        )

        # 3. INTERFAZ Y NAVEGACIÓN
        st.sidebar.title("CIB Talent Portal")
        menu = st.sidebar.radio("Navegación:", ["Dashboard", "Staff Directory", "Opportunities", "Training Log"])

        st.title(f"🚀 {menu}")

        # Botón dinámico para renderizar la pestaña activa
        if st.button(f"Sincronizar Vista: {menu}"):
            with st.spinner("Conectando con Gemini 3.1 Engine..."):
                response = model.generate_content(
                    f"Genera la visualización interactiva para la pestaña de {menu} organizando los datos en columnas claras.",
                    generation_config={"temperature": 0.1}
                )
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Error en la llamada de la API: {e}")
        st.info("Tip: Si el error persiste, genera una nueva API Key limpia desde Google AI Studio.")
            
else:
    st.sidebar.warning("⚠️ Se requiere API Key")
    st.info("Por favor, introduce tu API Key en la barra lateral para sincronizar el portal.")
