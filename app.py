
import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Laboratorio de Densidad Avanzado",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Función de IA para el feedback del tutor
@st.cache_data(show_spinner=False)
def get_ai_feedback(mass, volume, liquid_density):
    density = mass / volume
    try:
        api_key = os.environ.get("API_KEY")
        if not api_key: return "Configura tu API_KEY para recibir consejos del tutor."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        liquid_name = "Agua"
        if liquid_density < 1: liquid_name = "Aceite"
        elif liquid_density > 1: liquid_name = "Miel"

        prompt = f"""
        Actúa como un tutor de física. Un objeto de {mass}g y {volume}cm³ (ρ={density:.2f}) 
        está en un líquido llamado {liquid_name} que tiene una densidad de {liquid_density} g/cm³.
        Explica brevemente por qué flota o se hunde y da un dato curioso sobre este material o líquido.
        Máximo 2-3 frases muy claras.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Densidad del objeto: {density:.2f} g/cm³. En {liquid_name} ({liquid_density} g/cm³), el objeto {'flotará' if density <= liquid_density else 'se hundirá'}."

# 3. El Corazón de la App: Componente HTML/JS de alto rendimiento
def dense_lab_component():
    html_code = """
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #020617; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }
        .slider-indigo::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; background: #6366f1; cursor: pointer; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(99,102,241,0.5); }
        .slider-emerald::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; background: #10b981; cursor: pointer; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(16,185,129,0.5); }
        .glass { background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.1); }
        input[type=range] { -webkit-appearance: none; background: #1e293b; height: 8px; border-radius: 4px; outline: none; }
        .liquid-wave { transition: fill 0.5s ease; }
    </style>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 p-4 h-[650px]">
        <!-- VISUALIZADOR (Lado Izquierdo) -->
        <div class="lg:col-span-8 relative glass rounded-[2.5rem] p-8 overflow-hidden flex flex-col">
            <div class="flex justify-between items-center mb-4 z-10">
                <div class="flex items-center gap-3">
                    <div id="status-icon" class="w-3 h-3 rounded-full animate-pulse"></div>
                    <h2 id="status-text" class="text-xs font-black uppercase tracking-widest text-slate-400">Calculando...</h2>
                </div>
                <div id="liquid-label" class="px-4 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-[10px] font-bold text-blue-400 uppercase tracking-widest">Entorno: Agua</div>
            </div>
            
            <div class="flex-1 flex items-center justify-center relative">
                <svg id="canvas" viewBox="0 0 800 600" class="w-full max-w-[650px] drop-shadow-[0_20px_50px_rgba(0,0,0,0.5)]">
                    <!-- Regla Graduada -->
                    <g opacity="0.15">
                        <line x1="60" y1="100" x2="60" y2="550" stroke="white" stroke-width="2" />
                        <line x1="60" y1="550" x2="740" y2="550" stroke="white" stroke-width="2" />
                        <text x="30" y="555" fill="white" font-size="12">0</text>
                        <text x="20" y="255" fill="white" font-size="12">500</text>
                        <text x="20" y="105" fill="white" font-size="12">1000</text>
                        <line x1="55" y1="250" x2="65" y2="250" stroke="white" stroke-width="2" />
                    </g>

                    <!-- Líquido -->
                    <rect id="water-rect" x="80" y="250" width="640" height="300" rx="10" fill="#3b82f6" fill-opacity="0.3" class="liquid-wave" />
                    <line id="water-line" x1="80" y1="250" x2="720" y2="250" stroke="#3b82f6" stroke-width="3" stroke-dasharray="8,4" />
                    
                    <!-- Objeto -->
                    <g id="obj-group" style="transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);">
                        <rect id="obj-rect" rx="12" fill="#f8fafc" stroke-width="4" stroke="#6366f1" />
                        <g id="obj-particles"></g>
                        <text id="obj-info" text-anchor="middle" font-weight="bold" font-family="monospace" font-size="14" fill="rgba(0,0,0,0.4)"></text>
                    </g>
                </svg>
            </div>

            <!-- Selector de Líquidos (HUD) -->
            <div class="absolute bottom-8 right-8 flex gap-3 z-10">
                <button onclick="setLiquid(0.8, 'Aceite', '#f59e0b')" class="px-4 py-2 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-500 text-[10px] font-black uppercase transition-all">Aceite</button>
                <button onclick="setLiquid(1.0, 'Agua', '#3b82f6')" class="px-4 py-2 rounded-xl bg-blue-500/10 hover:bg-blue-500/20 text-blue-500 text-[10px] font-black uppercase transition-all border border-blue-500/30">Agua</button>
                <button onclick="setLiquid(1.4, 'Miel', '#ea580c')" class="px-4 py-2 rounded-xl bg-orange-600/10 hover:bg-orange-600/20 text-orange-600 text-[10px] font-black uppercase transition-all">Miel</button>
            </div>
        </div>

        <!-- CONTROLES (Lado Derecho) -->
        <div class="lg:col-span-4 glass rounded-[2.5rem] p-10 flex flex-col gap-8">
            <div class="mb-4">
                <h1 class="text-3xl font-black italic tracking-tighter bg-gradient-to-br from-indigo-400 to-emerald-400 bg-clip-text text-transparent">LAB DENSIDAD</h1>
                <p class="text-slate-500 text-xs font-bold uppercase tracking-widest mt-1">Simulación Física de Precisión</p>
            </div>

            <!-- Presets -->
            <div class="flex flex-wrap gap-2">
                <button onclick="setMaterial(0.5, '#78350f', 'Madera')" class="px-3 py-1.5 rounded-lg bg-slate-800 text-[9px] font-bold text-slate-400 hover:text-white transition-colors uppercase">Madera</button>
                <button onclick="setMaterial(0.9, '#e2e8f0', 'Hielo')" class="px-3 py-1.5 rounded-lg bg-slate-800 text-[9px] font-bold text-slate-400 hover:text-white transition-colors uppercase">Hielo</button>
                <button onclick="setMaterial(7.8, '#64748b', 'Acero')" class="px-3 py-1.5 rounded-lg bg-slate-800 text-[9px] font-bold text-slate-400 hover:text-white transition-colors uppercase">Acero</button>
                <button onclick="setMaterial(19.3, '#fbbf24', 'Oro')" class="px-3 py-1.5 rounded-lg bg-slate-800 text-[9px] font-bold text-slate-400 hover:text-white transition-colors uppercase">Oro</button>
            </div>

            <!-- Masa Slider -->
            <div class="space-y-4">
                <div class="flex justify-between items-end">
                    <label class="text-[10px] font-black text-slate-500 uppercase">Masa (m)</label>
                    <div class="flex items-baseline gap-1">
                        <span id="m-val" class="text-3xl font-mono font-black text-indigo-400">250</span>
                        <span class="text-slate-600 text-xs font-bold">g</span>
                    </div>
                </div>
                <input type="range" id="m-slider" min="1" max="1000" value="250" class="w-full slider-indigo">
            </div>

            <!-- Volumen Slider -->
            <div class="space-y-4">
                <div class="flex justify-between items-end">
                    <label class="text-[10px] font-black text-slate-500 uppercase">Volumen (V)</label>
                    <div class="flex items-baseline gap-1">
                        <span id="v-val" class="text-3xl font-mono font-black text-emerald-400">500</span>
                        <span class="text-slate-600 text-xs font-bold">cm³</span>
                    </div>
                </div>
                <input type="range" id="v-slider" min="10" max="1000" value="500" class="w-full slider-emerald">
            </div>

            <!-- Densidad Display -->
            <div class="mt-auto pt-8 border-t border-slate-800/50">
                <label class="text-[10px] font-black text-slate-600 uppercase mb-2 block">Densidad Resultante (ρ = m/V)</label>
                <div class="flex items-baseline gap-3">
                    <span id="d-val" class="text-7xl font-black font-mono tracking-tighter text-white">0.50</span>
                    <span class="text-slate-500 text-sm font-bold italic">g/cm³</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        const mS = document.getElementById('m-slider');
        const vS = document.getElementById('v-slider');
        const mD = document.getElementById('m-val');
        const vD = document.getElementById('v-val');
        const dD = document.getElementById('d-val');
        
        const obj = document.getElementById('obj-rect');
        const grp = document.getElementById('obj-group');
        const inf = document.getElementById('obj-info');
        const prt = document.getElementById('obj-particles');
        const water = document.getElementById('water-rect');
        const wLine = document.getElementById('water-line');
        const badge = document.getElementById('status-text');
        const bIcon = document.getElementById('status-icon');
        const lLabel = document.getElementById('liquid-label');

        let liquidD = 1.0;
        let debounceTimer;

        function setLiquid(d, name, color) {
            liquidD = d;
            water.style.fill = color;
            wLine.style.stroke = color;
            lLabel.innerText = "Entorno: " + name;
            lLabel.style.color = color;
            lLabel.style.borderColor = color + "44";
            update();
        }

        function setMaterial(d, color, name) {
            vS.value = 400;
            mS.value = Math.round(400 * d);
            obj.style.fill = color;
            update();
        }

        function update() {
            const m = parseFloat(mS.value);
            const v = parseFloat(vS.value);
            const d = m / v;

            mD.innerText = m;
            vD.innerText = v;
            dD.innerText = d.toFixed(2);
            dD.style.color = d > liquidD ? '#f43f5e' : '#10b981';

            // Visualización Física
            const size = Math.pow(v, 0.45) * 10 + 20;
            const waterLevel = 250;
            let y;

            if (d <= liquidD) {
                const immersed = size * (d / liquidD);
                y = waterLevel - (size - immersed);
                badge.innerText = "Flotación Positiva";
                bIcon.style.backgroundColor = "#10b981";
                obj.style.stroke = "#10b981";
            } else {
                y = 550 - size;
                badge.innerText = "Flotación Negativa";
                bIcon.style.backgroundColor = "#f43f5e";
                obj.style.stroke = "#f43f5e";
            }

            obj.setAttribute('width', size);
            obj.setAttribute('height', size);
            inf.setAttribute('x', size/2);
            inf.setAttribute('y', size/2 + 5);
            inf.innerText = d.toFixed(2);
            grp.setAttribute('transform', `translate(${400 - size/2}, ${y})`);

            // Partículas de masa
            let dots = "";
            const count = Math.min(m / 2, 250);
            for(let i=0; i<count; i++) {
                dots += `<circle cx="${Math.random()*size}" cy="${Math.random()*size}" r="1.5" fill="rgba(0,0,0,0.15)" />`;
            }
            prt.innerHTML = dots;

            // Debounce para Streamlit (IA)
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                if (window.parent.Streamlit) {
                    window.parent.postMessage({
                        type: 'streamlit:setComponentValue',
                        value: { mass: m, vol: v, liquid: liquidD }
                    }, '*');
                }
            }, 500);
        }

        mS.oninput = update;
        vS.oninput = update;
        update();
    </script>
    """
    return components.html(html_code, height=680)

# 4. Renderizado Final
st.markdown("<div style='margin-bottom: -30px;'></div>", unsafe_allow_html=True)

# Capturamos datos del componente
result = dense_lab_component()

# UI de la IA abajo
if result:
    m, v, ld = result['mass'], result['vol'], result['liquid']
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🤖 Tutoría de Inteligencia Artificial")
        with st.status("Consultando con el tutor de física...", expanded=True) as status:
            feedback = get_ai_feedback(m, v, ld)
            st.write(feedback)
            status.update(label="Análisis completado", state="complete", expanded=True)
            
    with col2:
        st.subheader("💡 Reto")
        st.markdown(f"""
        **¿Puedes hacer que el objeto flote en Miel pero se hunda en Aceite?**
        
        Ajusta la masa y el volumen hasta que la densidad esté entre **0.8 y 1.4**.
        """)
else:
    st.info("👋 ¡Bienvenido! Interactúa con los controles arriba para iniciar el análisis del Tutor IA.")

# Estilos adicionales para que se vea premium en Streamlit
st.markdown("""
<style>
    .stApp { background-color: #020617; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    .stAlert { border-radius: 20px; background-color: #0f172a; border: 1px solid #1e293b; color: #94a3b8; }
</style>
""", unsafe_allow_html=True)
