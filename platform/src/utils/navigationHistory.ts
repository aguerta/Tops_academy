/**
 * Navigation History Manager for Top's Academy PWA.
 * Sincroniza la navegación interna de vistas (React) con el History API del navegador (popstate)
 * para permitir retroceso nativo fluido en Android e iOS, confirmaciones de abandono
 * y protección de salida accidental (doble atrás).
 */

export type AppViewMode =
  | 'library'
  | 'overview'
  | 'pre_exercise'
  | 'practice'
  | 'completed'
  | 'challenge'
  | 'progress_log';

export interface NavigationState {
  viewMode: AppViewMode;
  courseId?: string;
  competencyId?: string;
  sessionType?: string;
  timestamp?: number;
}

/**
 * Returns the normalized app base path without trailing slash (e.g. '' for '/', '/Tops_academy' for '/Tops_academy/').
 */
export function getBasePath(): string {
  const raw =
    (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.BASE_URL) || '/';
  if (raw === './' || raw === '/') return '';
  const withLeading = raw.startsWith('/') ? raw : `/${raw}`;
  return withLeading.endsWith('/') ? withLeading.slice(0, -1) : withLeading;
}

/**
 * Serializes a NavigationState into a clean subpage URL under the app base path.
 */
export function buildUrlFromState(state: NavigationState): string {
  const base = getBasePath();
  if (!state.courseId || state.viewMode === 'library') {
    return `${base}/`;
  }
  const cId = encodeURIComponent(state.courseId);
  if (state.viewMode === 'overview') {
    return `${base}/curso/${cId}`;
  }
  if (state.viewMode === 'progress_log') {
    return `${base}/curso/${cId}/bitacora`;
  }
  if (state.viewMode === 'challenge') {
    return `${base}/curso/${cId}/challenge`;
  }
  if (state.viewMode === 'pre_exercise' || state.viewMode === 'practice' || state.viewMode === 'completed') {
    if (state.competencyId && state.sessionType) {
      return `${base}/curso/${cId}/unidad/${encodeURIComponent(state.competencyId)}/${encodeURIComponent(state.sessionType)}`;
    }
    if (state.sessionType) {
      return `${base}/curso/${cId}/sesion/${encodeURIComponent(state.sessionType)}`;
    }
    return `${base}/curso/${cId}`;
  }
  return `${base}/`;
}

/**
 * Parses a browser pathname (relative to basePath) into a NavigationState.
 */
export function parseUrlToState(pathname?: string): NavigationState {
  const rawPath =
    pathname ?? (typeof window !== 'undefined' ? window.location.pathname : '/');
  const base = getBasePath();
  let rel = rawPath;
  if (base && rel.startsWith(base)) {
    rel = rel.slice(base.length);
  }
  const segments = rel
    .split('/')
    .filter(Boolean)
    .map((s) => {
      try {
        return decodeURIComponent(s);
      } catch {
        return s;
      }
    });

  if (segments[0] !== 'curso' || !segments[1]) {
    return { viewMode: 'library' };
  }

  const courseId = segments[1];
  const sub = segments[2];

  if (!sub) {
    return { viewMode: 'overview', courseId };
  }
  if (sub === 'bitacora') {
    return { viewMode: 'progress_log', courseId };
  }
  if (sub === 'challenge') {
    return { viewMode: 'challenge', courseId };
  }
  if (sub === 'unidad' && segments[3]) {
    return {
      viewMode: 'pre_exercise',
      courseId,
      competencyId: segments[3],
      sessionType: segments[4] || 'practice',
    };
  }
  if (sub === 'sesion' && segments[3]) {
    return {
      viewMode: 'pre_exercise',
      courseId,
      sessionType: segments[3],
    };
  }

  return { viewMode: 'overview', courseId };
}

type BackInterceptor = () => boolean; // Devuelve true si interceptó y manejó el retroceso

let interceptors: BackInterceptor[] = [];
let lastRootBackPress = 0;
const ROOT_EXIT_THRESHOLD_MS = 2000;

/**
 * Registra un interceptor de retroceso (ej. cerrar sidebar o diálogo de confirmación).
 * Se ejecutan en orden LIFO (el último registrado tiene mayor prioridad).
 */
export function registerBackInterceptor(interceptor: BackInterceptor): () => void {
  interceptors.unshift(interceptor);
  return () => {
    interceptors = interceptors.filter((fn) => fn !== interceptor);
  };
}

/**
 * Agrega un nuevo estado al historial del navegador.
 */
