import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os
import json
import random

# 1. Configuración de página
st.set_page_config(page_title="Laboratorio de Densidad", layout="wide")

# 2. Fragmento para actualización rápida
@st.fragment
def visualizador_interactivo(mass, volume, color):
    density = mass / volume
    is_floating = density <= 1.0
    
    # Renderizado del SVG (tu lógica actual)
    size = (volume ** 0.48) * 8 + 35
    water_level = 240
    y_pos = water_level - (size * density) if is_floating else 560 - size
    
    stroke_color = "#10b981" if is_floating else "#f43f5e"
    
    svg_html = f"""
    <div style="display: flex; justify-content: center; background: #0f172a; padding: 20px; border-radius: 20px;">
        <svg viewBox="0 0 800 600" style="width: 100%; max-width: 500px;">
            <rect x="0" y="240" width="800" height="360" fill="#1e40af" fill-opacity="0.6" />
            <g transform="translate({400 - size/2}, {y_pos})">
                <rect width="{size}" height="{size}" rx="8" fill="{color}" stroke="{stroke_color}" stroke-width="3" />
                <text x="{size/2}" y="{size/2}" text-anchor="middle" fill="white">ρ:{density:.2f}</text>
            </g>
        </svg>
    </div>
    """
    st.components.v1.html(svg_html, height=450)
    
    if is_floating:
        st.success(f"El objeto FLOTA (Densidad: {density:.2f})")
    else:
        st.error(f"El objeto SE HUNDE (Densidad: {density:.2f})")

# 3. Interfaz Principal
with st.sidebar:
    st.title("Ajustes")
    m = st.slider("Masa (g)", 1, 1000, 150)
    v = st.slider("Volumen (cm³)", 10, 1000, 300)
    material = st.selectbox("Material", ["Madera", "Acero", "Oro"])
    colores = {"Madera": "#92400e", "Acero": "#64748b", "Oro": "#facc15"}

# Llamada al fragmento (esto es lo que lo hace rápido)
visualizador_interactivo(m, v, colores[material])

# Sección de IA (opcional, para no ralentizar el resto)
if st.button("Pedir explicación a la IA"):
    st.write("Conectando con Gemini...")
    # Aquí iría tu función get_ai_explanation
