import React from 'react';
import { designTokens } from '../utils/theme';

export function DragDropArea() {
  return (
    <div
      className="glass-surface relative flex flex-col items-center justify-center overflow-hidden rounded-card border border-white/60 bg-white/50 p-10 shadow-soft transition duration-smooth hover:-translate-y-[1px] hover:shadow-xl dark:border-white/10 dark:bg-white/10"
      style={{
        backdropFilter: `blur(${designTokens.blur})`,
        WebkitBackdropFilter: `blur(${designTokens.blur})`,
      }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-white/40 via-white/20 to-white/5 opacity-70 dark:from-white/5 dark:via-white/0 dark:to-white/5" />
      <div className="relative flex flex-col items-center gap-4 text-center">
        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-white/80 text-3xl shadow-inner backdrop-blur-[20px] dark:bg-white/10">
          <span role="img" aria-label="sparkles">
            ✨
          </span>
        </div>
        <div className="space-y-2">
          <p className="text-lg font-semibold text-slate-900 dark:text-slate-100">Drop your audio files</p>
          <p className="max-w-xs text-sm text-slate-600 dark:text-slate-300">
            Drag files from Finder or Explorer into this space. We will wire up conversion in the next phase.
          </p>
        </div>
        <div className="flex items-center gap-2 rounded-full bg-white/80 px-5 py-2 text-sm font-semibold text-slate-800 shadow-md dark:bg-white/10 dark:text-slate-100">
          <span className="h-2 w-2 rounded-full bg-accent" aria-hidden />
          Drag & Drop Placeholder
        </div>
      </div>
    </div>
  );
}
