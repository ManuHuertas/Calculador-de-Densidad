
import React, { useState, useEffect, useRef } from 'react';
import Visualizer from './components/Visualizer.tsx';
import Controls from './components/Controls.tsx';
import TutorPanel from './components/TutorPanel.tsx';
import { FlaskConical, Gauge, Zap, Waves } from 'lucide-react';
import { Streamlit } from "streamlit-component-lib";

const MATERIALS = [
  { name: 'Manual', density: null, color: 'fill-slate-100' },
  { name: 'Madera', density: 0.7, color: 'fill-amber-700' },
  { name: 'Hielo', density: 0.92, color: 'fill-blue-100' },
  { name: 'Acero', density: 7.8, color: 'fill-slate-500' },
  { name: 'Oro', density: 19.3, color: 'fill-amber-400' },
];

const LIQUIDS = [
  { name: 'Aceite', d: 0.8, color: 'bg-amber-500' },
  { name: 'Agua', d: 1.0, color: 'bg-blue-500' },
  { name: 'Miel', d: 1.4, color: 'bg-orange-600' }
];

const App: React.FC = () => {
  const [mass, setMass] = useState<number>(150);
  const [volume, setVolume] = useState<number>(300);
  const [selectedMaterial, setSelectedMaterial] = useState(MATERIALS[0]);
  const [liquidDensity, setLiquidDensity] = useState<number>(1.0);
  
  const density = mass / volume;
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // EFECTO CRÍTICO: Notificar a Streamlit INMEDIATAMENTE
  useEffect(() => {
    // Primera notificación para quitar el error amarillo y la pantalla de carga de Python
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight();
    
    // Enviar el primer valor para que 'result' en app.py deje de ser None
    Streamlit.setComponentValue({
      mass: 150,
      volume: 300,
      density: 0.5,
      liquidDensity: 1.0,
      isFloating: true
    });
  }, []);

  // Sincronización continua
  useEffect(() => {
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => {
      Streamlit.setComponentValue({
        mass,
        volume,
        density: parseFloat(density.toFixed(4)),
        liquidDensity,
        isFloating: density <= liquidDensity
      });
      Streamlit.setFrameHeight();
    }, 100);
    return () => { if (timerRef.current) clearTimeout(timerRef.current); };
  }, [mass, volume, liquidDensity]);

  const handleMaterialSelect = (material: typeof MATERIALS[0]) => {
    setSelectedMaterial(material);
    if (material.density !== null) {
      const targetVolume = 300;
      setVolume(targetVolume);
      setMass(Math.round(targetVolume * material.density));
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col overflow-hidden font-sans">
      <nav className="h-14 border-b border-slate-800 bg-slate-900/90 backdrop-blur-md flex items-center justify-between px-6 shrink-0 z-20">
        <div className="flex items-center gap-3">
          <FlaskConical className="w-5 h-5 text-indigo-500" />
          <h1 className="text-xs font-black tracking-widest uppercase">Densidad Lab</h1>
        </div>
        <div className="flex items-center gap-2 overflow-x-auto no-scrollbar py-1">
          {MATERIALS.map((m) => (
            <button
              key={m.name}
              onClick={() => handleMaterialSelect(m)}
              className={`px-3 py-1 rounded-full text-[10px] font-bold transition-all whitespace-nowrap ${
                selectedMaterial.name === m.name ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400'
              }`}
            >
              {m.name}
            </button>
          ))}
        </div>
      </nav>

      <main className="flex-1 flex flex-col lg:flex-row overflow-hidden">
        <section className="flex-1 relative bg-slate-950 p-4 flex flex-col min-h-0">
          <Visualizer mass={mass} volume={volume} materialColor={selectedMaterial.color} liquidDensity={liquidDensity} />
          
          <div className={`absolute top-8 left-8 flex items-center gap-3 px-6 py-3 rounded-2xl border-2 font-black text-xs bg-slate-900/80 backdrop-blur-xl z-10 transition-all ${
            density <= liquidDensity ? 'border-emerald-500/50 text-emerald-400 shadow-[0_0_20px_rgba(16,185,129,0.1)]' : 'border-rose-500/50 text-rose-400 shadow-[0_0_20px_rgba(244,63,94,0.1)]'
          }`}>
            <Zap className={`w-4 h-4 ${density <= liquidDensity ? 'animate-pulse text-emerald-400' : 'text-rose-400'}`} />
            <span>{density <= liquidDensity ? 'FLOTA' : 'SE HUNDE'}</span>
          </div>

          <div className="absolute bottom-8 right-8 flex flex-col gap-2 p-4 rounded-3xl bg-slate-900/60 border border-white/10 backdrop-blur-xl z-10">
            <div className="flex items-center gap-2 pb-2 border-b border-white/5">
                <Waves className="w-4 h-4 text-blue-400" />
                <span className="text-[10px] font-black uppercase text-slate-500">Fluido</span>
            </div>
            <div className="flex gap-2">
                {LIQUIDS.map(liq => (
                    <button 
                        key={liq.name}
                        onClick={() => setLiquidDensity(liq.d)}
                        className={`px-3 py-1.5 rounded-xl text-[9px] font-black transition-all border ${
                            liquidDensity === liq.d ? liq.color + ' text-white border-transparent' : 'bg-slate-800/50 text-slate-400 border-slate-700'
                        }`}
                    >
                        {liq.name}
                    </button>
                ))}
            </div>
          </div>
        </section>

        <aside className="w-full lg:w-[380px] bg-slate-900 border-l border-slate-800 flex flex-col shrink-0 overflow-y-auto">
          <div className="p-8 border-b border-slate-800 text-center shrink-0">
            <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2 flex items-center justify-center gap-2">
                <Gauge className="w-4 h-4" /> DENSIDAD
            </div>
            <div className="flex items-baseline justify-center gap-2">
              <span className={`text-6xl font-black font-mono tracking-tighter transition-colors ${density > liquidDensity ? 'text-rose-500' : 'text-emerald-500'}`}>
                {density.toFixed(2)}
              </span>
              <span className="text-slate-600 font-bold text-xs">g/cm³</span>
            </div>
          </div>

          <div className="p-6 space-y-8">
            <Controls mass={mass} volume={volume} onMassChange={setMass} onVolumeChange={setVolume} />
            <TutorPanel mass={mass} volume={volume} />
          </div>
        </aside>
      </main>
      <style>{`
        .no-scrollbar::-webkit-scrollbar { display: none; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 10px; }
      `}</style>
    </div>
  );
};

export default App;
