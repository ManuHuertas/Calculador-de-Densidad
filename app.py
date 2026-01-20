import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os
import json
import random

# 1. Configuración de la página (DEBE IR PRIMERO)
st.set_page_config(
    page_title="Laboratorio de Densidad",
    page_icon="🧪",
    layout="wide"
)

# 2. Configuración de materiales
MATERIALS = {
    "Manual": {"density": None, "color": "#ffffff"},
    "Madera": {"density": 0.70, "color": "#92400e"},
    "Hielo": {"density": 0.92, "color": "#f0f9ff"},
    "Acero": {"density": 7.80, "color": "#64748b"},
    "Oro": {"density": 19.30, "color": "#facc15"}
}

# 3. Lógica de la IA (con caché para no bloquear la web)
@st.cache_data(show_spinner=False)
def get_ai_explanation(mass, volume, density):
    try:
        api_key = st.secrets.get("API_KEY") # Usamos st.secrets para seguridad
        if not api_key: return None
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Explica brevemente por qué un objeto de {mass}g y {volume}cm3 (densidad {density:.2f}) flota o se hunde."
        response = model.generate_content(prompt)
        return response.text
    except:
        return "La densidad del agua es 1.00 g/cm³. Si tu objeto es mayor, se hunde."

# 4. Función para dibujar el vaso (SVG)
def render_visualizer(mass, volume, color):
    density = mass / volume
    is_floating = density <= 1.0
    size = (volume ** 0.48) * 8 + 35
    water_level = 240
    y_pos = water_level - (size * density) if is_floating else 560 - size
    stroke_color = "#10b981" if is_floating else "#f43f5e"
    
    return f"""
    <div style="display: flex; justify-content: center; background: #0f172a; padding: 15px; border-radius: 16px;">
        <svg viewBox="0 0 800 600" style="width: 100%; max-width: 500px;">
            <rect x="0" y="{water_level}" width="800" height="360" fill="#1e40af" fill-opacity="0.6" />
            <g transform="translate({400 - size/2}, {y_pos})">
                <rect width="{size}" height="{size}" rx="8" fill="{color}" stroke="{stroke_color}" stroke-width="3" />
                <text x="{size/2}" y="{size/2}" text-anchor="middle" fill="white" font-size="12">ρ:{density:.2f}</text>
            </g>
        </svg>
    </div>
    """

# 5. Bloque interactivo (FRAGMENTO para velocidad)
@st.fragment
def experiment_block():
    col_side, col_main = st.columns([1, 3])
    
    with col_side:
        st.subheader("🧪 Controles")
        m_choice = st.selectbox("Material", list(MATERIALS.keys()))
        
        # Lógica de valores automáticos
        d_preset = MATERIALS[m_choice]["density"]
        m_init = 150 if d_preset is None else int(300 * d_preset)
        
        mass = st.slider("Masa (g)", 1, 1000, m_init)
        vol = st.slider("Volumen (cm³)", 10, 1000, 300)
        
    with col_main:
        density = mass / vol
        color = MATERIALS[m_choice]["color"]
        components.html(render_visualizer(mass, vol, color), height=450)
        
        # Mostrar explicación de IA
        with st.expander("🤖 Explicación del Tutor IA"):
            info = get_ai_explanation(mass, vol, density)
            st.write(info if info else "Introduce tu API_KEY en Secrets para activar la IA.")

# Ejecución
st.title("Laboratorio de Densidad Interactivo")
experiment_block()
