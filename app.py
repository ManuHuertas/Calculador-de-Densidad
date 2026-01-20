
import streamlit as st
import streamlit.components.v1 as components
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Laboratorio de Densidad Pro",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos globales para integrar el componente perfectamente
st.markdown("""
<style>
    .stApp { background-color: #020617; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    .stAlert { border-radius: 20px; background-color: #0f172a; border: 1px solid #1e293b; color: #94a3b8; }
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) { padding: 0; }
</style>
""", unsafe_allow_html=True)

# 2. Declaración del componente de React
# Nota: En este entorno de desarrollo, el componente se sirve en el mismo host.
# Usamos declare_component para establecer la comunicación bidireccional.
parent_dir = os.path.dirname(os.path.abspath(__file__))
_density_explorer = components.declare_component(
    "density_explorer",
    path=parent_dir # Esto le dice a Streamlit que busque el index.html en la raíz
)

def main():
    # Renderizamos el componente de React
    # Este componente maneja toda la simulación a 60fps
    result = _density_explorer()

    # 3. Manejo seguro de los datos devueltos (Evita el TypeError)
    if result is not None:
        # Extraemos los datos enviados por App.tsx
        # Usamos .get() por seguridad para evitar errores si falta alguna clave
        mass = result.get('mass', 150)
        volume = result.get('volume', 300)
        liquid_density = result.get('liquidDensity', 1.0)
        is_floating = result.get('isFloating', True)
        
        # Aquí podrías añadir lógica adicional en Python si fuera necesario,
        # pero como el Tutor IA ya está integrado en el componente React (App.tsx),
        # no necesitamos duplicar la lógica aquí para mantener la velocidad.
    else:
        # Mensaje de carga inicial mientras el componente React se monta
        st.info("Cargando Laboratorio Interactivo... Si tarda demasiado, refresca la página.")

if __name__ == "__main__":
    main()
