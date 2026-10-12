import React from 'react';

export const MasteryLegend: React.FC = () => {
  return (
    <div className="flex flex-wrap items-center gap-x-6 gap-y-2 py-4 text-xs text-ka-text-secondary border-b border-ka-border-subtle">
      {/* Mastered */}
      <div className="flex items-center gap-2">
        <div className="w-5 h-5 rounded bg-ka-mastered flex items-center justify-center text-white text-[10px]">
          👑
        </div>
        <span className="font-medium text-ka-text-primary">Mastered</span>
      </div>

      {/* Proficient */}
      <div className="flex items-center gap-2">
        <div className="w-5 h-5 rounded bg-ka-proficient flex items-center justify-center text-white text-[10px]">
          👑
        </div>
        <span className="font-medium text-ka-text-primary">Proficient</span>
      </div>

      {/* Familiar */}
      <div className="flex items-center gap-2">
        <div className="w-5 h-5 rounded bg-ka-familiar flex items-center justify-center text-white text-[10px]">
          👑
        </div>
        <span className="font-medium text-ka-text-primary">Familiar</span>
      </div>

      {/* Attempted */}
      <div className="flex items-center gap-2">
        <div className="w-5 h-5 rounded bg-white border-2 border-ka-attempted flex items-center justify-center text-ka-attempted text-[10px]" />
        <span className="font-medium text-ka-text-primary">Attempted</span>
      </div>

      {/* Not started */}
      <div className="flex items-center gap-2">
        <div className="w-5 h-5 rounded bg-white border-2 border-ka-not-started flex items-center justify-center text-ka-not-started text-[10px]" />
        <span className="font-medium text-ka-text-primary">Not started</span>
      </div>

      {/* Quiz */}
      <div className="flex items-center gap-2">
        <div className="w-5 h-5 rounded bg-slate-200 flex items-center justify-center text-slate-700 text-xs font-bold">
          ⚡
        </div>
        <span className="font-medium text-ka-text-primary">Quiz</span>
      </div>

      {/* Unit test */}
      <div className="flex items-center gap-2">
        <div className="w-5 h-5 rounded bg-slate-200 flex items-center justify-center text-slate-700 text-xs font-bold">
          ★
        </div>
        <span className="font-medium text-ka-text-primary">Unit test</span>
      </div>
    </div>
  );
};
