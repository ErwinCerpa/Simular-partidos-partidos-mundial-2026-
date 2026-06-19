import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Simulador Mundial 2026", layout="wide")
st.title("⚽ Simulador Inteligente: Fase Final")

# Configuración de pesos
elo_w = st.sidebar.slider("Peso ELO", 0.0, 1.0, 0.3)
tac_w = st.sidebar.slider("Peso Táctico", 0.0, 1.0, 0.3)
log_w = st.sidebar.slider("Peso Logística", 0.0, 1.0, 0.2)
psi_w = st.sidebar.slider("Peso Psicología", 0.0, 1.0, 0.2)
pesos = np.array([elo_w, tac_w, log_w, psi_w])

def simular_partido(eq1, eq2):
    # Buscar datos del equipo en el df global (asegurar que existan)
    delta = np.array([eq1['ELO'] - eq2['ELO'], eq1['Tactico'] - eq2['Tactico'], 
                      eq1['Logistica'] - eq2['Logistica'], eq1['Psicologia'] - eq2['Psicologia']])
    prob = 1 / (1 + np.exp(-np.dot(delta, pesos)))
    return eq1 if np.random.rand() < prob else eq2

# Carga y Procesamiento
uploaded_file = st.file_uploader("Sube tu archivo equipos.csv", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='latin1')
    
    if st.button("🚀 Iniciar Torneo Completo"):
        # 1. Fase de Grupos
        clasificados = []
        for grupo, datos_grupo in df.groupby('Grupo'):
            puntos = {nombre: 0 for nombre in datos_grupo['Nombre']}
            equipos_dict = datos_grupo.to_dict('records')
            for i in range(len(equipos_dict)):
                for j in range(i + 1, len(equipos_dict)):
                    ganador = simular_partido(equipos_dict[i], equipos_dict[j])
                    puntos[ganador['Nombre']] += 3
            top_2 = pd.Series(puntos).nlargest(2).index.tolist()
            clasificados.extend([datos_grupo[datos_grupo['Nombre'] == t].iloc[0].to_dict() for t in top_2])
        
        st.write("✅ Fase de grupos finalizada. Iniciando eliminatorias...")
        
        # 2. Fase de Eliminación (Dieciseisavos a Final)
        ronda = clasificados
        while len(ronda) > 1:
            siguiente_ronda = []
            for i in range(0, len(ronda), 2):
                ganador = simular_partido(ronda[i], ronda[i+1])
                siguiente_ronda.append(ganador)
            ronda = siguiente_ronda
            st.write(f"--- Ronda de {len(ronda)*2} --- Ganadores: {[e['Nombre'] for e in ronda]}")
            
        st.success(f"🏆 ¡EL CAMPEÓN DEL MUNDIAL ES: {ronda[0]['Nombre']}!")