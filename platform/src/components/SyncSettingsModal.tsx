import React, { useState, useEffect, useRef } from 'react';
import { Cloud, CloudOff, RefreshCw, Check, Copy, AlertCircle, X, Eye, EyeOff } from 'lucide-react';
import {
  clearSyncConfig,
  getSyncConfig,
  syncWithGist,
  SyncResult,
} from '../utils/cloudSync';

interface SyncSettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSyncCompleted?: (result: SyncResult) => void;
}

export const SyncSettingsModal: React.FC<SyncSettingsModalProps> = ({
  isOpen,
  onClose,
  onSyncCompleted,
}) => {
  const [token, setToken] = useState('');
  const [gistId, setGistId] = useState('');
  const [showToken, setShowToken] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [lastSyncedAt, setLastSyncedAt] = useState<string | undefined>(undefined);
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [copiedId, setCopiedId] = useState(false);
  const isMountedRef = useRef(true);
  const copyTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    isMountedRef.current = true;
    return () => {
      isMountedRef.current = false;
      if (copyTimerRef.current) {
        clearTimeout(copyTimerRef.current);
        copyTimerRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    if (!isOpen) return;
    const cfg = getSyncConfig();
    if (cfg) {
      setToken(cfg.token);
      setGistId(cfg.gistId);
      setLastSyncedAt(cfg.lastSyncedAt);
    } else {
      setToken('');
      setGistId('');
      setLastSyncedAt(undefined);
    }
    setFeedback(null);
  }, [isOpen]);

  useEffect(() => {
    const el = dialogRef.current;
    if (!isOpen) {
      if (el?.open) el.close();
      return;
    }
    if (el && !el.open) {
      el.showModal();
    }
    return () => {
      if (el?.open) el.close();
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const handleConnectAndSync = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token.trim()) {
      setFeedback({ type: 'error', text: 'Ingresa tu GitHub Personal Access Token.' });
      return;
    }

    setIsSyncing(true);
    setFeedback(null);

    const trimmedToken = token.trim();
    const trimmedGistId = gistId.trim();

    const result = await syncWithGist({ token: trimmedToken, gistId: trimmedGistId });
    onSyncCompleted?.(result);

    if (!isMountedRef.current) return;
    setIsSyncing(false);

    if (result.status === 'created') {
      setGistId(result.gistId);
      setLastSyncedAt(result.lastSyncedAt);
      setFeedback({
        type: 'success',
        text: 'Gist privado creado y progreso subido. Copia el Gist ID de arriba para pegarlo en tu otra PC.',
      });
    } else if (result.status === 'synced') {
      setGistId(result.gistId);
      setLastSyncedAt(result.lastSyncedAt);
      setFeedback({
        type: 'success',
        text: 'Progreso sincronizado y combinado correctamente.',
      });
    } else if (result.status === 'error') {
      setFeedback({ type: 'error', text: result.message });
    }
  };

  const handleDisconnect = () => {
    if (isSyncing) return;
    clearSyncConfig();
    setToken('');
    setGistId('');
    setLastSyncedAt(undefined);
    setFeedback({
      type: 'success',
      text: 'Sincronización desconectada en este navegador (tu progreso local se mantiene intacto).',
    });
    onSyncCompleted?.({ status: 'unconfigured' });
  };

  const handleCopyGistId = async () => {
    if (!gistId.trim()) return;
    try {
      await navigator.clipboard.writeText(gistId.trim());
      if (!isMountedRef.current) return;
      setCopiedId(true);
      if (copyTimerRef.current) {
        clearTimeout(copyTimerRef.current);
      }
      copyTimerRef.current = setTimeout(() => {
        copyTimerRef.current = null;
        if (isMountedRef.current) {
          setCopiedId(false);
        }
      }, 2000);
    } catch {}
  };

  const isConnected = Boolean(getSyncConfig()?.gistId);

  return (
    <dialog
      ref={dialogRef}
      onCancel={(e) => {
        e.preventDefault();
        onClose();
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
      className="m-auto w-[calc(100%-2rem)] max-w-md bg-white rounded-2xl border border-ka-border shadow-xl p-0 overflow-hidden backdrop:bg-slate-900/50 backdrop:backdrop-blur-xs"
      aria-labelledby="sync-modal-title"
    >
      <div>
        <div className="flex items-center justify-between px-5 py-4 border-b border-ka-border bg-slate-50">
          <div className="flex items-center gap-2.5">
            <Cloud className="w-5 h-5 text-ka-blue" />
            <h2 id="sync-modal-title" className="text-base font-extrabold text-ka-text-primary">
              Sincronización en la Nube (GitHub Gist)
            </h2>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-200/60 transition-colors cursor-pointer"
            aria-label="Cerrar"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleConnectAndSync} className="p-5 space-y-4">
          <p className="text-xs text-ka-text-secondary leading-relaxed">
            Sincroniza automáticamente tu progreso entre tu PC de la U y tu casa usando un{' '}
            <strong>Gist privado</strong>. Los cambios de ambas máquinas se combinan por fecha
            competencia por competencia sin perder avances.
          </p>

          <div>
            <label
              htmlFor="sync-token-input"
              className="block text-xs font-bold text-ka-text-primary mb-1"
            >
              GitHub Token (permiso <code className="font-mono">Gists: Read &amp; write</code>)
            </label>
            <div className="relative">
              <input
                id="sync-token-input"
                type={showToken ? 'text' : 'password'}
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="github_pat_... o ghp_..."
                className="w-full pr-9 pl-3 py-2 text-xs font-mono border border-ka-border rounded-lg focus:outline-none focus:ring-2 focus:ring-ka-blue/30 focus:border-ka-blue"
                autoComplete="off"
              />
              <button
                type="button"
                onClick={() => setShowToken((v) => !v)}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 p-1 cursor-pointer"
                aria-label={showToken ? 'Ocultar token' : 'Mostrar token'}
              >
                {showToken ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
              </button>
            </div>
          </div>

          <div>
            <label
              htmlFor="sync-gist-id-input"
              className="block text-xs font-bold text-ka-text-primary mb-1"
            >
              Gist ID <span className="font-normal text-ka-text-secondary">(opcional en la 1.ª PC)</span>
            </label>
            <div className="flex gap-2">
              <input
                id="sync-gist-id-input"
                type="text"
                value={gistId}
                onChange={(e) => setGistId(e.target.value)}
                placeholder="Déjalo vacío para crear uno nuevo"
                className="flex-1 px-3 py-2 text-xs font-mono border border-ka-border rounded-lg focus:outline-none focus:ring-2 focus:ring-ka-blue/30 focus:border-ka-blue"
                autoComplete="off"
              />
              {gistId.trim() && (
                <button
                  type="button"
                  onClick={handleCopyGistId}
                  className="px-2.5 py-2 border border-ka-border rounded-lg text-xs font-bold text-ka-text-secondary hover:bg-slate-50 flex items-center gap-1 cursor-pointer shrink-0"
                  title="Copiar Gist ID"
                >
                  {copiedId ? (
                    <Check className="w-3.5 h-3.5 text-emerald-600" />
                  ) : (
                    <Copy className="w-3.5 h-3.5" />
                  )}
                </button>
              )}
            </div>
          </div>

          {lastSyncedAt && (
            <div className="text-[11px] text-ka-text-secondary">
              Última sincronización:{' '}
              <span className="font-semibold text-ka-text-primary">
                {new Date(lastSyncedAt).toLocaleString()}
              </span>
            </div>
          )}

          {feedback && (
            <div
              className={`p-3 rounded-lg text-xs flex items-start gap-2 ${
                feedback.type === 'success'
                  ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                  : 'bg-rose-50 text-rose-800 border border-rose-200'
              }`}
            >
              {feedback.type === 'success' ? (
                <Check className="w-4 h-4 shrink-0 mt-0.5 text-emerald-600" />
              ) : (
                <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-600" />
              )}
              <span className="break-words">{feedback.text}</span>
            </div>
          )}

          <div className="flex items-center justify-between gap-2 pt-2">
            {isConnected ? (
              <button
                type="button"
                disabled={isSyncing}
                onClick={handleDisconnect}
                className="px-3 py-2 text-xs font-bold text-rose-600 hover:bg-rose-50 rounded-lg transition-colors flex items-center gap-1.5 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <CloudOff className="w-3.5 h-3.5" />
                <span>Desconectar</span>
              </button>
            ) : (
              <span />
            )}

            <button
              type="submit"
              disabled={isSyncing}
              className="px-4 py-2 bg-ka-blue hover:bg-ka-blue-hover text-white text-xs font-bold rounded-lg shadow-xs transition-all flex items-center gap-2 cursor-pointer disabled:opacity-70"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? 'animate-spin' : ''}`} />
              <span>{isSyncing ? 'Sincronizando...' : 'Conectar y Sincronizar'}</span>
            </button>
          </div>
        </form>
      </div>
    </dialog>
  );
};
