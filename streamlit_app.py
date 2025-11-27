import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="UNJu - Laboratorio IA", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #ffffff;}
    h1 {color: #003057;}
    .stButton>button {background-color: #003057; color: white; border: 2px solid #cea133;}
    .privacy-box {background-color: #f0f7fb; padding: 10px; border-radius: 5px; border-left: 4px solid #003057; font-size: 13px;}
    .credits {font-size: 11px; color: #666; text-align: center; margin-top: 30px;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. MEMORIA COMPARTIDA ---
@st.cache_resource
def get_data_store():
    return []

votos_globales = get_data_store()

# --- 3. BARRA LATERAL (ALUMNO) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/23/Logo_UNJu.png", width=90)
    st.title("🎓 PARTICIPACIÓN")
    
    st.subheader("1. Tus Datos")
    nombre = st.text_input("Nombre Completo")
    email = st.text_input("Correo Electrónico")
    
    st.markdown("<div class='privacy-box'>🔐 <b>Privacidad:</b> Tu correo NO se mostrará en la pantalla pública.</div>", unsafe_allow_html=True)
    consentimiento = st.checkbox("Acepto compartir mis datos.")

    st.divider()

    st.subheader("2. Encuesta")
    opcion = st.radio("¿Detectas textos de IA?", ["Sí, tengo trucos 🕵️", "Tengo dudas 🤔", "No, parecen iguales 🤖"])
    justificacion = st.text_input("Palabra clave")

    if st.button("ENVIAR RESPUESTA 🚀"):
        if not consentimiento:
            st.error("⚠️ Debes aceptar la privacidad.")
        elif not nombre or not email:
            st.warning("⚠️ Completa Nombre y Email.")
        else:
            # Guardamos TODO en la lista interna
            nuevo_voto = {
                "Fecha": time.strftime("%H:%M:%S"),
                "Nombre": nombre,
                "Email": email, 
                "Opción": opcion,
                "Justificación": justificacion
            }
            votos_globales.append(nuevo_voto)
            st.success("¡Enviado!")
            time.sleep(0.5)
            st.rerun()

    # RECURSOS
    st.divider()
    st.header("📂 Descargas")
    link_doc = "https://docs.google.com/document/d/1AM1gwETYvGE_Crfne9jBpR7ZCHRysXURtl1M6UuA0Uo/edit?usp=sharing"
    st.link_button("📥 Documento del Taller", link_doc)
    
    st.markdown("<div class='credits'><b>EQUIPO DOCENTE UNJu</b><br>Esp. G. de la Cámara<br>Mag. N. Lozano<br>Prof. G. Cano</div>", unsafe_allow_html=True)

# --- 4. PANEL CENTRAL (PROFESOR) ---
st.title("Estrategias y Desafíos: IA en Educación")
st.markdown("### 📊 Monitor de Aula en Tiempo Real")

if len(votos_globales) > 0:
    st.metric("Alumnos Participando", len(votos_globales))
    
    # DATAFRAME COMPLETO
    df = pd.DataFrame(votos_globales)
    
    # --- ZONA BLINDADA CON CONTRASEÑA ---
    st.divider()
    with st.expander("🔐 ÁREA EXCLUSIVA DOCENTE (Requiere Clave)"):
        password = st.text_input("Ingresa la contraseña de administrador:", type="password")
        
        # CONTRASEÑA DEL PROFESOR
        clave_correcta = "unju2025" 
        
        if password == clave_correcta:
            st.success("✅ Acceso Autorizado")
            st.info("Descarga la lista completa con los correos de los alumnos.")
            
            # Botón de descarga
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 DESCARGAR BASE DE DATOS (CSV)",
                data=csv,
                file_name='asistencia_segura_unju.csv',
                mime='text/csv',
            )
        elif password:
            st.error("⛔ Contraseña incorrecta")

    st.divider()

    # --- GRÁFICOS PÚBLICOS (SIN MOSTRAR EMAIL) ---
    conteo = df['Opción'].value_counts().reset_index()
    conteo.columns = ['Respuesta', 'Votos']
    
    fig = px.bar(conteo, x='Respuesta', y='Votos', color='Respuesta', text='Votos',
                 color_discrete_sequence=['#003057', '#cea133', '#A0A0A0'])
    st.plotly_chart(fig, use_container_width=True)
    
    # TABLA PÚBLICA (FILTRADA - Solo muestra Nombre y Opinión)
    st.subheader("📝 Últimas participaciones")
    st.dataframe(df[["Nombre", "Opción", "Justificación"]], use_container_width=True, hide_index=True)

else:
    st.warning("⚠️ Esperando votos... Escanea el QR para participar.")

if st.button("🔄 ACTUALIZAR PANTALLA"):
    st.rerun()
