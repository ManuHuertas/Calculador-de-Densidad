
import React, { useEffect, useState } from 'react';
import { getTutorExplanation } from '../services/gemini.ts';
import { TutorObservation } from '../types.ts';
import { BrainCircuit, Lightbulb } from 'lucide-react';

interface TutorPanelProps {
  mass: number;
  volume: number;
}

const TutorPanel: React.FC<TutorPanelProps> = ({ mass, volume }) => {
  const [observation, setObservation] = useState<TutorObservation | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const timer = setTimeout(async () => {
      setLoading(true);
      const res = await getTutorExplanation(mass, volume);
      setObservation(res);
      setLoading(false);
    }, 1500);
    return () => clearTimeout(timer);
  }, [mass, volume]);

  return (
    <div className="bg-slate-950/50 rounded-2xl p-4 border border-slate-800 space-y-3">
      <div className="flex items-center gap-2 text-[10px] font-black text-slate-500 uppercase tracking-widest">
        <BrainCircuit className="w-4 h-4 text-indigo-400" /> Tutor IA
        {loading && <span className="ml-2 w-1.5 h-1.5 rounded-full bg-indigo-500 animate-ping" />}
      </div>
      <p className="text-xs text-slate-400 leading-relaxed italic">
        {observation?.explanation || "Analizando el objeto..."}
      </p>
      {observation?.scientificFact && (
        <div className="pt-2 border-t border-slate-800 flex gap-2 items-start">
            <Lightbulb className="w-3 h-3 text-amber-500 mt-1 shrink-0" />
            <p className="text-[10px] text-slate-500 italic">{observation.scientificFact}</p>
        </div>
      )}
    </div>
  );
};

export default TutorPanel;
