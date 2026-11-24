import React, { useMemo, useState } from 'react';
import { Course, CourseMasteryRecord, CompetencyMastery } from '../types';
import {
  formatTimingSeconds,
  getActiveMisconceptions,
  getCompetencyRetrievability,
  getMasteryChallengeReadiness,
  getResolvedMisconceptions,
  isUnitStarted,
  TIER_COLORS,
} from '../utils/masteryStorage';
import {
  computeCalibrationMetrics,
  formatCooldownRemaining,
  getCooldownRemainingMs,
} from '../utils/fsrsEngine';
import {
  computeM22HypothesisSummary,
  exportM22EventsAsJson,
  loadM22Events,
} from '../utils/m22Telemetry';
import { MathText } from './MathText';

interface ProgressLogViewProps {
  course: Course;
  mastery: CourseMasteryRecord;
  onBackToCourse: () => void;
  onStartMasteryChallenge: () => void;
  onStartMisconceptionDrill: () => void;
  onStartColdTransferProbe?: () => void;
  now?: Date;
}

function formatRelativeDue(dueIso: string | undefined, now: Date): { label: string; isDue: boolean } {
  if (!dueIso) return { label: 'Sin programar', isDue: false };
  const dueMs = Date.parse(dueIso);
  if (!Number.isFinite(dueMs)) return { label: 'Sin programar', isDue: false };
  const diffMs = dueMs - now.getTime();
  const diffDays = diffMs / 86_400_000;
  if (diffMs <= 0) {
    const overdueDays = Math.abs(diffDays);
    if (overdueDays < 1) return { label: 'Vence hoy', isDue: true };
    return { label: `Vencido hace ${Math.round(overdueDays)}d`, isDue: true };
  }
  if (diffDays < 1) {
    const hours = Math.max(1, Math.round(diffMs / 3_600_000));
    return { label: `En ${hours}h`, isDue: false };
  }
  return { label: `En ${Math.round(diffDays)}d`, isDue: false };
}

