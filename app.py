
import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os
import json
import random

# Configuración de la página
st.set_page_config(
    page_title="Laboratorio de Densidad Interactivo",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para mejorar la estética
st.markdown("""
    <style>
    .main {
        background-color: #020617;
    }
    .stMetric {
        background-color: #0f172a;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #1e293b;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 900;
        font-size: 3rem !important;
    }
    .tutor-box {
        background-color: #0f172a;
        border-left: 4px solid #6366f1;
        padding: 20px;
        border-radius: 0 15px 15px 0;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Configuración de materiales
MATERIALS = {
    "Manual": {"density": None, "color": "#ffffff"},
    "Madera": {"density": 0.70, "color": "#92400e"},
    "Hielo": {"density": 0.92, "color": "#f0f9ff"},
    "Acero": {"density": 7.80, "color": "#64748b"},
    "Oro": {"density": 19.30, "color": "#facc15"}
}

# Inicialización de estado
if 'mass' not in st.session_state:
    st.session_state.mass = 150
if 'volume' not in st.session_state:
    st.session_state.volume = 300

# --- LÓGICA DE GEMINI ---
@st.cache_data(show_spinner=False)
def get_ai_explanation(mass, volume, density):
    try:
        api_key = os.environ.get("API_KEY")
        if not api_key:
            return {"explanation": "Configura la API_KEY para ver el análisis.", "fact": "La densidad es masa/volumen."}
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt = f"""
        Actúa como un profesor de física. Explica brevemente por qué un objeto de {mass}g y {volume}cm³ 
        (densidad {density:.2f} g/cm³) flota o se hunde en agua. 
        Responde en formato JSON con las llaves 'explanation' y 'fact' (un dato curioso corto).
        """
        
        response = model.generate_content(prompt)
        data = json.loads(response.text.replace('```json', '').replace('```', ''))
        return data
    except Exception as e:
        return {
            "explanation": f"El objeto tiene una densidad de {density:.2f} g/cm³.",
            "fact": "El agua tiene una densidad de 1.0 g/cm³."
        }

# --- RENDERIZADO DEL VISUALIZADOR SVG ---
def render_visualizer(mass, volume, color):
    density = mass / volume
    is_floating = density <= 1.0
    
    # Cálculos de tamaño y posición (basados en la lógica de React anterior)
    size = (volume ** 0.48) * 8 + 35
    water_level = 240
    
    if is_floating:
        immersed_part = size * max(0.02, density)
        y_pos = water_level - (size - immersed_part)
    else:
        y_pos = 560 - size
    
    # Generar partículas estables usando el volumen como semilla
    random.seed(42)
    particles_svg = ""
    for i in range(min(int(mass), 300)):
        px = random.uniform(0.05, 0.95) * size
        py = random.uniform(0.05, 0.95) * size
        pr = random.uniform(1, 2)
        p_color = "rgba(0,0,0,0.2)" if is_floating else "rgba(255,255,255,0.1)"
        particles_svg += f'<circle cx="{px}" cy="{py}" r="{pr}" fill="{p_color}" />'

    stroke_color = "#10b981" if is_floating else "#f43f5e"
    
    svg_html = f"""
    <div style="display: flex; justify-content: center; background: #0f172a; padding: 20px; border-radius: 20px; border: 1px solid #1e293b;">
        <svg viewBox="0 0 800 600" style="width: 100%; max-width: 600px; height: auto; border-radius: 10px;">
            <defs>
                <linearGradient id="waterGrad" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stop-color="#1e40af" stop-opacity="0.6" />
                    <stop offset="100%" stop-color="#1e3a8a" stop-opacity="0.9" />
                </linearGradient>
            </defs>
            <!-- Suelo -->
            <rect x="0" y="560" width="800" height="40" fill="#020617" />
            <!-- Agua -->
            <rect x="0" y="{water_level}" width="800" height="{600-water_level}" fill="url(#waterGrad)" />
            <!-- Superficie -->
            <line x1="0" y1="{water_level}" x2="800" y2="{water_level}" stroke="#60a5fa" stroke-width="2" stroke-dasharray="8,6" opacity="0.5" />
            
            <!-- Objeto -->
            <g transform="translate({400 - size/2}, {y_pos})" style="transition: all 0.5s ease-out;">
                <rect width="{size}" height="{size}" rx="8" fill="{color}" stroke="{stroke_color}" stroke-width="3" />
                {particles_svg}
                <text x="{size/2}" y="{size/2 + 5}" text-anchor="middle" fill="#000" font-family="sans-serif" font-weight="bold" font-size="12" opacity="0.5">
                    ρ:{density:.2f}
                </text>
            </g>
        </svg>
    </div>
    """
    return svg_html

# --- INTERFAZ DE USUARIO (SIDEBAR) ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/physics.png", width=60)
    st.title("Ajustes")
    
    material_choice = st.selectbox("Selecciona un material", list(MATERIALS.keys()))
    
    # Si se elige un material, forzar los sliders
    if MATERIALS[material_choice]["density"] is not None:
        target_density = MATERIALS[material_choice]["density"]
        st.session_state.volume = 300
        st.session_state.mass = int(300 * target_density)
    
    st.divider()
    
    mass = st.slider("Masa (g)", 1, 1000, st.session_state.mass, key="mass_slider")
    volume = st.slider("Volumen (cm³)", 10, 1000, st.session_state.volume, key="volume_slider")
    
    # Actualizar estado para sincronía
    st.session_state.mass = mass
    st.session_state.volume = volume

# --- CUERPO PRINCIPAL ---
density = mass / volume

col_vis, col_data = st.columns([2, 1])

with col_vis:
    st.markdown(f"### Laboratorio Virtual")
    color = MATERIALS[material_choice]["color"]
    st.components.v1.html(render_visualizer(mass, volume, color), height=500)
    
    # Banner de estado
    if density <= 1.0:
        st.success(f"✅ El objeto **FLOTA** (Densidad {density:.2f} < 1.00)")
    else:
        st.error(f"⚓ El objeto **SE HUNDE** (Densidad {density:.2f} > 1.00)")

with col_data:
    st.markdown("### Datos del Experimento")
    st.metric("Densidad Resultante", f"{density:.2f} g/cm³", delta=f"{density-1:.2f} vs Agua", delta_color="inverse")
    
    st.divider()
    
    # Sección del Tutor IA
    st.markdown("### 🤖 Tutor IA")
    ai_data = get_ai_explanation(mass, volume, density)
    
    st.markdown(f"""
    <div class="tutor-box">
        <p style="color: #cbd5e1; font-size: 0.9rem;">{ai_data['explanation']}</p>
        <hr style="border: 0; border-top: 1px solid #334155; margin: 15px 0;">
        <p style="color: #fbbf24; font-size: 0.8rem; font-weight: bold;">💡 SABÍAS QUE...</p>
        <p style="color: #94a3b8; font-size: 0.8rem; font-style: italic;">{ai_data['fact']}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("Física Interactiva v3.0 | Desarrollado para Streamlit Cloud")
