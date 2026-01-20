
import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os
import json
import random

# 1. Configuración de la página
st.set_page_config(
    page_title="Laboratorio de Densidad",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Estilos CSS (Look & Feel de Laboratorio Profesional)
st.markdown("""
    <style>
    .main { background-color: #020617; }
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        color: #6366f1;
        font-size: 3rem !important;
    }
    .tutor-card {
        background-color: #0f172a;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #1e293b;
        border-left: 5px solid #6366f1;
    }
    .card-title {
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Datos de Materiales
MATERIALS = {
    "Personalizado": {"density": None, "color": "#f8fafc"},
    "Madera": {"density": 0.70, "color": "#92400e"},
    "Hielo": {"density": 0.92, "color": "#bae6fd"},
    "Acero": {"density": 7.80, "color": "#64748b"},
    "Oro": {"density": 19.30, "color": "#fbbf24"}
}

# 4. Lógica de IA
@st.cache_data(show_spinner=False)
def get_ai_analysis(mass, volume, density):
    try:
        api_key = os.environ.get("API_KEY")
        if not api_key: return None
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3-flash-preview')
        prompt = f"Profesor de física: Explica en 2 frases por qué un objeto de {mass}g y {volume}cm3 con densidad {density:.2f} flota o se hunde. Incluye un dato curioso corto."
        response = model.generate_content(prompt)
        return response.text
    except:
        return None

# 5. Generador de Visualización SVG
def get_svg_sim(mass, volume, color):
    density = mass / volume
    is_floating = density <= 1.0
    # Escalar tamaño visual
    side = (volume ** 0.45) * 10 + 20
    water_line = 250
    
    if is_floating:
        # Parte sumergida proporcional a la densidad
        immersed = side * density
        y = water_line - (side - immersed)
    else:
        y = 550 - side # Al fondo

    stroke = "#10b981" if is_floating else "#ef4444"
    
    # Partículas (Masa)
    random.seed(42)
    dots = ""
    for _ in range(min(int(mass), 200)):
        dx, dy = random.random()*side, random.random()*side
        dots += f'<circle cx="{dx}" cy="{dy}" r="1.5" fill="rgba(0,0,0,0.2)"/>'

    return f"""
    <div style="display: flex; justify-content: center; background: #020617; border-radius: 20px; border: 1px solid #1e293b; padding: 20px;">
        <svg viewBox="0 0 800 600" style="width: 100%; max-width: 600px;">
            <rect x="0" y="{water_line}" width="800" height="350" fill="#1e40af" fill-opacity="0.4"/>
            <line x1="0" y1="{water_line}" x2="800" y2="{water_line}" stroke="#60a5fa" stroke-width="2" stroke-dasharray="10,5"/>
            <g transform="translate({400-side/2}, {y})">
                <rect width="{side}" height="{side}" fill="{color}" stroke="{stroke}" stroke-width="4" rx="5"/>
                {dots}
                <text x="{side/2}" y="{side/2}" text-anchor="middle" font-family="monospace" font-weight="bold" font-size="12" fill="black" opacity="0.5">ρ={density:.2f}</text>
            </g>
            <text x="10" y="240" font-family="sans-serif" font-size="12" fill="#60a5fa" opacity="0.6">NIVEL AGUA (ρ=1.0)</text>
        </svg>
    </div>
    """

# 6. Interfaz de Usuario
st.title("🧪 Simulador de Densidad")
st.write("Explora cómo la relación entre masa y volumen determina si un objeto flota.")

# Columnas principales
col_sim, col_ctrl = st.columns([3, 2], gap="large")

with col_ctrl:
    st.markdown('<p class="card-title">Configuración del Objeto</p>', unsafe_allow_html=True)
    
    # Selección de Material
    mat_name = st.selectbox("Selecciona un material:", list(MATERIALS.keys()))
    mat_data = MATERIALS[mat_name]
    
    # Valores iniciales según material
    default_vol = 300
    if mat_data["density"]:
        default_mass = int(default_vol * mat_data["density"])
    else:
        default_mass = 150

    # Sliders (Fuera de fragmentos para evitar errores)
    mass = st.slider("Masa (g)", 1, 1000, default_mass)
    volume = st.slider("Volumen (cm³)", 10, 1000, default_vol)
    
    density = mass / volume
    
    # Métricas
    st.divider()
    st.metric("Densidad Resultante", f"{density:.2f} g/cm³")
    
    if density <= 1.0:
        st.success("✅ El objeto es menos denso que el agua: **FLOTA**")
    else:
        st.error("❌ El objeto es más denso que el agua: **SE HUNDE**")

with col_sim:
    # Renderizado de la simulación
    html_sim = get_svg_sim(mass, volume, mat_data["color"])
    components.html(html_sim, height=500)
    
    # Panel de IA
    st.markdown('<div class="tutor-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">✨ Análisis del Tutor IA</p>', unsafe_allow_html=True)
    
    explanation = get_ai_analysis(mass, volume, density)
    if explanation:
        st.info(explanation)
    else:
        st.write(f"Un objeto con masa de {mass}g y volumen de {volume}cm³ tiene una densidad de {density:.2f} g/cm³.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("Física Interactiva • Creado para Estudiantes")