export const ProgressLogView: React.FC<ProgressLogViewProps> = ({
  course,
  mastery,
  onBackToCourse,
  onStartMasteryChallenge,
  onStartMisconceptionDrill,
  onStartColdTransferProbe,
  now = new Date(),
}) => {
  const [ledgerTab, setLedgerTab] = useState<'active' | 'resolved'>('active');
  const [sortByUrgency, setSortByUrgency] = useState(true);

  const compNameById = useMemo(
    () => new Map(course.competencies.map((c) => [c.id, c.name])),
    [course.competencies]
  );

  const readiness = useMemo(
    () => getMasteryChallengeReadiness(course, mastery, now),
    [course, mastery, now]
  );

  const activeTraps = useMemo(() => getActiveMisconceptions(mastery), [mastery]);
  const resolvedTraps = useMemo(() => getResolvedMisconceptions(mastery), [mastery]);
  const calibration = useMemo(
    () => computeCalibrationMetrics(mastery.srs_telemetry),
    [mastery.srs_telemetry]
  );

  const m22Events = useMemo(() => loadM22Events(course.course_id), [course.course_id]);
  const m22Summary = useMemo(() => computeM22HypothesisSummary(m22Events), [m22Events]);
  const hasColdProbeQuestions = useMemo(
    () =>
      course.questions.some(
        (q) =>
          q.type === 'open_symbolic' ||
          q.type === 'fill_in_the_blank' ||
          (q.type === 'adversarial_break' && q.adversarial_break?.mode === 'counterexample')
      ),
    [course.questions]
  );

  const formatPct = (val: number | null) =>
    val === null ? '--' : `${Math.round(val * 100)}%`;
  const formatSignedPp = (val: number | null) =>
    val === null ? '--' : `${val >= 0 ? '+' : ''}${Math.round(val * 100)} pp`;

  const handleExportM22Json = () => {
    const json = exportM22EventsAsJson(course.course_id);
    const blob = new Blob([json], { type: 'application/json;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `m22_telemetry_${course.course_id}_${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const retentionRows = useMemo(() => {
    const rows = course.competencies.map((comp, idx) => {
      const m: CompetencyMastery | undefined = mastery.competencies?.[comp.id];
      const started = isUnitStarted(m);
      const hasFsrs = Boolean(m?.fsrs && m.fsrs.state !== 0 && m.fsrs.last_review);
      const r = hasFsrs ? getCompetencyRetrievability(m, now) : started ? 1 : null;
      const stability = m?.fsrs?.stability ?? 0;
      const dueInfo = formatRelativeDue(m?.fsrs?.due, now);
      const cooldownMs =
        m?.status === 'Proficient'
          ? getCooldownRemainingMs(m.last_tier_promotion_at || m.last_practiced, now)
          : 0;
      return {
        comp,
        idx,
        m,
        started,
        hasFsrs,
        r,
        stability,
        dueInfo,
        cooldownMs,
      };
    });

    if (!sortByUrgency) return rows;

    return rows.toSorted((a, b) => {
      if (a.started !== b.started) return a.started ? -1 : 1;
      const ra = a.r ?? 2;
      const rb = b.r ?? 2;
      if (ra !== rb) return ra - rb;
      return a.idx - b.idx;
    });
  }, [course.competencies, mastery.competencies, now, sortByUrgency]);

  const meanRetentionPct = useMemo(() => {
    const tracked = retentionRows.filter((row) => row.hasFsrs && row.r !== null);
    if (tracked.length === 0) return null;
    const sum = tracked.reduce((acc, row) => acc + (row.r ?? 0), 0);
    return Math.round((sum / tracked.length) * 100);
  }, [retentionRows]);

  // Chronological fluency points across all competency histories
  const fluencyPoints = useMemo(() => {
    const raw: Array<{ dateMs: number; label: string; avgSec: number; compName: string }> = [];
    for (const comp of course.competencies) {
      const hist = mastery.competencies?.[comp.id]?.history || [];
      for (const h of hist) {
        if (typeof h.avg_seconds_per_question === 'number' && h.avg_seconds_per_question > 0) {
          const ms = Date.parse(h.date);
          if (Number.isFinite(ms)) {
            raw.push({
              dateMs: ms,
              label: new Date(ms).toLocaleDateString(),
              avgSec: h.avg_seconds_per_question,
              compName: comp.name,
            });
          }
        }
      }
    }
    raw.sort((a, b) => a.dateMs - b.dateMs);
    return raw.slice(-30);
  }, [course.competencies, mastery.competencies]);

  const fluencyDeltaPct = useMemo(() => {
    if (fluencyPoints.length < 2) return null;
    const first = fluencyPoints[0].avgSec;
    const last = fluencyPoints[fluencyPoints.length - 1].avgSec;
    if (first <= 0) return null;
    return Math.round(((last - first) / first) * 100);
  }, [fluencyPoints]);

  const svgChart = useMemo(() => {
    if (fluencyPoints.length === 0) return null;
    const w = 560;
    const h = 160;
    const padX = 36;
    const padY = 20;
    const maxSec = Math.max(30, ...fluencyPoints.map((p) => p.avgSec));
    const minSec = 0;
    const innerW = w - padX * 2;
    const innerH = h - padY * 2;

    const coords = fluencyPoints.map((p, i) => {
      const x =
        fluencyPoints.length === 1
          ? padX + innerW / 2
          : padX + (i / (fluencyPoints.length - 1)) * innerW;
      const norm = (p.avgSec - minSec) / Math.max(1, maxSec - minSec);
      const y = padY + innerH - norm * innerH;
      return { x, y, ...p };
    });

    const polyline = coords.map((c) => `${c.x.toFixed(1)},${c.y.toFixed(1)}`).join(' ');
    return { w, h, padX, padY, maxSec, coords, polyline };
  }, [fluencyPoints]);

  const displayedTraps = ledgerTab === 'active' ? activeTraps : resolvedTraps;

  return (
    <div
      data-testid="progress-log-view"
      className="flex-1 min-w-0 w-full max-w-5xl mx-auto px-4 sm:px-6 pt-6 sm:pt-8 pb-20 space-y-6"
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-ka-border-subtle pb-4">
        <div className="min-w-0">
          <button
            type="button"
            onClick={onBackToCourse}
            className="text-xs font-bold text-ka-blue hover:text-ka-blue-hover flex items-center gap-1 mb-1 cursor-pointer"
          >
            <span>←</span>
            <span>Volver al curso</span>
          </button>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-ka-text-primary tracking-tight">
            Bitácora de Fluidez, Retención FSRS y Trampas
          </h1>
          <p className="text-xs sm:text-sm text-ka-text-secondary mt-0.5 truncate">
            <MathText text={course.title} inline />
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2 shrink-0">
          {readiness.startedCount > 0 && (
            <button
              type="button"
              data-testid="progress-log-mastery-challenge-btn"
              onClick={onStartMasteryChallenge}
              className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs sm:text-sm font-bold shadow-sm transition-colors cursor-pointer"
            >
              🧠 Mastery Challenge (6 preg.)
            </button>
          )}
          {activeTraps.length > 0 && (
            <button
              type="button"
              data-testid="progress-log-practice-traps-btn"
              onClick={onStartMisconceptionDrill}
              className="px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-700 text-white text-xs sm:text-sm font-bold shadow-sm transition-colors cursor-pointer"
            >
              🎯 Practicar mis Trampas ({activeTraps.length})
            </button>
          )}
        </div>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <div className="p-4 rounded-xl bg-white border border-ka-border-card shadow-sm">
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
            Retención Media R(t)
          </div>
          <div className="text-2xl font-extrabold text-slate-900 mt-1">
            {meanRetentionPct !== null ? `${meanRetentionPct}%` : '--'}
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">
            Modelo FSRS-5/6 (meta 90%)
          </div>
        </div>

        <div className="p-4 rounded-xl bg-white border border-ka-border-card shadow-sm">
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
            Repasos Vencidos / Listas 12h
          </div>
          <div className="text-2xl font-extrabold text-amber-700 mt-1">
            {readiness.decayDueCount} / {readiness.proficientEligibleCount}
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">
            Olvido activo / Listas para Mastered
          </div>
        </div>

        <div className="p-4 rounded-xl bg-white border border-ka-border-card shadow-sm">
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
            Trampas Activas / Superadas
          </div>
          <div className="text-2xl font-extrabold text-rose-700 mt-1">
            {activeTraps.length}{' '}
            <span className="text-emerald-700 text-lg font-bold">/ {resolvedTraps.length}</span>
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">
            Inmunidad al lograr racha ≥ 2
          </div>
        </div>

        <div className="p-4 rounded-xl bg-white border border-ka-border-card shadow-sm">
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
            Brier Score FSRS
          </div>
          <div className="text-2xl font-extrabold text-indigo-700 mt-1">
            {calibration.brierScore !== null ? calibration.brierScore.toFixed(3) : '--'}
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">
            {calibration.n} repasos espaciados (meta &lt; 0.20)
          </div>
        </div>
      </div>

      {/* Block 1: FSRS Retention Map R(t) */}
      <section className="bg-white rounded-xl border border-ka-border-card shadow-sm p-4 sm:p-6 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold text-ka-text-primary">
              1. Mapa de Retención R(t) por Unidad
            </h2>
            <p className="text-xs text-ka-text-secondary">
              Probabilidad estimada de evocación actual y estabilidad de memoria (en días).
            </p>
          </div>
          <button
            type="button"
            onClick={() => setSortByUrgency((v) => !v)}
            className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold border border-slate-200 cursor-pointer"
          >
            {sortByUrgency ? 'Orden: Menor R(t) primero' : 'Orden: Currículo del curso'}
          </button>
        </div>

        <div className="space-y-2.5 max-h-80 overflow-y-auto pr-1">
          {retentionRows.map(({ comp, idx, m, started, hasFsrs, r, stability, dueInfo, cooldownMs }) => {
            const pct = r !== null ? Math.round(r * 100) : null;
            const tier = m?.status || 'Not started';
            const barColor =
              pct === null
                ? 'bg-slate-200'
                : pct >= 85
                ? 'bg-emerald-500'
                : pct >= 50
                ? 'bg-amber-500'
                : 'bg-rose-500';
            return (
              <div
                key={comp.id}
                className="p-3 rounded-lg bg-slate-50 border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
              >
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2 text-xs">
                    <span className="font-bold text-slate-500">U{idx + 1}</span>
                    <span
                      className="px-1.5 py-0.5 rounded text-[10px] font-bold"
                      style={{
                        backgroundColor: TIER_COLORS[tier].bg,
                        color: TIER_COLORS[tier].text,
                        border: `1px solid ${TIER_COLORS[tier].border}`,
                      }}
                    >
                      {tier}
                    </span>
                    {m?.needs_review && m.review_reason === 'decay' && (
                      <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-300">
                        ⏳ Repaso sugerido
                      </span>
                    )}
                    {m?.needs_review && m.review_reason !== 'decay' && (
                      <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-800 border border-rose-300">
                        🩹 Error reciente
                      </span>
                    )}
                    {cooldownMs > 0 && (
                      <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-indigo-50 text-indigo-800 border border-indigo-200">
                        ⏱️ Faltan {formatCooldownRemaining(cooldownMs)} para Mastered
                      </span>
                    )}
                  </div>
                  <div className="text-sm font-bold text-slate-900 truncate mt-0.5">
                    <MathText text={comp.name} inline />
                  </div>
                </div>

                <div className="w-full sm:w-64 shrink-0 space-y-1">
                  <div className="flex items-center justify-between text-[11px] font-semibold">
                    <span className="text-slate-600">
                      {hasFsrs ? `S = ${stability.toFixed(1)}d • ${dueInfo.label}` : started ? 'Iniciada' : 'Sin iniciar'}
                    </span>
                    <span className="font-extrabold text-slate-800">
                      {pct !== null ? `${pct}%` : '--'}
                    </span>
                  </div>
                  <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className={`h-2 rounded-full ${barColor}`}
                      style={{ width: `${pct ?? 0}%` }}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Block 2: Fluency Latency Compression Curve */}
      <section className="bg-white rounded-xl border border-ka-border-card shadow-sm p-4 sm:p-6 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold text-ka-text-primary">
              2. Curva de Fluidez (Sistema 2 → Sistema 1)
            </h2>
            <p className="text-xs text-ka-text-secondary">
              Evolución de latencia media por reactivo a lo largo de tus últimas sesiones (la latencia nunca penaliza FSRS).
            </p>
          </div>
          {fluencyDeltaPct !== null && (
            <span
              className={`px-2.5 py-1 rounded-full text-xs font-extrabold border ${
                fluencyDeltaPct <= 0
                  ? 'bg-emerald-100 text-emerald-800 border-emerald-300'
                  : 'bg-slate-100 text-slate-700 border-slate-200'
              }`}
            >
              {fluencyDeltaPct <= 0
                ? `⚡ ${Math.abs(fluencyDeltaPct)}% más rápido`
                : `+${fluencyDeltaPct}% tiempo medio`}
            </span>
          )}
        </div>

        {svgChart ? (
          <div className="w-full overflow-x-auto">
            <svg
              viewBox={`0 0 ${svgChart.w} ${svgChart.h}`}
              className="w-full h-44 min-w-[320px] bg-slate-50 rounded-lg border border-slate-200"
              role="img"
              aria-label="Curva de compresión de latencia por sesión"
            >
              <line
                x1={svgChart.padX}
                y1={svgChart.padY}
                x2={svgChart.padX}
                y2={svgChart.h - svgChart.padY}
                stroke="#cbd5e1"
                strokeWidth="1"
              />
              <line
                x1={svgChart.padX}
                y1={svgChart.h - svgChart.padY}
                x2={svgChart.w - svgChart.padX}
                y2={svgChart.h - svgChart.padY}
                stroke="#cbd5e1"
                strokeWidth="1"
              />
              <text x={8} y={svgChart.padY + 4} fontSize="10" fill="#64748b">
                {svgChart.maxSec}s
              </text>
              <text x={14} y={svgChart.h - svgChart.padY} fontSize="10" fill="#64748b">
                0s
              </text>
              {svgChart.coords.length > 1 && (
                <polyline
                  fill="none"
                  stroke="#1865f2"
                  strokeWidth="2.5"
                  strokeLinejoin="round"
                  strokeLinecap="round"
                  points={svgChart.polyline}
                />
              )}
              {svgChart.coords.map((pt, i) => (
                <circle
                  key={`${pt.dateMs}-${i}`}
                  cx={pt.x}
                  cy={pt.y}
                  r="4"
                  fill="#1865f2"
                  stroke="#ffffff"
                  strokeWidth="1.5"
                >
                  <title>{`${pt.compName}: ${formatTimingSeconds(pt.avgSec)} (${pt.label})`}</title>
                </circle>
              ))}
            </svg>
          </div>
        ) : (
          <div className="p-6 rounded-lg bg-slate-50 border border-dashed border-slate-300 text-center text-xs text-slate-500">
            Completa al menos una sesión con telemetría de tiempo para visualizar tu curva de fluidez.
          </div>
        )}
      </section>

      {/* Block 3: Misconception Ledger */}
      <section
        data-testid="misconception-ledger-section"
        className="bg-white rounded-xl border border-ka-border-card shadow-sm p-4 sm:p-6 space-y-4"
      >
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-lg font-bold text-ka-text-primary">
              3. Cuaderno Personal de Trampas (Misconception Ledger)
            </h2>
            <p className="text-xs text-ka-text-secondary">
              Captura errores diagnósticos reales (D-XX-YY). Acertar 2 veces sin pistas ni errores previos en preguntas portadoras marca la trampa como superada.
            </p>
          </div>
          <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-lg border border-slate-200 self-start">
            <button
              type="button"
              onClick={() => setLedgerTab('active')}
              className={`px-3 py-1 rounded-md text-xs font-bold transition-colors cursor-pointer ${
                ledgerTab === 'active'
                  ? 'bg-white text-rose-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Activas ({activeTraps.length})
            </button>
            <button
              type="button"
              onClick={() => setLedgerTab('resolved')}
              className={`px-3 py-1 rounded-md text-xs font-bold transition-colors cursor-pointer ${
                ledgerTab === 'resolved'
                  ? 'bg-white text-emerald-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Superadas ({resolvedTraps.length})
            </button>
          </div>
        </div>

        {displayedTraps.length === 0 ? (
          <div className="p-6 rounded-lg bg-slate-50 border border-dashed border-slate-300 text-center text-xs text-slate-500">
            {ledgerTab === 'active'
              ? '¡Sin trampas activas registradas en este curso! Sigue practicando.'
              : 'Aún no has completado la racha de 2 aciertos autónomos para ninguna trampa.'}
          </div>
        ) : (
          <div className="space-y-2.5 max-h-80 overflow-y-auto pr-1">
            {displayedTraps.map((entry) => {
              const compName = compNameById.get(entry.competency_id) || entry.competency_id;
              const streakPct = Math.min(100, Math.round((entry.resolved_streak / 2) * 100));
              return (
                <div
                  key={entry.distractor_id}
                  className={`p-3.5 rounded-lg border text-xs space-y-2 ${
                    ledgerTab === 'active'
                      ? 'bg-rose-50/60 border-rose-200'
                      : 'bg-emerald-50/60 border-emerald-200'
                  }`}
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center gap-2 min-w-0">
                      <span className="px-2 py-0.5 rounded font-mono font-extrabold bg-slate-900 text-white text-[11px]">
                        {entry.distractor_id}
                      </span>
                      <span className="font-bold text-slate-800 truncate">
                        <MathText text={compName} inline />
                      </span>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <span className="px-2 py-0.5 rounded bg-white border border-slate-200 font-bold text-slate-700">
                        {entry.count} {entry.count === 1 ? 'caída' : 'caídas'}
                      </span>
                      <span className="px-2 py-0.5 rounded bg-white border border-slate-200 font-bold text-indigo-700">
                        Inmunidad: {Math.min(2, entry.resolved_streak)}/2
                      </span>
                    </div>
                  </div>
                  <div className="text-slate-800 leading-relaxed break-words [overflow-wrap:anywhere]">
                    <MathText text={entry.rationale} />
                  </div>
                  <div className="w-full h-1.5 bg-white/80 rounded-full overflow-hidden border border-slate-200">
                    <div
                      className={`h-1.5 ${
                        ledgerTab === 'active' ? 'bg-indigo-500' : 'bg-emerald-500'
                      }`}
                      style={{ width: `${streakPct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* Block 4: Empirical FSRS Calibration (Brier Score / Log-Loss) */}
      <section
        data-testid="fsrs-calibration-section"
        className="bg-white rounded-xl border border-ka-border-card shadow-sm p-4 sm:p-6 space-y-3"
      >
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold text-ka-text-primary">
              4. Calibración Empírica FSRS (Brier Score &amp; Log-Loss)
            </h2>
            <p className="text-xs text-ka-text-secondary">
              Evalúa qué tan bien predijo R(t) tus aciertos reales tras intervalos de días/semanas (ventana hasta 500 eventos).
            </p>
          </div>
          <span
            className={`px-2.5 py-1 rounded-full text-xs font-bold border ${
              calibration.isReliable
                ? calibration.brierScore !== null && calibration.brierScore < 0.2
                  ? 'bg-emerald-100 text-emerald-800 border-emerald-300'
                  : 'bg-amber-100 text-amber-900 border-amber-300'
                : 'bg-slate-100 text-slate-600 border-slate-200'
            }`}
          >
            {calibration.isReliable
              ? calibration.brierScore !== null && calibration.brierScore < 0.2
                ? '✓ Calibración Óptima (< 0.20)'
                : '⚠️ Revisar retención objetivo'
              : `Muestra en acumulación (${calibration.n}/20)`}
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
            <div className="text-slate-500 font-semibold">Brier Score</div>
            <div className="text-base font-extrabold text-slate-900 mt-0.5">
              {calibration.brierScore !== null ? calibration.brierScore.toFixed(4) : '--'}
            </div>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
            <div className="text-slate-500 font-semibold">Log-Loss</div>
            <div className="text-base font-extrabold text-slate-900 mt-0.5">
              {calibration.logLoss !== null ? calibration.logLoss.toFixed(4) : '--'}
            </div>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
            <div className="text-slate-500 font-semibold">R(t) Predicho Medio</div>
            <div className="text-base font-extrabold text-slate-900 mt-0.5">
              {calibration.meanPredictedR !== null
                ? `${Math.round(calibration.meanPredictedR * 100)}%`
                : '--'}
            </div>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
            <div className="text-slate-500 font-semibold">Acierto Real Observado</div>
            <div className="text-base font-extrabold text-slate-900 mt-0.5">
              {calibration.meanActual !== null
                ? `${Math.round(calibration.meanActual * 100)}%`
                : '--'}
            </div>
          </div>
        </div>
      </section>

      {/* Block 5: Telemetría M22 (Fase 0 · H1–H4) */}
      <section
        data-testid="m22-telemetry-card"
        className="bg-white rounded-xl border border-ka-border-card shadow-sm p-4 sm:p-5 space-y-3"
      >
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <h2 className="text-base sm:text-lg font-bold text-ka-text-primary">
                Telemetría M22 (Fase 0 · H1–H4)
              </h2>
              <span
                data-testid="m22-total-events-badge"
                className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-slate-100 text-slate-700 border border-slate-200"
              >
                {m22Summary.total_events} {m22Summary.total_events === 1 ? 'evento' : 'eventos'}
              </span>
            </div>
            <p className="text-xs text-ka-text-secondary">
              Diagnóstico empírico N=1 sin mutar FSRS ni niveles de maestría.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2 shrink-0">
            {onStartColdTransferProbe && (
              <button
                type="button"
                data-testid="progress-log-cold-transfer-probe-btn"
                disabled={!hasColdProbeQuestions}
                onClick={onStartColdTransferProbe}
                title={
                  hasColdProbeQuestions
                    ? 'Iniciar Sonda de Transferencia Fría (sin etiquetas ni pistas)'
                    : 'No hay preguntas elegibles para la Sonda Fría'
                }
                className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-900 disabled:bg-slate-200 disabled:text-slate-400 text-white text-xs font-bold shadow-sm transition-colors cursor-pointer disabled:cursor-not-allowed"
              >
                🧪 Sonda Fría (M22)
              </button>
            )}
            <button
              type="button"
              data-testid="export-m22-json-btn"
              onClick={handleExportM22Json}
              className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-800 border border-slate-300 text-xs font-bold transition-colors cursor-pointer"
            >
              ⬇️ Exportar JSON (M22)
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
          <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
            <div className="flex items-center justify-between gap-2">
              <span className="font-bold text-slate-800">H1 · Calibración de Nivel</span>
              <span className="font-mono font-extrabold text-indigo-700">
                {formatSignedPp(m22Summary.h1_tier_calibration.accuracy_gap)}
              </span>
            </div>
            <div className="text-[11px] text-slate-600 mt-1">
              Not started ({m22Summary.h1_tier_calibration.not_started.n}):{' '}
              {formatPct(m22Summary.h1_tier_calibration.not_started.first_attempt_accuracy)} ·
              Familiar+ ({m22Summary.h1_tier_calibration.familiar_plus.n}):{' '}
              {formatPct(m22Summary.h1_tier_calibration.familiar_plus.first_attempt_accuracy)}
            </div>
          </div>

          <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
            <div className="flex items-center justify-between gap-2">
              <span className="font-bold text-slate-800">H2 · Recurrencia de Trampa</span>
              <span className="font-mono font-extrabold text-rose-700">
                {formatPct(m22Summary.h2_trap_recurrence.recurrence_rate)}
              </span>
            </div>
            <div className="text-[11px] text-slate-600 mt-1">
              4-strikes: {m22Summary.h2_trap_recurrence.total_4_strike_events} · Repeticiones:{' '}
              {m22Summary.h2_trap_recurrence.recurrences}/
              {m22Summary.h2_trap_recurrence.followed_exposures}
            </div>
          </div>

          <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
            <div className="flex items-center justify-between gap-2">
              <span className="font-bold text-slate-800">H3 · Transferencia Sin Etiqueta</span>
              <span className="font-mono font-extrabold text-amber-700">
                {formatSignedPp(m22Summary.h3_unlabeled_transfer.accuracy_delta)}
              </span>
            </div>
            <div className="text-[11px] text-slate-600 mt-1">
              Etiquetada ({m22Summary.h3_unlabeled_transfer.labeled.n}):{' '}
              {formatPct(m22Summary.h3_unlabeled_transfer.labeled.first_attempt_accuracy)} ·
              Sonda ({m22Summary.h3_unlabeled_transfer.unlabeled_probe.n}):{' '}
              {formatPct(m22Summary.h3_unlabeled_transfer.unlabeled_probe.first_attempt_accuracy)}
            </div>
          </div>

          <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
            <div className="flex items-center justify-between gap-2">
              <span className="font-bold text-slate-800">H4 · Dependencia de Pistas</span>
              <span className="font-mono font-extrabold text-emerald-700">
                {formatPct(m22Summary.h4_hint_dependence.hint_assisted_share)}
              </span>
            </div>
            <div className="text-[11px] text-slate-600 mt-1">
              Sin pista ({m22Summary.h4_hint_dependence.proficient_mastered_cold.n}):{' '}
              {formatPct(m22Summary.h4_hint_dependence.proficient_mastered_cold.first_attempt_accuracy)}{' '}
              · Con pista ({m22Summary.h4_hint_dependence.proficient_mastered_hint_assisted.n}):{' '}
              {formatPct(
                m22Summary.h4_hint_dependence.proficient_mastered_hint_assisted.first_attempt_accuracy
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
