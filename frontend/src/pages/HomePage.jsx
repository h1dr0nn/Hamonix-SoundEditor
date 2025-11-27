import React, { useMemo, useState } from 'react';
import { DragDropArea } from '../components/DragDropArea';
import { FileListPanel } from '../components/FileListPanel';
import { FormatSelector } from '../components/FormatSelector';
import { OutputFolderChooser } from '../components/OutputFolderChooser';
import { ProgressIndicator } from '../components/ProgressIndicator';
import { ToastMessage } from '../components/ToastMessage';
import { useTheme } from '../hooks/useTheme';
import { designTokens } from '../utils/theme';

const mockFiles = [
  { name: 'Podcast_Mixdown.wav', format: 'WAV', duration: '03:45', status: 'Ready', size: '48 MB' },
  { name: 'Voice_Memo_12.m4a', format: 'M4A', duration: '01:10', status: 'Queued', size: '8 MB' },
  { name: 'Stem_Vocals.aiff', format: 'AIFF', duration: '04:22', status: 'Converted', size: '62 MB' },
];

const formatOptions = ['AAC', 'MP3', 'WAV', 'FLAC', 'AIFF', 'OGG'];

export function HomePage() {
  const { theme, toggleTheme } = useTheme();
  const [selectedFormat, setSelectedFormat] = useState('AAC');

  const sessionProgress = useMemo(() => ({ progress: 38, status: 'Preview' }), []);

  return (
    <div
      className="min-h-screen bg-gradient-to-br from-white/70 via-background to-white/30 px-4 py-10 text-slate-900 transition duration-smooth dark:from-[#101012] dark:via-[#141418] dark:to-[#0f0f12] dark:text-slate-100"
      style={{ fontFamily: designTokens.font }}
    >
      <div className="mx-auto flex max-w-6xl flex-col gap-6">
        <header className="flex flex-col gap-4 rounded-card border border-white/60 bg-white/60 p-5 shadow-soft backdrop-blur-[32px] transition duration-smooth dark:border-white/10 dark:bg-white/10">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">Sound Converter</p>
              <h1 className="text-2xl font-semibold text-slate-900 dark:text-white">Phase 2 · UI/UX Shell</h1>
              <p className="text-sm text-slate-600 dark:text-slate-300">iOS/macOS glassmorphism preview with light & dark mode.</p>
            </div>
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={toggleTheme}
                className="flex items-center gap-2 rounded-full border border-white/70 bg-white/70 px-4 py-2 text-xs font-semibold text-slate-800 shadow-md transition duration-smooth hover:-translate-y-[1px] hover:shadow-lg focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent dark:border-white/10 dark:bg-white/10 dark:text-slate-100"
              >
                <span className="h-2 w-2 rounded-full bg-accent" aria-hidden />
                {theme === 'dark' ? 'Switch to Light' : 'Switch to Dark'}
              </button>
              <span className="rounded-full bg-accent px-4 py-2 text-xs font-semibold text-white shadow-md">Sonoma style</span>
            </div>
          </div>
        </header>

        <div className="grid gap-6 lg:grid-cols-[280px,1fr]">
          <aside className="glass-surface relative overflow-hidden rounded-card border border-white/60 bg-white/60 p-5 shadow-soft transition duration-smooth dark:border-white/10 dark:bg-white/10">
            <div className="absolute inset-0 bg-gradient-to-b from-white/70 via-white/30 to-white/0 opacity-80 dark:from-white/10 dark:via-white/5 dark:to-transparent" />
            <div className="relative space-y-6">
              <div className="space-y-2">
                <p className="text-xs uppercase tracking-[0.18em] text-slate-500 dark:text-slate-400">Workspace</p>
                <h2 className="text-xl font-semibold text-slate-900 dark:text-white">Session overview</h2>
                <p className="text-sm text-slate-600 dark:text-slate-300">
                  Prepare files, pick formats, and preview progress. Backend wiring arrives in Phase 3.
                </p>
              </div>
              <div className="space-y-3 rounded-2xl border border-white/60 bg-white/60 p-4 shadow-inner dark:border-white/10 dark:bg-white/5">
                <div className="flex items-center justify-between text-sm font-semibold text-slate-800 dark:text-slate-100">
                  <span>Files</span>
                  <span>{mockFiles.length}</span>
                </div>
                <div className="flex items-center justify-between text-sm font-semibold text-slate-800 dark:text-slate-100">
                  <span>Format</span>
                  <span>{selectedFormat}</span>
                </div>
                <div className="flex items-center justify-between text-sm font-semibold text-slate-800 dark:text-slate-100">
                  <span>Status</span>
                  <span>{sessionProgress.status}</span>
                </div>
              </div>
              <div className="space-y-2 rounded-2xl border border-white/50 bg-white/50 p-4 shadow-sm dark:border-white/10 dark:bg-white/5">
                <p className="text-xs uppercase tracking-[0.15em] text-slate-500 dark:text-slate-400">Tips</p>
                <ul className="space-y-2 text-sm text-slate-700 dark:text-slate-200">
                  <li>• Drag files or use the Add button.</li>
                  <li>• Select an output format to preview states.</li>
                  <li>• Light/Dark adapts to macOS-style surfaces.</li>
                </ul>
              </div>
            </div>
          </aside>

          <main className="space-y-6">
            <section className="grid gap-4 rounded-card border border-white/60 bg-white/60 p-5 shadow-soft backdrop-blur-[32px] transition duration-smooth dark:border-white/10 dark:bg-white/10 lg:grid-cols-[1.15fr,0.85fr]">
              <DragDropArea />
              <div className="flex flex-col justify-between gap-6 rounded-card border border-white/60 bg-white/60 p-4 shadow-inner dark:border-white/10 dark:bg-white/5">
                <FormatSelector formats={formatOptions} selected={selectedFormat} onSelect={setSelectedFormat} />
                <OutputFolderChooser path="~/Music/Exports" onChoose={() => {}} />
              </div>
            </section>

            <section className="grid gap-4 rounded-card border border-white/60 bg-white/60 p-5 shadow-soft backdrop-blur-[32px] transition duration-smooth dark:border-white/10 dark:bg-white/10 lg:grid-cols-[1.1fr,0.9fr]">
              <FileListPanel files={mockFiles} />
              <div className="flex flex-col gap-4">
                <ProgressIndicator progress={sessionProgress.progress} status={sessionProgress.status} />
                <ToastMessage
                  title="Preview mode"
                  message="UI is ready for Phase 3 wiring. Animations and theming mirror macOS Sonoma."
                  tone="info"
                />
              </div>
            </section>
          </main>
        </div>
      </div>
    </div>
  );
}
