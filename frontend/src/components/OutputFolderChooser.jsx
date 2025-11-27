import React from 'react';

export function OutputFolderChooser({ path, onChoose }) {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-slate-500 dark:text-slate-400">Destination</p>
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Output folder</h3>
        </div>
        <span className="rounded-full bg-emerald-500/15 px-3 py-1 text-[11px] font-semibold text-emerald-700 dark:bg-emerald-400/10 dark:text-emerald-100">
          Ready
        </span>
      </div>

      <div className="flex items-center gap-3 rounded-2xl border border-white/60 bg-white/60 px-4 py-3 shadow-sm transition duration-smooth hover:shadow-lg dark:border-white/10 dark:bg-white/10">
        <div className="flex flex-1 flex-col overflow-hidden">
          <p className="text-xs uppercase tracking-[0.15em] text-slate-500 dark:text-slate-400">Current path</p>
          <p className="truncate text-sm font-semibold text-slate-900 dark:text-slate-100">{path}</p>
        </div>
        <button
          type="button"
          onClick={onChoose}
          className="rounded-full bg-accent px-4 py-2 text-xs font-semibold text-white shadow-md transition duration-smooth hover:translate-y-[1px] hover:shadow-lg focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
        >
          Choose…
        </button>
      </div>
    </div>
  );
}
