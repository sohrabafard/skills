/**
 * Client-only Shaka Player core wrapper for Vue 3 + Quasar + Vite, against Shaka v5.2.3.
 *
 * Obeys /alaa-vue-typescript-clean-code ($alaa-vue-typescript-clean-code):
 * no `any`, one frozen return object, derived primitives only in reactivity.
 *
 * Properties this file exists to guarantee, each with its reference:
 *  - the Player is NEVER reactive                      references/11-vue-quasar-binding.md
 *  - ONE lifecycle handle, so two callers cannot both destroy it   references/10-...
 *  - a run token, so a fast source change cannot load into a dead player
 *  - validated, named config - no magic numbers        references/15-...
 *  - a resilience policy, because maxAttempts defaults to 2 and VOD failures are fatal
 *                                                      references/35-...
 *  - credentials enter ONLY through a filter reading a getter, so a retry refreshes
 *                                                      references/40-..., references/42-...
 *  - errors classified by code; nothing logs the error object   references/70-...
 */

import { onBeforeUnmount, onMounted, readonly, ref, watch, type Ref } from "vue";
import type { ShakaError, ShakaNamespace, ShakaPlayer, ShakaStats } from "./shakaTypes";

/** A read grant with a known expiry. The TTL contract is owned by the object-storage skills. */
export interface MediaGrant {
  readonly token: string;
  readonly expiresAtMs: number;
}

/** Stable error identity for i18n mapping. Never surface a raw Shaka code to a user. */
export type PlayerErrorKind =
  | "unsupported-browser"
  | "missing-video-element"
  | "secure-context-required"
  | "manifest-unavailable"
  | "drm-failed"
  | "playback-failed";

export interface PlayerError {
  readonly kind: PlayerErrorKind;
  /** The Shaka code, for logs and bug reports. Not for display. */
  readonly code: number | null;
}

/** Tuning knobs. Every field has a stated range and is validated at construction. */
export interface PlayerTuning {
  /** Seconds fetched ahead of the playhead. 5..120. */
  readonly bufferAheadSeconds: number;
  /** Seconds buffered before playback resumes. 0..30, and strictly < bufferAheadSeconds. */
  readonly resumeAtSeconds: number;
  /** Attempts per request. 1..10. Shaka's own default is 2. */
  readonly requestAttempts: number;
  /** Overall per-request timeout, ms. 5000..60000. */
  readonly requestTimeoutMs: number;
  /** Soft ABR height cap, px. 240..2160. */
  readonly maxAutoHeight: number;
  /** Ceiling on app-level streaming retries before giving up. 0..50. */
  readonly maxStreamingRetries: number;
}

export const DEFAULT_TUNING: PlayerTuning = Object.freeze({
  bufferAheadSeconds: 30,
  resumeAtSeconds: 2,
  requestAttempts: 6,
  requestTimeoutMs: 20_000,
  maxAutoHeight: 1080,
  maxStreamingRetries: 10
});

const RANGES: Readonly<Record<keyof PlayerTuning, readonly [number, number]>> = Object.freeze({
  bufferAheadSeconds: [5, 120],
  resumeAtSeconds: [0, 30],
  requestAttempts: [1, 10],
  requestTimeoutMs: [5_000, 60_000],
  maxAutoHeight: [240, 2160],
  maxStreamingRetries: [0, 50]
});

export interface UseShakaPlayerOptions {
  /** Manifest URL. A change reloads playback; null tears playback down. */
  readonly source: Ref<string | null>;
  /** Host-owned video element ref. */
  readonly videoEl: Ref<HTMLVideoElement | null>;
  /** Called on every request attempt. Returning a fresh grant is how a retry recovers a 401. */
  readonly getGrant?: () => Promise<MediaGrant>;
  readonly tuning?: Partial<PlayerTuning>;
  /** Receives QoE quantities on session end. Wire NAMES come from /alaa-services-contract. */
  readonly onSessionEnd?: (stats: ShakaStats) => void;
}

