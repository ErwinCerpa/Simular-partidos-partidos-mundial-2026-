import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Simulador Mundial 2026", layout="wide")
st.title("⚽ Simulador Inteligente: Mundial 48 Equipos")

# Sidebar: Pesos
elo_w = st.sidebar.slider("Peso ELO", 0.0, 1.0, 0.3, key="s1")
tac_w = st.sidebar.slider("Peso Táctico", 0.0, 1.0, 0.3, key="s2")
log_w = st.sidebar.slider("Peso Logística", 0.0, 1.0, 0.2, key="s3")
psi_w = st.sidebar.slider("Peso Psicología", 0.0, 1.0, 0.2, key="s4")
pesos = np.array([elo_w, tac_w, log_w, psi_w])

# Base de datos completa (48 equipos)
data = {
    'Nombre': ['Mexico', 'Corea del Sur', 'Rep. Checa', 'Sudafrica', 'Argentina', 'Marruecos', 'Escocia', 'Bolivia', 'EEUU', 'Suiza', 'Nigeria', 'Panama', 'Brasil', 'Japon', 'Serbia', 'Australia', 'Francia', 'Colombia', 'Grecia', 'Canada', 'Inglaterra', 'Ecuador', 'Turquia', 'Argelia', 'Alemania', 'Chile', 'Islandia', 'Iran', 'España', 'Noruega', 'Ghana', 'Corea del Norte', 'Portugal', 'Dinamarca', 'Tunez', 'Honduras', 'Uruguay', 'Polonia', 'Costa Rica', 'Jamaica', 'Italia', 'Senegal', 'Paraguay', 'Austria', 'Croacia', 'Suecia', 'Egipto', 'Arabia Saudita'],
    'ELO': [8.2, 7.4, 7.1, 6.5, 9.5, 7.6, 6.8, 6.0, 8.0, 7.5, 7.0, 6.5, 9.3, 7.8, 7.2, 6.9, 9.6, 7.9, 6.9, 7.4, 9.2, 7.5, 7.1, 6.8, 9.0, 7.3, 6.7, 7.0, 9.1, 7.6, 6.9, 6.2, 8.9, 7.7, 6.8, 6.4, 8.5, 7.2, 6.8, 6.6, 8.7, 7.5, 7.0, 7.4, 8.3, 7.5, 7.1, 6.5],
    'Tactico': [7.6, 7.8, 7.3, 6.0, 9.2, 7.5, 6.9, 5.8, 7.7, 7.6, 7.0, 6.4, 9.0, 8.2, 7.1, 6.8, 9.4, 8.0, 7.0, 7.2, 9.1, 7.4, 7.2, 6.7, 8.9, 7.3, 6.5, 6.9, 9.3, 7.5, 6.8, 6.5, 8.8, 7.6, 6.7, 6.3, 8.3, 7.1, 6.6, 6.5, 8.6, 7.4, 6.9, 7.3, 8.2, 7.4, 7.0, 6.4],
    'Logistica': [9.5, 6.8, 7.2, 6.0, 8.0, 7.0, 7.5, 6.0, 9.0, 7.3, 6.5, 7.8, 7.5, 6.9, 7.2, 6.5, 7.8, 8.5, 7.0, 8.5, 7.5, 8.2, 7.1, 6.8, 7.6, 8.0, 6.8, 6.5, 7.4, 7.2, 6.5, 6.0, 7.2, 7.3, 6.6, 7.5, 8.0, 7.2, 8.0, 7.5, 7.4, 7.0, 7.8, 7.4, 7.2, 7.2, 6.8, 6.2],
    'Psicologia': [8.1, 7.7, 7.2, 6.5, 9.6, 8.5, 7.0, 6.0, 7.9, 7.6, 7.8, 6.8, 9.2, 7.8, 7.0, 7.2, 9.3, 8.2, 7.0, 7.5, 8.8, 7.7, 7.3, 7.2, 8.5, 7.8, 6.8, 7.3, 8.6, 7.1, 7.5, 7.5, 8.4, 7.6, 7.0, 7.0, 9.0, 7.1, 7.5, 6.8, 8.2, 8.0, 7.5, 7.0, 9.1, 7.4, 7.6, 6.8]
}
df = pd.DataFrame(data)

def simular_partido(eq1, eq2):
    delta = np.array([eq1['ELO'] - eq2['ELO'], eq1['Tactico'] - eq2['Tactico'], 
                      eq1['Logistica'] - eq2['Logistica'], eq1['Psicologia'] - eq2['Psicologia']])
    prob = 1 / (1 + np.exp(-np.dot(delta, pesos)))
    return eq1 if np.random.rand() < prob else eq2

if st.button("🚀 Iniciar Mundial 48 Equipos"):
    st.write("--- Fase de Grupos (12 grupos de 4) ---")
    clasificados = []
    lista_terceros = []

    # Procesar 12 grupos
    for i in range(12):
        grupo = df.iloc[i*4:(i+1)*4].to_dict('records')
        puntos = {e['Nombre']: 0 for e in grupo}
        for idx in range(4):
            for j in range(idx + 1, 4):
                ganador = simular_partido(grupo[idx], grupo[j])
                puntos[ganador['Nombre']] += 3
        
        ranking = pd.Series(puntos).sort_values(ascending=False)
        clasificados.extend([df[df['Nombre'] == ranking.index[0]].iloc[0].to_dict(), 
                             df[df['Nombre'] == ranking.index[1]].iloc[0].to_dict()])
        lista_terceros.append(df[df['Nombre'] == ranking.index[2]].iloc[0].to_dict())

    # Agregar los 8 mejores terceros
    clasificados.extend(sorted(lista_terceros, key=lambda x: x['ELO'], reverse=True)[:8])
    
    st.write(f"✅ 32 Equipos clasificados a Dieciseisavos.")
    
    # Fase Eliminatoria
    ronda = clasificados
    fases = ["Dieciseisavos", "Octavos", "Cuartos", "Semifinal", "Final"]
    for fase in fases:
        siguiente = []
        for i in range(0, len(ronda), 2):
            siguiente.append(simular_partido(ronda[i], ronda[i+1]))
        ronda = siguiente
        st.write(f"--- {fase} --- Ganadores: {[e['Nombre'] for e in ronda]}")
    
    st.success(f"🏆 CAMPEÓN DEL MUNDIAL: {ronda[0]['Nombre']}")
