
import React, { useMemo } from 'react';

interface VisualizerProps {
  mass: number;
  volume: number;
  materialColor?: string;
  liquidDensity?: number;
}

const Visualizer: React.FC<VisualizerProps> = ({ mass, volume, materialColor, liquidDensity = 1.0 }) => {
  const density = mass / volume;
  const isFloating = density <= liquidDensity;
  
  // Tamaño escalado para visibilidad
  const size = Math.pow(volume, 0.45) * 10 + 20;
  const containerHeight = 600;
  const waterLevel = 250; 
  
  // Cálculo de posición Y
  let yPos: number;
  if (isFloating) {
    const immersedRatio = density / liquidDensity;
    // Flotando: parte fuera y parte dentro
    yPos = waterLevel - (size - (size * Math.max(0.1, immersedRatio)));
  } else {
    // Hundido: en el fondo
    yPos = containerHeight - size - 50;
  }

  const liquidColor = liquidDensity < 1 ? '#f59e0b' : liquidDensity > 1 ? '#d97706' : '#3b82f6';

  // Partículas estáticas calculadas una sola vez
  const particles = useMemo(() => {
    const count = Math.min(Math.floor(mass / 5), 100);
    return Array.from({ length: count }).map((_, i) => ({
      id: i,
      x: Math.random() * 0.8 + 0.1,
      y: Math.random() * 0.8 + 0.1,
    }));
  }, [mass]);

  return (
    <div className="w-full h-full rounded-3xl overflow-hidden relative bg-[#010409] border border-slate-800 shadow-2xl">
      <svg className="w-full h-full" viewBox="0 0 800 600" preserveAspectRatio="xMidYMid meet">
        {/* Fondo del Tanque */}
        <rect x="0" y="0" width="800" height="600" fill="#010409" />
        
        {/* Líquido */}
        <rect x="50" y={waterLevel} width="700" height={containerHeight - waterLevel - 50} fill={liquidColor} fillOpacity="0.2" rx="4" />
        <line x1="50" y1={waterLevel} x2="750" y2={waterLevel} stroke={liquidColor} strokeWidth="2" strokeDasharray="8,4" opacity="0.4" />

        {/* Objeto */}
        <g transform={`translate(${400 - size / 2}, ${yPos})`} style={{ transition: 'transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)' }}>
          <rect 
            width={size} 
            height={size} 
            rx="4" 
            className={`${materialColor || 'fill-slate-100'} stroke-2 ${isFloating ? 'stroke-emerald-400/50' : 'stroke-rose-500/50'}`} 
          />
          {particles.map((p) => (
            <circle 
              key={p.id} 
              cx={p.x * size} 
              cy={p.y * size} 
              r={1.5} 
              fill="rgba(0,0,0,0.3)" 
            />
          ))}
        </g>
        
        {/* Suelo del Tanque */}
        <rect x="50" y={550} width="700" height="10" fill="#1e293b" rx="2" />
      </svg>
    </div>
  );
};

export default Visualizer;