/** Validates tuning and builds the Shaka config. Throws on a value outside its stated range. */
export function buildPlayerConfig(input: Partial<PlayerTuning> = {}): Record<string, unknown> {
  const t: PlayerTuning = { ...DEFAULT_TUNING, ...input };

  for (const key of Object.keys(RANGES) as (keyof PlayerTuning)[]) {
    const [min, max] = RANGES[key];
    const value = t[key];
    if (!Number.isFinite(value) || value < min || value > max) {
      throw new RangeError(`PlayerTuning.${key} must be in [${min}, ${max}]; received ${value}`);
    }
  }
  if (t.resumeAtSeconds >= t.bufferAheadSeconds) {
    // Upstream: "rebufferingGoal should always be less than bufferingGoal".
    throw new RangeError("PlayerTuning.resumeAtSeconds must be less than bufferAheadSeconds");
  }

  const retry = {
    maxAttempts: t.requestAttempts,
    baseDelay: 500,
    backoffFactor: 2,
    fuzzFactor: 0.5,          // keep at 0.5: it exists to stop client stampedes
    timeout: t.requestTimeoutMs,
    stallTimeout: 5_000,
    connectionTimeout: 8_000
  };

  return {
    // v6-ready spelling. The individual preferred* scalars are removed in v6.0 and are
    // already absent from the shipped .d.ts.
    preferredAudio: [{ language: "fa" }, { language: "en" }],
    preferredText: [],
    preferredVideo: [{ hdrLevel: "AUTO" }],

    manifest: { retryParameters: { ...retry, maxAttempts: t.requestAttempts + 2 } },
    drm: { retryParameters: { ...retry, maxAttempts: Math.min(4, t.requestAttempts) } },

    streaming: {
      retryParameters: retry,
      bufferingGoal: t.bufferAheadSeconds,
      rebufferingGoal: t.resumeAtSeconds,
      bufferBehind: 30,
      ignoreTextStreamFailures: true,   // a broken subtitle must not kill playback
      allowMediaSourceRecoveries: true,
      // Branch on getLoadMode() at runtime, never on user-agent.
      preferNativeHls: false,
      useNativeHlsForFairPlay: true
    },

    // SOFT cap: the track stays in the list and hand-selectable.
    // Top-level `restrictions` is HARD and can fail playback with 4012.
    abr: { enabled: true, restrictions: { maxHeight: t.maxAutoHeight } }
  };
}

