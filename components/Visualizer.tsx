
import React, { useMemo } from 'react';

interface VisualizerProps {
  mass: number;
  volume: number;
  materialColor?: string;
  liquidDensity?: number;
}

const PARTICLE_POOL = Array.from({ length: 500 }).map(() => ({
  x: Math.random(),
  y: Math.random(),
  r: 1 + Math.random() * 1.5,
}));

const Visualizer: React.FC<VisualizerProps> = ({ mass, volume, materialColor, liquidDensity = 1.0 }) => {
  const density = mass / volume;
  const isFloating = density <= liquidDensity;
  const size = Math.pow(volume, 0.45) * 10 + 20;
  const waterLevel = 250; 
  
  let yPos: number;
  if (isFloating) {
    const immersedRatio = density / liquidDensity;
    yPos = waterLevel - (size - (size * Math.max(0.1, immersedRatio)));
  } else {
    yPos = 550 - size;
  }

  const visibleParticles = useMemo(() => {
    return PARTICLE_POOL.slice(0, Math.min(Math.floor(mass / 2), 500));
  }, [mass]);

  const liquidColor = liquidDensity < 1 ? '#f59e0b' : liquidDensity > 1 ? '#d97706' : '#3b82f6';

  return (
    <div className="w-full h-full rounded-3xl overflow-hidden relative bg-[#020617] border border-slate-800">
      <svg className="w-full h-full" viewBox="0 0 800 600" preserveAspectRatio="xMidYMid meet">
        <rect x="80" y={waterLevel} width="640" height={600 - waterLevel} fill={liquidColor} fillOpacity="0.2" />
        <line x1="80" y1={waterLevel} x2="720" y2={waterLevel} stroke={liquidColor} strokeWidth="2" strokeDasharray="5,5" opacity="0.6" />

        <g transform={`translate(${400 - size / 2}, ${yPos})`} style={{ transition: 'transform 0.2s ease-out' }}>
          <rect width={size} height={size} rx="8" className={`${materialColor || 'fill-white'} stroke-[2px] ${density > liquidDensity ? 'stroke-rose-500' : 'stroke-emerald-400'}`} />
          {visibleParticles.map((p, i) => (
            <circle key={i} cx={p.x * size} cy={p.y * size} r={p.r} fill="rgba(0,0,0,0.2)" />
          ))}
        </g>
      </svg>
    </div>
  );
};

export default Visualizer;
