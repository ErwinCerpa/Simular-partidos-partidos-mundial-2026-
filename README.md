Simulador Mundial 2026: Inteligencia Predictiva.
Este proyecto es un simulador avanzado diseñado para predecir el campeón de la Copa Mundial 2026. Utiliza un enfoque multivariable basado en Simulaciones de Monte Carlo y Regresión Logística, procesando el nuevo formato de 48 equipos de la FIFA. 
Funcionamiento del Modelo.
El programa no utiliza azar puro; cada partido es un evento estadístico calculado mediante la diferencia de fuerzas entre dos selecciones bajo cuatro pilares determinantes.

1. Factores Determinantes (Δ)
El modelo calcula la probabilidad de victoria (P) basándose en el vector de diferencia entre el equipo A y el equipo B:
        - ELO (30%): Valor histórico de fortaleza competitiva.
        - Táctico (30%): Eficiencia en bloque, posesión y Expected Goals (xG).
        - Logística (20%): Impacto del factor local (EE.UU., México, Canadá) y desgaste por viajes.
        - Psicología (20%): Resiliencia histórica en escenarios límite (penales, remontadas).

2. Base Matemática
El núcleo del cálculo es una función sigmoide aplicada a la diferencia ponderada de fuerzas:

z = β₁(ELO₁ - ELO₂) + β₂(Tac₁ - Tac₂) + β₃(Log₁ - Log₂) + β₄(Psi₁ - Psi₂)

                        P(Victoria₁) = 1 / 1 + e⁻ᶻ

Donde β representa el peso específico de cada factor. El sistema genera 1,000 interacciones (Monte Carlo) para determinar la probabilidad de campeonato de cada país, eliminando el sesgo de un resultado único. 

Tecnologías Utilizadas
1. Python 3.13: Motor de cálculo.
2. Streamlit: Interfaz gráfica web interactiva.
3. Pandas & NumPy: Procesamiento de datos matriciales.


Contribuciones y Mejoras.
Este proyecto es de código abierto y busco hacerlo más preciso. Si deseas contribuir, aquí tienes algunas áreas de oportunidad:
        Integración de APIs: Conectar datos reales de la API de la FIFA para actualizar el ELO en tiempo real.
        Ajuste de Variables: Implementar un sistema de aprendizaje automático (Machine Learning) para que el modelo ajuste los pesos (β) basándose en resultados históricos reales.
        Visualización: Añadir gráficos interactivos más avanzados (D3.js o Plotly) para el bracket de eliminación.
        
        
¡Si tienes una mejora, haz un fork del repo y envía tu Pull Request!.
