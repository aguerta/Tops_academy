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
  | 'challenge';

export interface NavigationState {
  viewMode: AppViewMode;
  courseId?: string;
  competencyId?: string;
  timestamp?: number;
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
    window.history.pushState(payload, '', window.location.href);
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
    window.history.replaceState(payload, '', window.location.href);
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

  // Asegurar que el estado inicial tenga viewMode: 'library'
  const currentState = options.getCurrentState();
  if (!window.history.state || !window.history.state.viewMode) {
    replaceNavState(currentState);
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

    // 3. Transición de vista según el estado recuperado
    if (previousState && previousState.viewMode) {
      options.onNavigate(previousState);
    } else {
      options.onNavigate({ viewMode: 'library' });
    }
  };

  window.addEventListener('popstate', handlePopState);

  return () => {
    window.removeEventListener('popstate', handlePopState);
  };
}
