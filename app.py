import streamlit as st
import pandas as pd
import numpy as np

# 1. Definición de la Base de Datos (Global)
data = {
    'Nombre': ['Mexico', 'Corea del Sur', 'Rep. Checa', 'Sudafrica', 'Argentina', 'Marruecos', 'Escocia', 'Bolivia', 'EEUU', 'Suiza', 'Nigeria', 'Panama', 'Brasil', 'Japon', 'Serbia', 'Australia', 'Francia', 'Colombia', 'Grecia', 'Canada', 'Inglaterra', 'Ecuador', 'Turquia', 'Argelia', 'Alemania', 'Chile', 'Islandia', 'Iran', 'España', 'Noruega', 'Ghana', 'Corea del Norte', 'Portugal', 'Dinamarca', 'Tunez', 'Honduras', 'Uruguay', 'Polonia', 'Costa Rica', 'Jamaica', 'Italia', 'Senegal', 'Paraguay', 'Austria', 'Croacia', 'Suecia', 'Egipto', 'Arabia Saudita'],
    'ELO': [8.2, 7.4, 7.1, 6.5, 9.5, 7.6, 6.8, 6.0, 8.0, 7.5, 7.0, 6.5, 9.3, 7.8, 7.2, 6.9, 9.6, 7.9, 6.9, 7.4, 9.2, 7.5, 7.1, 6.8, 9.0, 7.3, 6.7, 7.0, 9.1, 7.6, 6.9, 6.2, 8.9, 7.7, 6.8, 6.4, 8.5, 7.2, 6.8, 6.6, 8.7, 7.5, 7.0, 7.4, 8.3, 7.5, 7.1, 6.5],
    'Tactico': [7.6, 7.8, 7.3, 6.0, 9.2, 7.5, 6.9, 5.8, 7.7, 7.6, 7.0, 6.4, 9.0, 8.2, 7.1, 6.8, 9.4, 8.0, 7.0, 7.2, 9.1, 7.4, 7.2, 6.7, 8.9, 7.3, 6.5, 6.9, 9.3, 7.5, 6.8, 6.5, 8.8, 7.6, 6.7, 6.3, 8.3, 7.1, 6.6, 6.5, 8.6, 7.4, 6.9, 7.3, 8.2, 7.4, 7.0, 6.4],
    'Logistica': [9.5, 6.8, 7.2, 6.0, 8.0, 7.0, 7.5, 6.0, 9.0, 7.3, 6.5, 7.8, 7.5, 6.9, 7.2, 6.5, 7.8, 8.5, 7.0, 8.5, 7.5, 8.2, 7.1, 6.8, 7.6, 8.0, 6.8, 6.5, 7.4, 7.2, 6.5, 6.0, 7.2, 7.3, 6.6, 7.5, 8.0, 7.2, 8.0, 7.5, 7.4, 7.0, 7.8, 7.4, 7.2, 7.2, 6.8, 6.2],
    'Psicologia': [8.1, 7.7, 7.2, 6.5, 9.6, 8.5, 7.0, 6.0, 7.9, 7.6, 7.8, 6.8, 9.2, 7.8, 7.0, 7.2, 9.3, 8.2, 7.0, 7.5, 8.8, 7.7, 7.3, 7.2, 8.5, 7.8, 6.8, 7.3, 8.6, 7.1, 7.5, 7.5, 8.4, 7.6, 7.0, 7.0, 9.0, 7.1, 7.5, 6.8, 8.2, 8.0, 7.5, 7.0, 9.1, 7.4, 7.6, 6.8]
}
df = pd.DataFrame(data)

# Configuración de grupos
grupos_data = {
    "A": ["Mexico", "Corea del Sur", "Rep. Checa", "Sudafrica"],
    "B": ["Argentina", "Marruecos", "Escocia", "Bolivia"],
    "C": ["EEUU", "Suiza", "Nigeria", "Panama"],
    "D": ["Brasil", "Japon", "Serbia", "Australia"],
    "E": ["Francia", "Colombia", "Grecia", "Canada"],
    "F": ["Inglaterra", "Ecuador", "Turquia", "Argelia"],
    "G": ["Alemania", "Chile", "Islandia", "Iran"],
    "H": ["España", "Noruega", "Ghana", "Corea del Norte"],
    "I": ["Portugal", "Dinamarca", "Tunez", "Honduras"],
    "J": ["Uruguay", "Polonia", "Costa Rica", "Jamaica"],
    "K": ["Italia", "Senegal", "Paraguay", "Austria"],
    "L": ["Croacia", "Suecia", "Egipto", "Arabia Saudita"]
}

# Interfaz
st.title("⚽ Simulador Mundial 2026")
elo_w = st.sidebar.slider("Peso ELO", 0.0, 1.0, 0.3, key="s1")
tac_w = st.sidebar.slider("Peso Táctico", 0.0, 1.0, 0.3, key="s2")
log_w = st.sidebar.slider("Peso Logística", 0.0, 1.0, 0.2, key="s3")
psi_w = st.sidebar.slider("Peso Psicología", 0.0, 1.0, 0.2, key="s4")
pesos = np.array([elo_w, tac_w, log_w, psi_w])

def simular_partido(n1, n2):
    eq1 = df[df['Nombre'] == n1].iloc[0]
    eq2 = df[df['Nombre'] == n2].iloc[0]
    delta = np.array([eq1['ELO']-eq2['ELO'], eq1['Tactico']-eq2['Tactico'], eq1['Logistica']-eq2['Logistica'], eq1['Psicologia']-eq2['Psicologia']])
    prob = 1 / (1 + np.exp(-np.dot(delta, pesos)))
    return n1 if np.random.rand() < prob else n2

if st.button("📊 Ejecutar 10,000 Simulaciones"):
    conteo = {e: 0 for e in df['Nombre']}
    barra = st.progress(0)
    for sim in range(10000):
        clasificados = []
        lista_terceros = []
        for letra, miembros in grupos_data.items():
            pts = {e: 0 for e in miembros}
            for i in range(len(miembros)):
                for j in range(i+1, len(miembros)):
                    pts[simular_partido(miembros[i], miembros[j])] += 3
            rank = pd.Series(pts).sort_values(ascending=False)
            clasificados.extend([rank.index[0], rank.index[1]])
            lista_terceros.append((rank.index[2], pts[rank.index[2]]))
        clasificados.extend([t[0] for t in sorted(lista_terceros, key=lambda x: x[1], reverse=True)[:8]])
        
        ronda = clasificados
        while len(ronda) > 1:
            ronda = [simular_partido(ronda[i], ronda[i+1]) for i in range(0, len(ronda), 2)]
        conteo[ronda[0]] += 1
        if sim % 100 == 0: barra.progress(sim/10000)
    
    res = pd.DataFrame(list(conteo.items()), columns=['Pais', 'Victorias'])
    res['Probabilidad (%)'] = (res['Victorias'] / 100)
    st.bar_chart(res.set_index('Pais'))
    st.dataframe(res.sort_values(by='Probabilidad (%)', ascending=False))
