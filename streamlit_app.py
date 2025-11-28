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
    }
    .stButton>button:hover {background-color: #cea133; color: #003057;}
    
    /* Caja de Privacidad */
    .privacy-box {
        background-color: #e3f2fd; 
        padding: 12px; 
        border-radius: 8px; 
        border-left: 5px solid #003057; 
        font-size: 13px;
        margin-bottom: 15px;
    }
    
    /* Créditos Mejorados */
    .credits-container {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #ddd;
        text-align: center;
    }
    .credits-title {
        color: #003057;
        font-weight: bold;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .credits-names {
        color: #555;
        font-size: 11px;
        margin-top: 5px;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DATOS (MEMORIA) ---
@st.cache_resource
def get_data_store():
    return []

votos_globales = get_data_store()

# --- 3. BARRA LATERAL (RUTA DE APRENDIZAJE) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/23/Logo_UNJu.png", width=100)
    st.title("🎓 LABORATORIO IA")
    
    # --- PASO 1: IDENTIDAD ---
    st.header("1️⃣ Identificación")
    nombre = st.text_input("Nombre Completo (Requerido)")
    email = st.text_input("Correo Electrónico (Requerido)")
    
    st.markdown("<div class='privacy-box'>🔐 <b>Privacidad:</b> Tus respuestas se procesan de forma segura y ética.</div>", unsafe_allow_html=True)
    consentimiento = st.checkbox("Acepto participar en el taller.")

    st.divider()

    # --- PASO 2: ENCUESTA INICIAL ---
    st.header("2️⃣ Diagnóstico")
    st.write("**¿Crees que podrías identificar un texto escrito por IA?**")
    opcion_encuesta = st.radio("Selecciona:", 
                              ["Sí, es fácil 🕵️", "Tengo dudas / A veces 🤔", "No, es imposible 🤖"], 
                              label_visibility="collapsed")

    st.divider()

    # --- PASO 3: RECURSOS Y EXPERIMENTACIÓN ---
    st.header("3️⃣ Recursos y Práctica")
    st.info("Sigue este orden para responder el Quiz final:")

    # Botones de Recursos
    link_doc = "https://docs.google.com/document/d/1AM1gwETYvGE_Crfne9jBpR7ZCHRysXURtl1M6UuA0Uo/edit?usp=sharing"
    st.link_button("📄 1. Leer: La Escritura con IA y Plagio (PDF)", link_doc)
    
    link_prezi = "https://prezi.com/p/lqubx8gnsufo/la-escritura-con-ia-y-plagio-controversias-en-la-evaluacion-actual/?present=1"
    st.link_button("📽️ 2. Ver: Prezi (Concepto Explosividad)", link_prezi)
    
    link_gem = "https://gemini.google.com/gem/1TrcGQ8KaDiV7uIqF_JUPA57OKhL7gybb?usp=sharing"
    st.link_button("🕵️ 3. Probar: Mi GEM Detector de IA", link_gem)
    
    link_drive = "https://drive.google.com/drive/folders/1WScG-E2HKwzhFMeIk_pjlt6Y97wRuSF3"
    st.link_button("🛠️ 4. Construir: Descargar Metadatos (Arma tu GEM)", link_drive)

    st.divider()

    # --- PASO 4: EVALUACIÓN FINAL ---
    st.header("4️⃣ Quiz de Cierre")
    st.write("Demuestra tu mirada crítica:")
    
    # P1: Plagio
    p1 = st.radio("¿Qué diferencia al nuevo 'Plagio IA' del tradicional?", 
                 ["Es un simple Copiar-Pegar", "Simula una voz humana (Simulación)", "Es un error de formato"])
    
    # P2: Explosividad
    p2 = st.radio("¿Qué significa 'Alta Explosividad' en un texto?", 
                 ["Que es monótono (IA)", "Que tiene variabilidad humana 💥", "Que usa mayúsculas"])
    
    # P3: Mirada Crítica (NUEVA)
    p3 = st.radio("Tras usar el GEM Detector, ¿cuál es la conclusión profesional?", 
                 ["El GEM nunca se equivoca (100% exacto)", "Hay que tener una mirada crítica sobre la respuesta 👁️", "Si dice Humano, es Humano"])

    # BOTÓN DE ENVÍO
    if st.button("🚀 ENVIAR EVALUACIÓN"):
        if not consentimiento:
            st.error("⚠️ Debes aceptar la privacidad.")
        elif not nombre or not email:
            st.warning("⚠️ Faltan datos (Nombre/Email).")
        else:
            # Corrección
            score = 0
            feedback = []
            
            if "Simula" in p1: score += 1
            else: feedback.append("P1: Recuerda, la IA no copia, 'simula'.")
                
            if "variabilidad" in p2: score += 1
            else: feedback.append("P2: Los humanos somos 'explosivos' al escribir.")
                
            if "mirada crítica" in p3: score += 1
            else: feedback.append("P3: ¡Cuidado! La IA es un asistente, tú eres el juez.")

            # Guardar
            registro = {
                "Hora": time.strftime("%H:%M:%S"),
                "Nombre": nombre,
                "Email": email,
                "Opinion": opcion_encuesta,
                "P1_Plagio": p1,
                "P2_Explosividad": p2,
                "P3_Critica": p3,
                "Puntaje": score
            }
            votos_globales.append(registro)

            # Retroalimentación Inmediata
            if score == 3:
                st.balloons()
                st.success("🏆 ¡PERFECTO! Has demostrado un criterio experto.")
            else:
                st.info(f"Tu Puntaje: {score}/3")
                for f in feedback:
                    st.warning(f)
            
            time.sleep(2)
            st.rerun()

    # --- CRÉDITOS ---
    st.markdown("""
    <div class='credits-container'>
        <div class='credits-title'>Equipo Docente UNJu</div>
        <div class='credits-names'>
            Esp. Guillermo Zenon de la Cámara<br>
            Mag. Nilda Lozano<br>
            Prof. Gloria Cano
        </div>
        <div style='font-size: 10px; color: #999; margin-top: 10px;'>
            Powered by Streamlit & Gemini
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. PANEL CENTRAL (PROFESOR) ---
st.title("Monitor de Clase: IA y Pensamiento Crítico")
st.markdown("### 📊 Tablero de Control en Tiempo Real")

if len(votos_globales) > 0:
    df = pd.DataFrame(votos_globales)
    
    # MÉTRICAS
    c1, c2, c3 = st.columns(3)
    c1.metric("Alumnos", len(df))
    
    promedio = df["Puntaje"].mean()
    c2.metric("Calificación Promedio", f"{promedio:.1f} / 3.0")
    
    # Porcentaje de Pensamiento Crítico
    criticos = len(df[df["P3_Critica"].str.contains("mirada crítica")])
    porc_criticos = (criticos / len(df)) * 100
    c3.metric("Nivel de Pensamiento Crítico", f"{porc_criticos:.0f}%")

    # --- ZONA ADMINISTRACIÓN (CLAVE: unju2025) ---
    with st.expander("🔐 ADMINISTRACIÓN DOCENTE"):
        passw = st.text_input("Clave:", type="password")
        if passw == "unju2025":
            st.success("Modo Admin Activo")
            ca, cb = st.columns(2)
            csv = df.to_csv(index=False).encode('utf-8')
            ca.download_button("📥 DESCARGAR EXCEL (CSV)", csv, "resultados_unju.csv", "text/csv")
            if cb.button("🗑️ BORRAR TODO"):
                votos_globales.clear()
                st.rerun()
    
    st.divider()

    # --- GRÁFICOS ---
    
    # 1. Opinión Inicial
    st.subheader("1. Diagnóstico de Percepción")
    fig_op = px.bar(df['Opinion'].value_counts().reset_index(), x='Opinion', y='count', 
                    title="¿Confianza en detección humana?", color='Opinion',
                    color_discrete_sequence=['#003057', '#cea133', '#A0A0A0'])
    st.plotly_chart(fig_op, use_container_width=True)

    # 2. Resultados de Aprendizaje (3 Conceptos)
    st.subheader("2. Validación de Conocimientos")
    cg1, cg2, cg3 = st.columns(3)
    
    with cg1:
        st.markdown("**Concepto: Simulación**")
        vals1 = df["P1_Plagio"].apply(lambda x: "Correcto" if "Simula" in x else "Incorrecto")
        st.plotly_chart(px.pie(names=vals1, color=vals1, color_discrete_map={"Correcto":"#28a745", "Incorrecto":"#dc3545"}), use_container_width=True)

    with cg2:
        st.markdown("**Concepto: Explosividad**")
        vals2 = df["P2_Explosividad"].apply(lambda x: "Correcto" if "variabilidad" in x else "Incorrecto")
        st.plotly_chart(px.pie(names=vals2, color=vals2, color_discrete_map={"Correcto":"#28a745", "Incorrecto":"#dc3545"}), use_container_width=True)

    with cg3:
        st.markdown("**Concepto: Mirada Crítica**")
        vals3 = df["P3_Critica"].apply(lambda x: "Correcto" if "mirada crítica" in x else "Incorrecto")
        st.plotly_chart(px.pie(names=vals3, color=vals3, color_discrete_map={"Correcto":"#28a745", "Incorrecto":"#dc3545"}), use_container_width=True)

    # Tabla Resumen
    st.divider()
    st.caption("Últimos registros recibidos:")
    st.dataframe(df[["Nombre", "Puntaje", "P3_Critica"]].tail(5), use_container_width=True, hide_index=True)

else:
    st.info("👋 Esperando a los alumnos... Escaneen el QR para comenzar la experiencia.")

if st.button("🔄 ACTUALIZAR DATOS"):
    st.rerun()
