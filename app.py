
import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os
import json

# 1. Configuración de la página
st.set_page_config(
    page_title="Laboratorio de Densidad PRO",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Lógica de IA (Gemini)
@st.cache_data(show_spinner=False)
def get_ai_tutor_feedback(mass, volume):
    density = mass / volume
    try:
        api_key = os.environ.get("API_KEY")
        if not api_key: return "Configura tu API_KEY para recibir consejos del tutor."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3-flash-preview')
        prompt = f"""
        Como un tutor de física experto, analiza un objeto de {mass}g y {volume}cm³ (ρ={density:.2f}).
        Explica brevemente por qué flota o se hunde y da un consejo para cambiar su flotabilidad.
        Máximo 2 frases.
        """
        response = model.generate_content(prompt)
        return response.text
    except:
        return f"Densidad: {density:.2f} g/cm³. Los objetos con densidad menor a 1.0 flotan en agua."

# 3. Componente Interactivo (HTML + JS + Tailwind)
# Este bloque maneja la interactividad 100% fluida en el navegador.
def interactive_lab():
    html_code = """
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #020617; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }
        .slider-thumb::-webkit-slider-thumb {
            -webkit-appearance: none; appearance: none;
            width: 18px; height: 18px; background: #6366f1;
            cursor: pointer; border-radius: 50%; border: 2px solid white;
        }
        .glass-panel {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 p-4 h-full">
        <!-- Panel de Simulación -->
        <div class="lg:col-span-2 relative glass-panel rounded-3xl p-6 overflow-hidden flex flex-col min-h-[500px]">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xs font-black uppercase tracking-widest text-slate-500">Simulación en Tiempo Real</h2>
                <div id="status-badge" class="px-3 py-1 rounded-full text-[10px] font-bold"></div>
            </div>
            
            <div id="canvas-container" class="flex-1 flex items-center justify-center">
                <svg id="lab-svg" viewBox="0 0 800 600" class="w-full max-w-[600px] h-auto drop-shadow-2xl">
                    <!-- Agua -->
                    <rect x="0" y="250" width="800" height="350" fill="#1e40af" fill-opacity="0.4" />
                    <line x1="0" y1="250" x2="800" y2="250" stroke="#60a5fa" stroke-width="2" stroke-dasharray="10,5" />
                    
                    <!-- Objeto -->
                    <g id="object-group" style="transition: transform 0.1s ease-out;">
                        <rect id="cube" x="0" y="0" rx="8" fill="#f8fafc" stroke-width="4" />
                        <g id="particles"></g>
                        <text id="label" x="0" y="0" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="rgba(0,0,0,0.4)"></text>
                    </g>
                </svg>
            </div>
        </div>

        <!-- Panel de Controles -->
        <div class="glass-panel rounded-3xl p-8 flex flex-col gap-10">
            <div>
                <h1 class="text-2xl font-black mb-2 bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent italic">LAB DENSIDAD</h1>
                <p class="text-slate-500 text-xs">Mueve las barras para ver cambios inmediatos.</p>
            </div>

            <!-- Masa -->
            <div class="space-y-4">
                <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">Masa (g)</span>
                    <span id="mass-val" class="text-xl font-mono font-black text-indigo-400">150</span>
                </div>
                <input type="range" id="mass-slider" min="1" max="1000" value="150" 
                    class="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer slider-thumb">
            </div>

            <!-- Volumen -->
            <div class="space-y-4">
                <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">Volumen (cm³)</span>
                    <span id="vol-val" class="text-xl font-mono font-black text-emerald-400">300</span>
                </div>
                <input type="range" id="vol-slider" min="10" max="1000" value="300" 
                    class="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer slider-thumb">
            </div>

            <!-- Lectura de Densidad -->
            <div class="mt-auto border-t border-slate-800 pt-6">
                <span class="text-[10px] font-black text-slate-600 uppercase tracking-widest block mb-1">Densidad (ρ = m/V)</span>
                <div class="flex items-baseline gap-2">
                    <span id="dens-val" class="text-6xl font-black font-mono tracking-tighter text-white">0.50</span>
                    <span class="text-slate-500 font-bold text-sm italic">g/cm³</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        const massSlider = document.getElementById('mass-slider');
        const volSlider = document.getElementById('vol-slider');
        const massText = document.getElementById('mass-val');
        const volText = document.getElementById('vol-val');
        const densText = document.getElementById('dens-val');
        const cube = document.getElementById('cube');
        const particles = document.getElementById('particles');
        const label = document.getElementById('label');
        const group = document.getElementById('object-group');
        const badge = document.getElementById('status-badge');

        function update() {
            const m = parseFloat(massSlider.value);
            const v = parseFloat(volSlider.value);
            const d = m / v;

            massText.innerText = m;
            volText.innerText = v;
            densText.innerText = d.toFixed(2);
            densText.style.color = d > 1 ? '#f43f5e' : '#10b981';

            // Visualización
            const size = Math.pow(v, 0.45) * 10 + 20;
            const waterLine = 250;
            let y;
            
            if (d <= 1) {
                const immersed = size * d;
                y = waterLine - (size - immersed);
                badge.innerText = "FLOTA";
                badge.className = "px-3 py-1 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";
                cube.style.stroke = "#10b981";
            } else {
                y = 550 - size;
                badge.innerText = "SE HUNDE";
                badge.className = "px-3 py-1 rounded-full text-[10px] font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30";
                cube.style.stroke = "#f43f5e";
            }

            cube.setAttribute('width', size);
            cube.setAttribute('height', size);
            label.setAttribute('x', size / 2);
            label.setAttribute('y', size / 2 + 5);
            label.innerText = "ρ " + d.toFixed(2);
            group.setAttribute('transform', `translate(${400 - size/2}, ${y})`);

            // Partículas
            let dots = "";
            const count = Math.min(m, 200);
            for(let i=0; i<count; i++) {
                const px = Math.random() * size;
                const py = Math.random() * size;
                dots += `<circle cx="${px}" cy="${py}" r="1.5" fill="rgba(0,0,0,0.15)" />`;
            }
            particles.innerHTML = dots;

            // Enviar a Streamlit cuando se suelta o periódicamente
            if (window.parent.Streamlit) {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: { mass: m, vol: v }
                }, '*');
            }
        }

        massSlider.oninput = update;
        volSlider.oninput = update;
        update(); // Init
    </script>
    """
    return components.html(html_code, height=700)

# 4. Renderizado Final
st.markdown("<h2 style='text-align: center; color: #6366f1; margin-bottom: 0;'>🧪 LABORATORIO DE FÍSICA</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.8rem;'>Simulación de Densidad de Alta Precisión</p>", unsafe_allow_html=True)

# Capturamos los datos enviados desde el componente JS
result = interactive_lab()

# Si recibimos datos (cuando el usuario interactúa), mostramos la IA
if result:
    m, v = result['mass'], result['vol']
    st.markdown("---")
    col_ia, col_info = st.columns([2, 1])
    
    with col_ia:
        st.markdown(f"### ✨ Tutoría IA para {m}g y {v}cm³")
        feedback = get_ai_tutor_feedback(m, v)
        st.info(feedback)
    
    with col_info:
        st.markdown("### 📚 Sabías que...")
        st.write("La densidad es una propiedad intrínseca. No importa cuánta madera tengas, si es el mismo tipo, su densidad siempre será la misma.")

else:
    st.info("💡 Mueve las barras arriba para que el Tutor IA analice tu experimento.")