export function useShakaPlayer(options: UseShakaPlayerOptions) {
  const tuning: PlayerTuning = { ...DEFAULT_TUNING, ...options.tuning };
  const config = buildPlayerConfig(tuning);   // throws NOW if a value is out of range

  const loading = ref(false);
  const ready = ref(false);
  const buffering = ref(false);
  const error = ref<PlayerError | null>(null);

  // NOT reactive, by upstream instruction: Vue's reactive Proxy breaks Shaka at load time.
  let shaka: ShakaNamespace | null = null;
  let player: ShakaPlayer | null = null;
  let run = 0;
  let disposed = false;
  let streamingRetries = 0;
  const disposers: Array<() => void> = [];

  onMounted(() => { void loadSource(options.source.value); });
  watch(() => options.source.value, (next, prev) => {
    if (disposed || next === prev) return;
    void loadSource(next);
  });
  // Awaited: the component does not finish unmounting until teardown completes.
  onBeforeUnmount(async () => { await dispose(); });

  async function loadSource(uri: string | null): Promise<void> {
    const token = ++run;
    error.value = null;
    ready.value = false;
    if (!uri || disposed) { loading.value = false; return; }

    loading.value = true;
    try {
      if (!(await ensurePlayer(token))) return;
      if (!player || disposed || token !== run) return;
      streamingRetries = 0;
      await player.load(uri);
      if (disposed || token !== run) return;
      loading.value = false;
      ready.value = true;
    } catch (raw) {
      if (disposed || token !== run) return;
      loading.value = false;
      error.value = classify(raw);
    }
  }

  async function ensurePlayer(token: number): Promise<boolean> {
    if (player) return true;

    const video = options.videoEl.value;
    if (!video) { error.value = { kind: "missing-video-element", code: null }; return false; }

    // Dynamic import: nothing Shaka runs on the server. The package `main` is the NON-UI
    // build and there are no named ESM exports, so unwrap `.default`.
    const mod = (await import("shaka-player/dist/shaka-player.ui.js")) as { default?: unknown };
    if (disposed || token !== run) return false;
    shaka = (mod.default ?? mod) as ShakaNamespace;

    shaka.polyfill.installAll();                       // polyfills BEFORE the support check
    if (!shaka.Player.isBrowserSupported()) {
      error.value = { kind: "unsupported-browser", code: null };
      return false;
    }

    const next = new shaka.Player();                   // no arguments: the one-arg form is deprecated
    await next.attach(video);
    if (disposed || token !== run) { await next.destroy(); return false; }

    player = next;
    next.configure(config);
    installAuth(next);
    installResiliencePolicy(next);
    registerListeners(next);
    return true;
  }

  /** The ONLY place a credential enters the player. Reads a getter, so a refresh during a
   *  retry loop is visible to the very next attempt (filters run per attempt since v5.0). */
  function installAuth(p: ShakaPlayer): void {
    const getGrant = options.getGrant;
    if (!getGrant || !shaka) return;
    const T = shaka.net.NetworkingEngine.RequestType;
    p.getNetworkingEngine().registerRequestFilter(async (type, request) => {
      if (type !== T.SEGMENT && type !== T.MANIFEST && type !== T.LICENSE) return;
      const grant = await getGrant();
      request.headers["Authorization"] = `Bearer ${grant.token}`;
    });
  }

  /** Overriding streaming.failureCallback REPLACES Shaka's built-in live auto-retry,
   *  so the live branch below re-implements it. On VOD there is no built-in retry at all. */
  function installResiliencePolicy(p: ShakaPlayer): void {
    if (!shaka) return;
    const Code = shaka.util.Error.Code;
    const RECOVERABLE = shaka.util.Error.Severity.RECOVERABLE;
    const retryable = new Set<number>([
      Code.BAD_HTTP_STATUS, Code.HTTP_ERROR, Code.TIMEOUT, Code.SEGMENT_MISSING
    ]);

    p.configure("streaming.failureCallback", (raw: ShakaError) => {
      if (!retryable.has(raw.code)) return;                 // allow-list: unknown codes stay fatal
      if (navigator.onLine === false) return;               // Shaka's own 'online' listener resumes us
      if (streamingRetries >= tuning.maxStreamingRetries) return;

      streamingRetries += 1;
      raw.severity = RECOVERABLE;                           // this is what stops it being fatal
      const delaySeconds = Math.min(0.5 * Math.pow(2, streamingRetries), 30);
      if (!p.retryStreaming(delaySeconds)) {
        streamingRetries = tuning.maxStreamingRetries;      // exhausted; stop trying
      }
    });

    p.configure("drm.failureCallback", (raw: ShakaError) => {
      if (raw.code === Code.LICENSE_REQUEST_FAILED) {
        raw.handled = true;   // the request filter refreshes the grant on the next attempt
      }
    });
  }

  function registerListeners(p: ShakaPlayer): void {
    const on = <T,>(type: string, listener: (event: T) => void): void => {
      p.addEventListener(type, listener as (event: never) => void);
      disposers.push(() => p.removeEventListener(type, listener as (event: never) => void));
    };

    on<{ buffering: boolean }>("buffering", e => { buffering.value = e.buffering === true; });
    on<{ detail: ShakaError }>("error", e => { error.value = classify(e.detail); });
    on<unknown>("loaded", () => { streamingRetries = 0; });
    // 'unloading' is the last moment getStats() still holds this session's counters.
    on<unknown>("unloading", () => { options.onSessionEnd?.(p.getStats()); });
  }

  /** Maps a failure to a stable kind. Never logs the error object: for a network error
   *  `data` carries the failing URI and its query string. */
  function classify(raw: unknown): PlayerError {
    if (raw instanceof Error) return { kind: "playback-failed", code: null };  // a Shaka crash
    const e = raw as Partial<ShakaError>;
    const code = typeof e.code === "number" ? e.code : null;
    if (code === null) return { kind: "playback-failed", code: null };
    if (code === 4042) return { kind: "secure-context-required", code };       // NO_WEB_CRYPTO_API
    if (code >= 6000 && code < 7000) return { kind: "drm-failed", code };
    if (code >= 1000 && code < 2000) return { kind: "manifest-unavailable", code };
    if (code >= 4000 && code < 5000) return { kind: "manifest-unavailable", code };
    return { kind: "playback-failed", code };
  }

  /** The only teardown path. Timers and listeners first, then destroy(). */
  async function dispose(): Promise<void> {
    if (disposed) return;
    disposed = true;
    run += 1;
    loading.value = false;
    ready.value = false;
    while (disposers.length > 0) disposers.pop()?.();
    const current = player;
    player = null;
    await current?.destroy();
  }

  // ONE frozen handle. No inner init() returning a second API object.
  return Object.freeze({
    loading: readonly(loading),
    ready: readonly(ready),
    buffering: readonly(buffering),
    error: readonly(error),
    /** Read-only escape hatch for a module that needs stats. Returns null before load. */
    stats: (): ShakaStats | null => player?.getStats() ?? null,
    dispose
  });
}
