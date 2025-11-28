import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="UNJu - Laboratorio IA", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #ffffff;}
    h1 {color: #003057; font-weight: 800;}
    h2, h3 {color: #cea133;}
    .stButton>button {
        background-color: #003057; 
        color: white; 
        border-radius: 8px; 
        border: 2px solid #cea133;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {background-color: #cea133; color: #003057;}
    .privacy-box {background-color: #e3f2fd; padding: 10px; border-radius: 5px; font-size: 12px; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DATOS (MEMORIA) ---
@st.cache_resource
def get_data_store():
    return []

votos_globales = get_data_store()

# --- 3. BARRA LATERAL (ALUMNO) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/23/Logo_UNJu.png", width=90)
    st.title("🎓 GIMNASIO COGNITIVO")
    
    # === MÓDULO A: IDENTIDAD (Siempre visible) ===
    st.subheader("1. Identificación")
    nombre = st.text_input("Nombre Completo")
    email = st.text_input("Correo Electrónico")
    consentimiento = st.checkbox("Acepto participar.")
    
    st.divider()

    # === MÓDULO B: ENCUESTA DE OPINIÓN ===
    st.subheader("2. Encuesta Inicial")
    st.write("**¿Detectas textos de IA?**")
    opcion_encuesta = st.radio("Elige una opción:", 
                              ["Sí, es fácil 🕵️", "Tengo dudas / A veces 🤔", "No, es imposible 🤖"],
                              label_visibility="collapsed")
    
    # --- BOTÓN 1: SOLO OPINIÓN ---
    if st.button("📨 ENVIAR OPINIÓN"):
        if not consentimiento or not nombre:
            st.error("⚠️ Completa Nombre y acepta Privacidad.")
        else:
            votos_globales.append({
                "Tipo": "Encuesta",
                "Nombre": nombre,
                "Email": email,
                "Opinion": opcion_encuesta,
                "Puntaje": None # No aplica
            })
            st.success("¡Opinión registrada!")
            time.sleep(1)
            st.rerun()

    st.divider()

    # === MÓDULO C: RECURSOS ===
    st.subheader("3. Material de Estudio")
    link_doc = "https://docs.google.com/document/d/1AM1gwETYvGE_Crfne9jBpR7ZCHRysXURtl1M6UuA0Uo/edit?usp=sharing"
    st.link_button("📄 Leer Documento (PDF)", link_doc)
    
    link_prezi = "https://prezi.com/p/lqubx8gnsufo/la-escritura-con-ia-y-plagio-controversias-en-la-evaluacion-actual/?present=1"
    st.link_button("📽️ Ver Prezi (Explosividad)", link_prezi)
    
    link_gem = "https://gemini.google.com/gem/1TrcGQ8KaDiV7uIqF_JUPA57OKhL7gybb?usp=sharing"
    st.link_button("🕵️ Probar mi GEM Detector", link_gem)
    
    link_drive = "https://drive.google.com/drive/folders/1WScG-E2HKwzhFMeIk_pjlt6Y97wRuSF3"
    st.link_button("🛠️ Descargar Metadatos", link_drive)

    st.divider()

    # === MÓDULO D: QUIZ FINAL ===
    st.subheader("4. Quiz de Cierre")
    
    p1 = st.radio("Concepto de Nuevo Plagio:", ["Copiar-Pegar", "Simulación de voz humana", "Error formato"])
    p2 = st.radio("Alta Explosividad significa:", ["Texto Monótono (IA)", "Variabilidad Humana 💥", "Uso de mayúsculas"])
    p3 = st.radio("Conclusión sobre el GEM:", ["Es 100% exacto", "Requiere mirada crítica 👁️", "Si dice Humano es Humano"])

    # --- BOTÓN 2: SOLO QUIZ ---
    if st.button("🚀 ENVIAR QUIZ FINAL"):
        if not consentimiento or not nombre:
            st.error("⚠️ Completa Nombre y acepta Privacidad.")
        else:
            score = 0
            if "Simulación" in p1: score += 1
            if "Variabilidad" in p2: score += 1
            if "mirada crítica" in p3: score += 1
            
            votos_globales.append({
                "Tipo": "Quiz",
                "Nombre": nombre,
                "Email": email,
                "Opinion": None, # No aplica
                "P1": p1, "P2": p2, "P3": p3,
                "Puntaje": score
            })
            
            if score == 3: st.balloons()
            st.success(f"¡Quiz enviado! Nota: {score}/3")
            time.sleep(2)
            st.rerun()
            
    # Créditos
    st.markdown("<div style='text-align:center; color:grey; font-size:10px; margin-top:20px;'>Docentes: G. de la Cámara, N. Lozano, G. Cano</div>", unsafe_allow_html=True)

# --- 4. PANTALLA PROFESOR ---
st.title("Monitor: IA y Pensamiento Crítico")
st.markdown("### 📊 Tablero en Tiempo Real")

if len(votos_globales) > 0:
    df = pd.DataFrame(votos_globales)
    
    # Separamos los datos para no mezclar peras con manzanas
    df_encuesta = df[df["Tipo"] == "Encuesta"]
    df_quiz = df[df["Tipo"] == "Quiz"]
    
    # MÉTRICAS
    c1, c2, c3 = st.columns(3)
    # Contamos nombres únicos para saber alumnos reales
    total_alumnos = len(df["Nombre"].unique())
    c1.metric("Alumnos Activos", total_alumnos)
    
    if not df_quiz.empty:
        promedio = df_quiz["Puntaje"].mean()
        c2.metric("Promedio Quiz", f"{promedio:.1f} / 3.0")
        
        # Pensamiento Crítico
        criticos = len(df_quiz[df_quiz["P3"].str.contains("mirada crítica", na=False)])
        porc = (criticos / len(df_quiz)) * 100
        c3.metric("Pensamiento Crítico", f"{porc:.0f}%")

    # ADMIN
    with st.expander("🔐 ADMINISTRACIÓN (Clave: unju2025)"):
        pwd = st.text_input("Clave:", type="password")
        if pwd == "unju2025":
            c_csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 BAJAR EXCEL COMPLETO", c_csv, "unju_completo.csv", "text/csv")
            if st.button("🗑️ BORRAR TODO"):
                votos_globales.clear()
                st.rerun()

    st.divider()
    
    # GRÁFICOS
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("📊 Opiniones")
        if not df_encuesta.empty:
            fig1 = px.bar(df_encuesta['Opinion'].value_counts().reset_index(), x='Opinion', y='count', color='Opinion')
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Esperando opiniones...")

    with col_g2:
        st.subheader("🧠 Resultados Quiz")
        if not df_quiz.empty:
            fig2 = px.histogram(df_quiz, x="Puntaje", nbins=4, title="Distribución de Notas", color_discrete_sequence=['#cea133'])
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Esperando exámenes...")

    # TABLA (Últimos 5 registros)
    st.divider()
    st.caption("Actividad Reciente:")
    st.dataframe(df[["Nombre", "Tipo", "Puntaje"]].tail(5), use_container_width=True, hide_index=True)

else:
    st.info("👋 Esperando participación...")

if st.button("🔄 ACTUALIZAR"):
    st.rerun()
