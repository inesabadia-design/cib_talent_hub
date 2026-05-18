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
        
        # System Instructions para el comportamiento del Dashboard
        instruction = """
        Actúa como el CIB Talent Manager de Nfq. Tu interfaz es un Dashboard ejecutivo en Markdown.
        Censo Real del Staff:
        1. Juan Pérez (Senior Consultant - Funcional) -> Estado: [BLOQUEADO]
        2. Marta García (Consultant - Técnico) -> Estado: [EN EVALUACIÓN]
        3. Carlos Ruiz (Manager - Funcional) -> Estado: [BLOQUEADO]
        4. Marcos Fernández (Associate - Funcional) -> Estado: [DISPONIBLE]
        5. Jorge Álvarez (Senior Manager - Técnico) -> Estado: [DISPONIBLE]
        6. Marina Sánchez (Senior Consultant - Técnico) -> Estado: [DISPONIBLE]
        7. Elena Navarro (Manager - Técnico) -> Estado: [DISPONIBLE]
        8. David López (Associate - Técnico) -> Estado: [DISPONIBLE]

        Reglas estéticas obligatorias:
        - Estructura la información en columnas y tablas limpias con fondo blanco.
        - Usa el color Rojo Santander (#ec0000) para destacar alertas o perfiles [BLOQUEADO].
        - Usa el color Verde para destacar perfiles [DISPONIBLE].
        - Muestra datos coherentes con el censo de 8 personas.
        """
        
        # LLAMADA DE CONFIGURACIÓN ESTÁNDAR (Evita el error 404 de versión)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=instruction
        )

        # 3. INTERFAZ Y NAVEGACIÓN
        st.sidebar.title("CIB Talent Portal")
        menu = st.sidebar.radio("Navegación:", ["Dashboard", "Staff Directory", "Opportunities", "Training Log"])

        st.title(f"🚀 {menu}")

        # Botón dinámico para renderizar la pestaña activa
        if st.button(f"Sincronizar Vista: {menu}"):
            with st.spinner("Conectando con Gemini 3.1 Pro Engine..."):
                # Bajamos la temperatura para que sea preciso y estructurado
                response = model.generate_content(
                    f"Muestra la sección de {menu} formateada con las reglas del sistema.",
                    generation_config={"temperature": 0.1}
                )
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Error en la llamada de la API: {e}")
        st.info("Tip: Asegúrate de que tu API Key de Google AI Studio está activa y no tiene espacios.")
            
else:
    st.sidebar.warning("⚠️ Se requiere API Key")
    st.info("Por favor, introduce tu API Key en la barra lateral para sincronizar el portal.")
