
import React, { useState, useEffect, useRef } from 'react';
import Visualizer from './components/Visualizer.tsx';
import Controls from './components/Controls.tsx';
import TutorPanel from './components/TutorPanel.tsx';
import { FlaskConical, Gauge, Zap, Info, Waves } from 'lucide-react';
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
  const [isReady, setIsReady] = useState(false);

  const density = mass / volume;
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    Streamlit.setFrameHeight();
    const readyTimer = setTimeout(() => {
        Streamlit.setComponentReady();
        setIsReady(true);
    }, 150);
    return () => clearTimeout(readyTimer);
  }, []);

  useEffect(() => {
    if (!isReady) return;
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
    }, 150);
    return () => { if (timerRef.current) clearTimeout(timerRef.current); };
  }, [mass, volume, liquidDensity, isReady, density]);

  const handleMaterialSelect = (material: typeof MATERIALS[0]) => {
    setSelectedMaterial(material);
    if (material.density !== null) {
      const targetVolume = 300;
      setVolume(targetVolume);
      setMass(Math.round(targetVolume * material.density));
    }
  };

  return (
    <div className="h-screen bg-slate-950 text-slate-100 flex flex-col overflow-hidden font-sans border-t border-slate-800">
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
              className={`px-3 py-1 rounded-full text-[10px] font-bold transition-all ${
                selectedMaterial.name === m.name ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400'
              }`}
            >
              {m.name}
            </button>
          ))}
        </div>
      </nav>

      <main className="flex-1 flex flex-col lg:flex-row overflow-hidden">
        <section className="flex-1 relative bg-slate-950 p-4 flex flex-col min-h-0 overflow-hidden">
          <Visualizer mass={mass} volume={volume} materialColor={selectedMaterial.color} liquidDensity={liquidDensity} />
          
          <div className={`absolute top-8 left-8 flex items-center gap-3 px-6 py-3 rounded-2xl border-2 font-black text-xs bg-slate-900/80 backdrop-blur-xl z-10 transition-all ${
            density <= liquidDensity ? 'border-emerald-500/50 text-emerald-400' : 'border-rose-500/50 text-rose-400'
          }`}>
            <Zap className="w-4 h-4" />
            <span>{density <= liquidDensity ? 'FLOTACIÓN POSITIVA' : 'FLOTACIÓN NEGATIVA'}</span>
          </div>

          <div className="absolute bottom-8 right-8 flex flex-col gap-2 p-4 rounded-3xl bg-slate-900/60 border border-white/10 backdrop-blur-xl z-10">
            <div className="flex items-center gap-2 pb-2 border-b border-white/5">
                <Waves className="w-4 h-4 text-blue-400" />
                <span className="text-[10px] font-black uppercase text-slate-500">Líquido</span>
            </div>
            <div className="flex gap-2">
                {LIQUIDS.map(liq => (
                    <button 
                        key={liq.name}
                        onClick={() => setLiquidDensity(liq.d)}
                        className={`px-4 py-2 rounded-xl text-[9px] font-black transition-all ${
                            liquidDensity === liq.d ? liq.color + ' text-white' : 'bg-slate-800/50 text-slate-400'
                        }`}
                    >
                        {liq.name}
                    </button>
                ))}
            </div>
          </div>
        </section>

        <aside className="w-full lg:w-[400px] bg-slate-900 border-l border-slate-800 flex flex-col shrink-0 overflow-y-auto">
          <div className="p-8 border-b border-slate-800 text-center shrink-0">
            <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Densidad</div>
            <div className="flex items-baseline justify-center gap-2">
              <span className={`text-7xl font-black font-mono tracking-tighter transition-colors ${density > liquidDensity ? 'text-rose-500' : 'text-emerald-500'}`}>
                {density.toFixed(2)}
              </span>
              <span className="text-slate-600 font-bold text-sm italic">g/cm³</span>
            </div>
          </div>

          <div className="p-8 space-y-10">
            <Controls mass={mass} volume={volume} onMassChange={setMass} onVolumeChange={setVolume} />
            <TutorPanel mass={mass} volume={volume} />
          </div>
        </aside>
      </main>
      <style>{`.no-scrollbar::-webkit-scrollbar { display: none; }`}</style>
    </div>
  );
};

export default App;
