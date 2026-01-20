
import React from 'react';
import { Weight, Box } from 'lucide-react';

interface ControlsProps {
  mass: number;
  volume: number;
  onMassChange: (val: number) => void;
  onVolumeChange: (val: number) => void;
}

const Controls: React.FC<ControlsProps> = ({ mass, volume, onMassChange, onVolumeChange }) => {
  return (
    <div className="space-y-8">
      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs font-bold text-slate-300">
          <div className="flex items-center gap-2"><Weight className="w-4 h-4 text-indigo-500" /> MASA</div>
          <span className="font-mono">{mass}g</span>
        </div>
        <input type="range" min="1" max="1000" value={mass} onChange={(e) => onMassChange(parseInt(e.target.value))} className="w-full h-1 bg-slate-800 rounded-full appearance-none cursor-pointer accent-indigo-500" />
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs font-bold text-slate-300">
          <div className="flex items-center gap-2"><Box className="w-4 h-4 text-emerald-500" /> VOLUMEN</div>
          <span className="font-mono">{volume}cm³</span>
        </div>
        <input type="range" min="10" max="1000" value={volume} onChange={(e) => onVolumeChange(parseInt(e.target.value))} className="w-full h-1 bg-slate-800 rounded-full appearance-none cursor-pointer accent-emerald-500" />
      </div>
    </div>
  );
};

export default Controls;
