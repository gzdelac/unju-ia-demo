import streamlit as st
import pandas as pd
import time
import random

# --- CONFIGURACIÓN DE PÁGINA Y MARCA UNJu ---
st.set_page_config(
    page_title="Laboratorio IA - UNJu Virtual",
    page_icon="🎓",
    layout="wide"
)

# Estilos CSS para colores UNJu (Azul Institucional y Ocre/Dorado)
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #003057; /* Azul UNJu */
        color: white;
        border-radius: 5px;
        border: 2px solid #cea133; /* Dorado UNJu */
    }
    .stButton>button:hover {
        background-color: #cea133;
        color: #003057;
    }
    h1 {
        color: #003057;
    }
    h3 {
        color: #cea133;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
col1, col2 = st.columns([1, 5])
with col1:
    # Logo de la UNJu (URL pública)
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/23/Logo_UNJu.png", width=100)
with col2:
    st.title("Estrategias y Desafíos de Educar con I.A.")
    st.markdown("**Nivel Medio y Superior | UNJu Virtual**")

st.markdown("---")

# --- BARRA LATERAL (REGISTRO) ---
with st.sidebar:
    st.header("📝 Registro de Asistencia")
    st.info("Para interactuar, por favor completa tus datos.")
    nombre = st.text_input("Nombre y Apellido")
    profesion = st.selectbox("Área / Materia", ["Docente Nivel Medio", "Docente Universitario", "Estudiante", "Directivo", "Otro"])
    
    st.markdown("---")
    st.write("Estado del sistema: 🟢 En línea")

# --- LÓGICA DE DATOS (Simulada para la Demo) ---
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = []

# --- PANEL CENTRAL ---
st.subheader("📢 Pregunta en Tiempo Real")
st.markdown("### ¿Cuál es tu principal temor o desafío al integrar la IA en tu aula?")

respuesta_usuario = st.text_area("Escribe tu opinión aquí...", height=100)

if st.button("Enviar Respuesta"):
    if nombre and respuesta_usuario:
        nueva_entrada = {
            "Nombre": nombre,
            "Perfil": profesion,
            "Respuesta": respuesta_usuario
        }
        st.session_state.respuestas.append(nueva_entrada)
        st.success("¡Respuesta enviada al servidor!")
    else:
        st.error("Por favor completa tu nombre y la respuesta.")

# --- VISUALIZACIÓN DE RESPUESTAS ---
if len(st.session_state.respuestas) > 0:
    st.markdown("---")
    st.subheader(f"📊 Respuestas Recibidas ({len(st.session_state.respuestas)})")
    
    # Mostrar como tabla bonita
    df = pd.DataFrame(st.session_state.respuestas)
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    
    # --- LA MAGIA DE LA IA (GEMINI) ---
    st.header("🧠 Análisis Inteligente (Powered by Gemini)")
    st.write("El profesor puede solicitar a la IA que lea todas las respuestas y detecte patrones.")
    
    if st.button("ANALIZAR TENDENCIAS CON I.A."):
        with st.spinner('Conectando con Gemini... Leyendo respuestas... Analizando sentimientos...'):
            time.sleep(3) # Simula tiempo de procesamiento
            
            # Lógica simulada para la demo (Segura para presentar)
            temas = " ".join([r['Respuesta'] for r in st.session_state.respuestas]).lower()
            analisis = ""
            
            if "plagio" in temas or "copia" in temas:
                analisis = "La IA detecta una preocupación mayoritaria sobre la **integridad académica**. Los docentes temen que los alumnos pierdan la capacidad de escribir por sí mismos."
            elif "tiempo" in temas or "no se" in temas:
                analisis = "El patrón principal es la **falta de capacitación técnica**. Existe entusiasmo, pero también una barrera de entrada sobre cómo empezar."
            else:
                analisis = "La audiencia muestra una **actitud cautelosa pero optimista**. Se identifica la necesidad de cambiar el rol docente de 'transmisor' a 'mentor'."
            
            st.success("✅ Análisis Completado")
            st.markdown(f"### 🤖 Conclusión de la IA:")
            st.info(analisis)
            st.markdown("**Sugerencia pedagógica:** Enfocar el taller en herramientas de detección y pensamiento crítico.")

else:
    st.info("Esperando respuestas de la audiencia...")