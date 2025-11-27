import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(
    page_title="UNJu - Laboratorio IA",
    page_icon="🎓",
    layout="wide"
)

# Estilos CSS Personalizados (Branding UNJu + Estética INNOA)
st.markdown("""
    <style>
    .main {background-color: #ffffff;}
    h1 {color: #003057; font-weight: 800;}
    h2, h3 {color: #cea133;}
    .stButton>button {
        background-color: #003057; 
        color: white; 
        width: 100%;
        border-radius: 8px; 
        font-weight: bold;
        border: 2px solid #cea133;
    }
    .stButton>button:hover {
        background-color: #cea133; 
        color: #003057;
    }
    /* Caja de privacidad */
    .privacy-box {
        background-color: #f0f7fb; 
        padding: 10px; 
        border-radius: 5px; 
        border-left: 4px solid #003057; 
        font-size: 13px;
        margin-bottom: 10px;
    }
    /* Créditos al pie */
    .credits {
        font-size: 11px;
        color: #666;
        text-align: center;
        margin-top: 30px;
        border-top: 1px solid #ddd;
        padding-top: 10px;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MEMORIA COMPARTIDA (BASE DE DATOS EN RAM) ---
@st.cache_resource
def get_data_store():
    return []

votos_globales = get_data_store()

# --- 3. BARRA LATERAL (ZONA DEL ALUMNO) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/23/Logo_UNJu.png", width=90)
    st.title("🎓 PARTICIPACIÓN")
    st.markdown("Bienvenido al **Gimnasio Cognitivo**.")
    
    st.divider()
    
    # --- MÓDULO DE DATOS PERSONALES ---
    st.subheader("1. Tus Datos")
    nombre = st.text_input("Nombre Completo")
    email = st.text_input("Correo Electrónico (Para envío de material)")
    
    # Checkbox de Privacidad (Obligatorio)
    st.markdown("""
    <div class='privacy-box'>
        🔐 <b>Protección de Datos:</b> 
        Tus respuestas serán anónimas en la pantalla pública. Tu correo se usará solo para fines académicos de este taller.
    </div>
    """, unsafe_allow_html=True)
    consentimiento = st.checkbox("Acepto participar y compartir mis datos.")

    st.divider()

    # --- MÓDULO DE VOTACIÓN ---
    st.subheader("2. Encuesta en Vivo")
    st.write("**¿Sabes detectar si un texto fue escrito por IA?**")
    opcion = st.radio(
        "Selecciona una opción:",
        ["Sí, tengo mis trucos 🕵️", "Tengo dudas / A veces 🤔", "No, me parecen iguales 🤖"],
        label_visibility="collapsed"
    )
    
    justificacion = st.text_input("¿Por qué? (Dinos una palabra clave)")
    
    # Botón de envío con validación
    if st.button("ENVIAR RESPUESTA 🚀"):
        if not consentimiento:
            st.error("⚠️ ERROR: Debes aceptar el uso de datos para participar.")
        elif not nombre or not email:
            st.warning("⚠️ Faltan datos: Por favor completa Nombre y Email.")
        else:
            # Guardamos el voto (Sin el email para la parte pública)
            nuevo_voto = {
                "Opción": opcion, 
                "Justificación": justificacion if justificacion else "Sin comentarios", 
                "Autor": nombre # El email no se guarda en la lista pública por seguridad
            }
            votos_globales.append(nuevo_voto)
            st.success("¡Voto registrado con éxito!")
            time.sleep(1)
            st.rerun()

    # --- MÓDULO DE RECURSOS (DESCARGAS) ---
    st.divider()
    st.header("📂 Material de Clase")
    st.info("Descarga aquí el documento oficial del taller.")
    
    # LINK OFICIAL PROPORCIONADO POR GUILLERMO
    link_documento = "https://docs.google.com/document/d/1AM1gwETYvGE_Crfne9jBpR7ZCHRysXURtl1M6UuA0Uo/edit?usp=sharing"
    
    st.link_button("📥 Abrir Documento del Taller", link_documento)
    
    # --- CRÉDITOS ---
    st.markdown("""
    <div class='credits'>
        <b>EQUIPO DOCENTE UNJu</b><br>
        Esp. Guillermo Zenon de la Cámara<br>
        Mag. Nilda Lozano<br>
        Prof. Gloria Cano<br><br>
        <i>UNJu Virtual - 2025</i>
    </div>
    """, unsafe_allow_html=True)

# --- 4. PANEL CENTRAL (PANTALLA DEL PROFESOR) ---

# Encabezado Principal
col_logo, col_titulo = st.columns([1, 6])
with col_titulo:
    st.title("Estrategias y Desafíos: IA en Educación")
    st.markdown("### 📊 Monitor de Aula en Tiempo Real")

# Métricas rápidas
if len(votos_globales) > 0:
    st.metric(label="👥 Alumnos Participando Ahora", value=len(votos_globales))
else:
    st.info("Esperando la primera participación... ¡Escaneen el QR!")

st.divider()

# --- 5. VISUALIZACIÓN DE DATOS ---
if st.button("🔄 ACTUALIZAR PANTALLA (DOCENTE)"):
    st.rerun()

if len(votos_globales) > 0:
    # Convertimos la lista en DataFrame para graficar
    df = pd.DataFrame(votos_globales)
    
    # Conteo de votos
    conteo = df['Opción'].value_counts().reset_index()
    conteo.columns = ['Respuesta', 'Votos']
    
    # GRÁFICO DE BARRAS (Plotly) - Colores Institucionales
    fig = px.bar(
        conteo, 
        x='Respuesta', 
        y='Votos', 
        text='Votos',
        color='Respuesta',
        color_discrete_sequence=['#003057', '#cea133', '#A0A0A0'], # Azul, Ocre, Gris
        title="Resultados de la Encuesta: Percepción de la IA"
    )
    fig.update_layout(height=450, showlegend=False)
    fig.update_traces(textposition='outside', textfont_size=20)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # --- Muro de Opiniones (Anónimo para el público) ---
    col_izq, col_der = st.columns(2)
    with col_izq:
        st.subheader("💬 Opiniones del Aula")
        # Mostramos las últimas 5 justificaciones
        comentarios = [c for c in df['Justificación'] if c != "Sin comentarios"]
        if comentarios:
            for com in comentarios[-5:]:
                st.info(f"🗨️ {com}")
        else:
            st.write("Sin comentarios textuales aún.")

    with col_der:
        st.subheader("🧠 Análisis IA (Simulado)")
        st.caption("El docente puede solicitar a Gemini una interpretación de los datos.")
        
        if st.button("SOLICITAR CONCLUSIÓN A GEMINI"):
            with st.spinner('Analizando patrones de respuesta...'):
                time.sleep(2.5)
                
                # Lógica simple para la demo basada en el ganador
                ganador = conteo.iloc[0]['Respuesta']
                
                analisis = f"**Análisis de {len(votos_globales)} respuestas:**\n\n"
                
                if "No" in ganador:
                    analisis += "🚨 **Alerta:** La mayoría de la clase NO distingue textos de IA. Esto confirma la necesidad urgente de alfabetización digital crítica."
                elif "dudas" in ganador:
                    analisis += "⚠️ **Oportunidad:** Existe una intuición sobre la IA, pero faltan herramientas técnicas de verificación."
                else:
                    analisis += "✅ **Nivel Avanzado:** El grupo muestra confianza, pero debemos validar si es real o sesgo de sobreconfianza."
                    
                st.success("Análisis Completado")
                st.markdown(f"### 🤖 Conclusión:")
                st.write(analisis)

else:
    # Estado inicial (Vacío)
    st.warning("⚠️ Aún no hay votos registrados. Por favor ingresen desde la barra lateral.")
