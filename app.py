
import streamlit as st
import streamlit.components.v1 as components
import os

# 1. Configuración de alto rendimiento
st.set_page_config(
    page_title="Laboratorio de Densidad 3.0",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para asegurar que la app se vea limpia y oscura
st.markdown("""
<style>
    .stApp { background-color: #020617; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    /* Eliminar espacios innecesarios */
    .block-container { padding-top: 0rem; padding-bottom: 0rem; }
</style>
""", unsafe_allow_html=True)

# 2. Conexión con el componente React
# Obtenemos la ruta absoluta de la carpeta actual
current_path = os.path.dirname(os.path.abspath(__file__))

# Declaramos el componente. Streamlit buscará el index.html
_density_lab = components.declare_component(
    "density_lab",
    path=current_path
)

def run_app():
    # El componente devuelve 'result' cuando el usuario mueve los sliders
    # Por defecto es None hasta que el componente se monta en el navegador
    result = _density_lab()

    if result is None:
        # Pantalla de carga elegante mientras React se inicia
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh; color: #6366f1;">
                <h2 style="font-family: sans-serif; font-weight: 900; letter-spacing: -0.05em;">CARGANDO LABORATORIO...</h2>
                <p style="color: #475569; font-size: 0.8rem; font-weight: bold;">PREPARANDO SIMULACIÓN FÍSICA Y TUTOR IA</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Si quisiéramos hacer algo con los datos en Python (ej. guardar en DB),
        # lo haríamos aquí. Pero para la visualización, React ya lo hace todo.
        pass

if __name__ == "__main__":
    run_app()
