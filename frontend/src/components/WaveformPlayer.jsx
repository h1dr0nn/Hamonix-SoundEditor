import React, { useEffect, useRef, useState } from 'react';
import WaveSurfer from 'wavesurfer.js';
import { FiPlay, FiPause } from 'react-icons/fi';
import { readFile } from '@tauri-apps/plugin-fs';
import { cn } from '../utils/cn';

export function WaveformPlayer({ file, minimal = false }) {
  const containerRef = useRef(null);
  const wavesurfer = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!containerRef.current || !file) return;

    // Create WaveSurfer instance
    const ws = WaveSurfer.create({
      container: containerRef.current,
      waveColor: 'rgba(251, 146, 60, 0.4)', // Amber-400 with opacity
      progressColor: '#ea580c', // Orange-600 (Darker for contrast)
      cursorColor: '#ea580c', // Orange-600 (Visible cursor)
      cursorWidth: 2,
      barWidth: 2,
      barRadius: 2,
      barGap: 1,
      height: 32, // Compact height for embedded mode
      normalize: true,
      hideScrollbar: true,
      interact: true,
      fillParent: true,
      autoCenter: true,
    });

    wavesurfer.current = ws;
    let isDestroyed = false;

    // Load audio file
    const loadAudio = async () => {
      try {
        let url;
        if (file instanceof File) {
          url = URL.createObjectURL(file);
        } else if (file.path) {
          const content = await readFile(file.path);
          
          // Determine MIME type
          const ext = file.path.split('.').pop().toLowerCase();
          const mimeTypes = {
            'mp3': 'audio/mpeg',
            'wav': 'audio/wav',
            'aac': 'audio/aac',
            'm4a': 'audio/mp4',
            'flac': 'audio/flac',
            'ogg': 'audio/ogg'
          };
          const mimeType = mimeTypes[ext] || 'audio/mpeg';
          
          const blob = new Blob([content], { type: mimeType });
          url = URL.createObjectURL(blob);
        }

        if (isDestroyed) return;

        if (url) {
          console.log('[WaveformPlayer] Loading URL:', url);
          await ws.load(url);
        } else {
          console.warn('[WaveformPlayer] No URL generated for file:', file);
        }
      } catch (err) {
        if (!isDestroyed) {
          console.error('[WaveformPlayer] Error loading audio:', err);
        }
      }
    };

    loadAudio();

    // Events
    ws.on('ready', () => {
      if (isDestroyed) return;
      console.log('[WaveformPlayer] Ready');
      setIsReady(true);
      ws.play(); // Auto-play on load
      setIsPlaying(true);
    });

    ws.on('play', () => setIsPlaying(true));
    ws.on('pause', () => setIsPlaying(false));
    ws.on('finish', () => setIsPlaying(false));

    return () => {
      isDestroyed = true;
      try {
        ws.stop();
        ws.destroy();
      } catch (e) {
        console.warn('Error destroying wavesurfer:', e);
      }
      wavesurfer.current = null;
    };
  }, [file]);

  const togglePlayPause = (e) => {
    e.stopPropagation();
    if (wavesurfer.current) {
      wavesurfer.current.playPause();
    }
  };

  return (
    <div className="flex h-full w-full items-center gap-3">
      {/* Play/Pause Button */}
      <button
        onClick={togglePlayPause}
        className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent text-white shadow-sm transition-transform hover:scale-105 active:scale-95"
      >
        {isPlaying ? <FiPause className="h-3.5 w-3.5" /> : <FiPlay className="ml-0.5 h-3.5 w-3.5" />}
      </button>

      {/* Waveform Container */}
      <div 
        ref={containerRef} 
        className="relative flex-1 opacity-0 transition-opacity duration-500"
        style={{ opacity: isReady ? 1 : 0 }}
      />
    </div>
  );
}
