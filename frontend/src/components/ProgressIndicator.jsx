import React from 'react';

export function ProgressIndicator({ progress = 0, status = 'Idle' }) {
  const safeProgress = Math.min(100, Math.max(0, progress));

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-slate-500 dark:text-slate-400">Activity</p>
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Progress</h3>
        </div>
        <span className="rounded-full bg-white/50 px-3 py-1 text-[11px] font-semibold text-slate-700 shadow-inner dark:bg-white/10 dark:text-slate-200">
          {status}
        </span>
      </div>

      <div className="space-y-2 rounded-2xl border border-white/60 bg-white/60 p-4 shadow-sm dark:border-white/10 dark:bg-white/10">
        <div className="flex items-center justify-between text-xs font-semibold text-slate-600 dark:text-slate-300">
          <span>Smoothing preview</span>
          <span>{safeProgress}%</span>
        </div>
        <div className="h-3 w-full overflow-hidden rounded-full bg-slate-200/70 dark:bg-white/10">
          <div
            className="h-full rounded-full bg-gradient-to-r from-accent/90 via-accent to-accent/80 shadow-[0_6px_20px_rgba(0,122,255,0.25)] transition-all duration-200 ease-out"
            style={{ width: `${safeProgress}%` }}
          />
        </div>
      </div>
    </div>
  );
}
