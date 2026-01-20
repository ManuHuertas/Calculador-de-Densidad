
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

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main { background-color: #020617; }
    .stMetric {
        background-color: #0f172a;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #1e293b;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 2.5rem !important;
    }
    .tutor-box {
        background-color: #0f172a;
        border-left: 4px solid #6366f1;
        padding: 20px;
        border-radius: 0 12px 12px 0;
        margin-top: 10px;
    }
    .stSlider { padding-bottom: 20px; }
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
        Responde en formato JSON con las llaves 'explanation' y 'fact'.
        """
        response = model.generate_content(prompt)
        return json.loads(response.text.replace('```json', '').replace('```', ''))
    except:
        return {
            "explanation": f"El objeto tiene una densidad de {density:.2f} g/cm³.",
            "fact": "El agua tiene una densidad de 1.0 g/cm³."
        }

def render_visualizer(mass, volume, color):
    density = mass / volume
    is_floating = density <= 1.0
    size = (volume ** 0.48) * 8 + 35
    water_level = 240
    
    if is_floating:
        immersed_part = size * max(0.02, density)
        y_pos = water_level - (size - immersed_part)
    else:
        y_pos = 560 - size
    
    random.seed(42)
    particles_svg = ""
    for i in range(min(int(mass), 300)):
        px, py = random.uniform(0.05, 0.95) * size, random.uniform(0.05, 0.95) * size
        pr = random.uniform(1, 1.8)
        p_color = "rgba(0,0,0,0.15)" if is_floating else "rgba(255,255,255,0.08)"
        particles_svg += f'<circle cx="{px}" cy="{py}" r="{pr}" fill="{p_color}" />'

    stroke_color = "#10b981" if is_floating else "#f43f5e"
    
    return f"""
    <div style="display: flex; justify-content: center; background: #0f172a; padding: 15px; border-radius: 16px; border: 1px solid #1e293b;">
        <svg viewBox="0 0 800 600" style="width: 100%; max-width: 550px; height: auto;">
            <defs>
                <linearGradient id="wGrad" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stop-color="#1e40af" stop-opacity="0.6" />
                    <stop offset="100%" stop-color="#1e3a8a" stop-opacity="0.9" />
                </linearGradient>
            </defs>
            <rect x="0" y="560" width="800" height="40" fill="#020617" />
            <rect x="0" y="{water_level}" width="800" height="{600-water_level}" fill="url(#wGrad)" />
            <line x1="0" y1="{water_level}" x2="800" y2="{water_level}" stroke="#60a5fa" stroke-width="2" stroke-dasharray="8,6" opacity="0.4" />
            <g transform="translate({400 - size/2}, {y_pos})">
                <rect width="{size}" height="{size}" rx="8" fill="{color}" stroke="{stroke_color}" stroke-width="3" />
                {particles_svg}
                <text x="{size/2}" y="{size/2 + 5}" text-anchor="middle" fill="#000" font-family="sans-serif" font-weight="900" font-size="10" opacity="0.4">
                    ρ:{density:.2f}
                </text>
            </g>
        </svg>
    </div>
    """

# Título Principal (Fuera de fragmento)
st.title("🧪 Laboratorio de Densidad")
st.markdown("Mueve los deslizadores para observar cómo cambian las partículas y el tamaño del objeto.")

# Encabezado del Sidebar (Fuera de fragmento para evitar errores de API)
with st.sidebar:
    st.markdown("### 📊 Controles del Experimento")

@st.fragment
def experiment_block():
    # Sliders en el sidebar (dentro del fragmento para que solo actualicen esto)
    with st.sidebar:
        m_choice = st.selectbox("Material de referencia", list(MATERIALS.keys()), index=0)
        
        d_val = MATERIALS[m_choice]["density"]
        init_v = 300
        init_m = int(init_v * d_val) if d_val else 150
        
        mass_val = st.slider("Masa (g)", 1, 1000, init_m if d_val else 150)
        vol_val = st.slider("Volumen (cm³)", 10, 1000, init_v if d_val else 300)
    
    curr_density = mass_val / vol_val
    curr_color = MATERIALS[m_choice]["color"]
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown(f"#### Simulación")
        components.html(render_visualizer(mass_val, vol_val, curr_color), height=480)
        
        if curr_density <= 1.0:
            st.success(f"**FLOTA** (ρ={curr_density:.2f})")
        else:
            st.error(f"**SE HUNDE** (ρ={curr_density:.2f})")

    with c2:
        st.markdown("#### Datos")
        st.metric("Densidad (ρ)", f"{curr_density:.2f}", f"{curr_density-1:.2f} g/cm³", delta_color="inverse")
        
        st.divider()
        st.markdown("##### 🤖 Tutoría IA")
        ai_info = get_ai_explanation(mass_val, vol_val, curr_density)
        st.markdown(f"""
        <div class="tutor-box">
            <p style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 10px;">{ai_info['explanation']}</p>
            <p style="color: #fbbf24; font-size: 0.75rem; font-weight: bold; margin-bottom: 2px;">SABÍAS QUE...</p>
            <p style="color: #94a3b8; font-size: 0.75rem; font-style: italic;">{ai_info['fact']}</p>
        </div>
        """, unsafe_allow_html=True)

# Ejecutar el fragmento
experiment_block()

st.divider()
st.caption("Física Interactiva • Optimizado para Streamlit Cloud")