export function pushNavState(state: NavigationState): void {
  if (typeof window === 'undefined') return;
  const payload: NavigationState = { ...state, timestamp: Date.now() };
  try {
    const targetUrl = buildUrlFromState(payload);
    window.history.pushState(payload, '', targetUrl);
  } catch (err) {
    console.warn('[NavigationHistory] Failed to push state:', err);
  }
}

/**
 * Reemplaza el estado actual en el historial.
 */
export function replaceNavState(state: NavigationState): void {
  if (typeof window === 'undefined') return;
  const payload: NavigationState = { ...state, timestamp: Date.now() };
  try {
    const targetUrl = buildUrlFromState(payload);
    window.history.replaceState(payload, '', targetUrl);
  } catch (err) {
    console.warn('[NavigationHistory] Failed to replace state:', err);
  }
}

export interface SetupNavigationOptions {
  getCurrentState: () => NavigationState;
  onNavigate: (state: NavigationState) => void;
  onDoubleBackToast: () => void;
}

/**
 * Inicializa el listener del evento popstate del navegador.
 */
export function setupNavigationHistory(options: SetupNavigationOptions): () => void {
  if (typeof window === 'undefined') return () => {};

  // Asegurar que el estado inicial refleje la URL actual sin sobrescribir subrutas al recargar
  if (!window.history.state || !window.history.state.viewMode) {
    replaceNavState(parseUrlToState());
  }

  const handlePopState = (event: PopStateEvent) => {
    // 1. Ejecutar interceptores de alta prioridad (modales, sidebar, alertas)
    for (const interceptor of interceptors) {
      const handled = interceptor();
      if (handled) {
        // Re-empujar estado para que la pila del historial permanezca alineada
        const cur = options.getCurrentState();
        try {
          window.history.pushState(cur, '', window.location.href);
        } catch {}
        return;
      }
    }

    // 2. Si estamos en la raíz (library) y el usuario intenta retroceder fuera de la PWA
    const previousState = event.state as NavigationState | null;
    const currentView = options.getCurrentState().viewMode;

    if (currentView === 'library' && (!previousState || previousState.viewMode === 'library')) {
      const now = Date.now();
      if (now - lastRootBackPress < ROOT_EXIT_THRESHOLD_MS) {
        // Segundo intento en < 2s: permitir que el sistema operativo salga/minimice la app
        lastRootBackPress = 0;
        return;
      } else {
        // Primer intento: Mostrar Toast y retener dentro de la app
        lastRootBackPress = now;
        options.onDoubleBackToast();
        // Re-empujar estado 'library' para evitar salir de inmediato
        try {
          window.history.pushState({ viewMode: 'library' }, '', window.location.href);
        } catch {}
        return;
      }
    }

    // 3. REGLA INVIOLABLE: Desde 'overview', retroceder NUNCA debe ingresar a un quiz, test, modal o completed.
    // Permitir avanzar (Forward) a 'progress_log' o 'challenge' si el historial apunta a ellos.
    if (currentView === 'overview') {
      if (
        previousState &&
        (previousState.viewMode === 'progress_log' || previousState.viewMode === 'challenge')
      ) {
        options.onNavigate(previousState);
        return;
      }
      options.onNavigate({ viewMode: 'library' });
      replaceNavState({ viewMode: 'library' });
      return;
    }

    // 4. Desde 'completed' o 'progress_log', retroceder debe volver al curso ('overview').
    if (currentView === 'completed' || currentView === 'progress_log') {
      const cur = options.getCurrentState();
      options.onNavigate({ viewMode: 'overview', courseId: cur.courseId });
      replaceNavState({ viewMode: 'overview', courseId: cur.courseId });
      return;
    }

    // 5. Transición de vista según el estado recuperado con sanitización estricta
    if (previousState && previousState.viewMode) {
      // Salvaguarda: No permitir que ningún retroceso aterrice en un quiz, examen o challenge efímero previo
      if (
        previousState.viewMode === 'practice' ||
        previousState.viewMode === 'challenge' ||
        previousState.viewMode === 'completed'
      ) {
        const cur = options.getCurrentState();
        options.onNavigate({ viewMode: 'overview', courseId: cur.courseId });
        replaceNavState({ viewMode: 'overview', courseId: cur.courseId });
      } else {
        options.onNavigate(previousState);
      }
    } else {
      options.onNavigate({ viewMode: 'library' });
    }
  };

  window.addEventListener('popstate', handlePopState);

  return () => {
    window.removeEventListener('popstate', handlePopState);
  };
}
