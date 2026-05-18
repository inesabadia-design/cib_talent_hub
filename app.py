import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN VISUAL (Fondo Blanco, Sidebar Azul Nfq)
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

# 2. CONFIGURACIÓN DEL MOTOR DE GOOGLE AI STUDIO
api_key = st.sidebar.text_input("Introduce tu Gemini API Key", type="password")

if api_key:
    try:
        # Conectamos con tu cuenta de AI Studio
        genai.configure(api_key=api_key)
        
        # Estas son las System Instructions que te pide el formulario
        instruction = """
        Actúa como el CIB Talent Manager de Nfq. Tu interfaz es un Dashboard ejecutivo en Markdown.
        Censo Real del Staff:
        1. Juan Pérez (Senior Consultant - Analista Funcional) -> Estado: [BLOQUEADO]
        2. Marta García (Consultant - Desarrolladora Python) -> Estado: [EN EVALUACIÓN]
        3. Carlos Ruiz (Manager - Jefe de Proyecto) -> Estado: [BLOQUEADO]
        4. Marcos Fernández (Associate - Consultor Funcional) -> Estado: [DISPONIBLE]
        5. Jorge Álvarez (Senior Manager - Arquitecto Java) -> Estado: [DISPONIBLE]
        6. Marina Sánchez (Senior Consultant - Data Analyst) -> Estado: [DISPONIBLE]
        7. Elena Navarro (Manager - Tech Lead) -> Estado: [DISPONIBLE]
        8. David López (Associate - Data Scientist) -> Estado: [DISPONIBLE]

        Reglas del Dashboard:
        - Estructura los datos en tablas limpias de Markdown con fondo blanco.
        - Muestra métricas coherentes con el censo de 8 personas.
        - Usa colores corporativos: Azul Nfq (#001529) y Rojo Santander (#ec0000) para bloqueados.
        """
        
        # Aquí llamamos al modelo Pro de tu AI Studio de forma correcta
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=instruction
        )

        # 3. INTERFAZ Y NAVEGACIÓN
        st.sidebar.title("CIB Talent Portal")
        menu = st.sidebar.radio("Navegación:", ["Dashboard", "Staff Directory", "Opportunities", "Training Log"])

        st.title(f"🚀 {menu}")

        # El botón mágico que envía la orden a Google AI Studio
        if st.button(f"Sincronizar Vista con AI Studio"):
            with st.spinner("Sincronizando con el motor de Gemini 3.1 Pro..."):
                # Enviamos el prompt dinámico
                response = model.generate_content(
                    f"Muestra la sección de {menu} formateada según tus instrucciones de sistema.",
                    generation_config={"temperature": 0.1}
                )
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Error detectado: {e}")
            
else:
    st.sidebar.warning("⚠️ Se requiere API Key de AI Studio")
    st.info("Introduce tu API Key en la barra lateral para conectar la web con la Inteligencia Artificial.")
