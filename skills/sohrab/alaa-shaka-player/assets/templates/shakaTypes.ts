/**
 * Structural typing seam for Shaka Player v5.2.3.
 *
 * Shaka ships `.d.ts` for every build variant, but `package.json` `"types"` resolves to the
 * NON-UI build (conflict C8, references/05-provenance-and-freshness.md). Rather than reach for
 * `any` - which /alaa-vue-typescript-clean-code ($alaa-vue-typescript-clean-code),
 * references/24-typescript-project-and-antipatterns.md forbids without an immediate typed
 * wrapper - declare only the members this application calls. The real Shaka objects satisfy
 * these shapes structurally, and a test can supply a small fake.
 *
 * Every member below exists at v5.2.3 (verified 2026-07-28). Nothing removed in v5.0 appears
 * here on purpose: `selectAudioLanguage`, `getAudioLanguagesAndRoles`, `setTextTrackVisibility`
 * and `isTextTrackVisible` are gone, and declaring them as optional members is what lets a
 * removed call compile and then silently do nothing.
 */

/** shaka.extern.Track - a variant. Only the fields a menu actually reads. */
export interface ShakaVariantTrack {
  readonly id: number;
  readonly active: boolean;
  readonly bandwidth: number;
  readonly language: string;
  readonly label: string | null;
  readonly height: number | null;
  readonly width: number | null;
  readonly frameRate: number | null;
  readonly roles: readonly string[];
  readonly channelsCount: number | null;
  readonly spatialAudio: boolean;
}

/** shaka.extern.AudioTrack. NOTE: there is no `id` field - key rows on language + role + label. */
export interface ShakaAudioTrack {
  readonly active: boolean;
  readonly language: string;
  readonly label: string | null;
  readonly roles: readonly string[];
  readonly channelsCount: number | null;
  readonly spatialAudio: boolean;
  readonly originalLanguage: string | null;
}

/** shaka.extern.TextTrack. */
export interface ShakaTextTrack {
  readonly id: number;
  readonly active: boolean;
  readonly language: string;
  readonly label: string | null;
  readonly kind: "caption" | "subtitle" | string;
  readonly forced: boolean;
  readonly roles: readonly string[];
}

/** shaka.extern.Stats. Many fields are NaN, never 0 - guard with Number.isFinite. */
export interface ShakaStats {
  readonly width: number; readonly height: number;
  readonly streamBandwidth: number; readonly estimatedBandwidth: number;
  readonly currentCodecs: string;
  readonly decodedFrames: number; readonly droppedFrames: number; readonly corruptedFrames: number;
  readonly completionPercent: number;
  readonly loadLatency: number;
  /** New in 5.2.0. Unset for audio-only. Prefer this over loadLatency for startup. */
  readonly timeToFirstFrame: number;
  readonly manifestTimeSeconds: number; readonly drmTimeSeconds: number; readonly licenseTime: number;
  readonly playTime: number; readonly pauseTime: number; readonly bufferingTime: number;
  readonly liveLatency: number; readonly maxSegmentDuration: number;
  readonly gapsJumped: number; readonly stallsDetected: number;
  readonly manifestSizeBytes: number; readonly bytesDownloaded: number;
  readonly nonFatalErrorCount: number;
  readonly manifestPeriodCount: number; readonly manifestGapCount: number;
  readonly switchHistory: readonly ShakaTrackChoice[];
  readonly stateHistory: readonly ShakaStateChange[];
}

/** timestamp is SECONDS since epoch, not milliseconds. */
export interface ShakaTrackChoice {
  readonly timestamp: number;
  readonly id: number;
  readonly type: "variant" | "text";
  readonly fromAdaptation: boolean;
  readonly bandwidth: number | null;
}

/** The LAST entry's `duration` keeps growing while the player is in that state. */
export interface ShakaStateChange {
  readonly timestamp: number;
  readonly state: "buffering" | "playing" | "paused" | "ended";
  readonly duration: number;
}

/** shaka.extern.Request. `uris` is an array: fallbacks are tried in order on retry. */
export interface ShakaRequest {
  uris: string[];
  method: string;
  headers: Record<string, string>;
  allowCrossSiteCredentials: boolean;
  /** 0-based. > 0 means this invocation is a retry. */
  readonly attempt: number;
}

export interface ShakaResponse {
  readonly uri: string;
  data: ArrayBuffer;
  readonly status: number;
  /** All keys are lowercased. May be unavailable cross-origin. */
  readonly headers: Record<string, string>;
}

/** shaka.util.Error. NOTE: this is NOT `instanceof Error` at runtime, by design. */
export interface ShakaError {
  severity: 1 | 2;
  readonly category: number;
  readonly code: number;
  /** Per-code shape. For BAD_HTTP_STATUS, data[1] is the HTTP status and data[4] the RequestType.
   *  For a network error this array CONTAINS THE FAILING URI - never log or render it. */
  readonly data: readonly unknown[];
  handled: boolean;
}

export interface ShakaNetworkingEngine {
  registerRequestFilter(
    filter: (type: number, request: ShakaRequest, context?: unknown) => Promise<void> | void
  ): void;
  registerResponseFilter(
    filter: (type: number, response: ShakaResponse, context?: unknown) => Promise<void> | void
  ): void;
  unregisterRequestFilter(filter: unknown): void;
  addEventListener(type: "retry", listener: (event: { error: ShakaError | null }) => void): void;
  removeEventListener(type: string, listener: (event: unknown) => void): void;
}

export interface ShakaPlayer {
  attach(mediaElement: HTMLMediaElement, initializeMediaSource?: boolean): Promise<void>;
  detach(keepAdManager?: boolean, isSwitchingContent?: boolean): Promise<void>;
  /** load() unloads any previous stream itself. Do not destroy the player to change source. */
  load(assetUri: string, startTime?: number | Date | null, mimeType?: string): Promise<void>;
  unload(initializeMediaSource?: boolean, keepAdManager?: boolean, isSwitchingContent?: boolean): Promise<void>;
  /** After this every method throws LOAD_INTERRUPTED (7000). The instance is dead. */
  destroy(): Promise<void>;

  configure(config: Record<string, unknown>): void;
  configure(path: string, value: unknown): void;
  getConfiguration(): Record<string, unknown>;
  resetConfiguration(): void;

  /** Required since v5.0 instead of setting video.currentTime during startup. */
  updateStartTime(startTime: number | Date): void;
  getLoadMode(): number;
  isLive(): boolean;
  isDynamic(): boolean;
  seekRange(): { start: number; end: number };
  goToLive(): void;
  getPlaybackRate(): number;
  trickPlay(rate: number, useTrickPlayTrack?: boolean): void;
  cancelTrickPlay(): void;

  getVariantTracks(): ShakaVariantTrack[];
  selectVariantTrack(track: ShakaVariantTrack, clearBuffer?: boolean, safeMargin?: number): void;
  getAudioTracks(): ShakaAudioTrack[];
  /** v5 replacement for the removed selectAudioLanguage(). */
  selectAudioTrack(track: ShakaAudioTrack, safeMargin?: number): void;
  getTextTracks(): ShakaTextTrack[];
  /** Selecting a text track also makes it visible. There is no visibility toggle in v5. */
  selectTextTrack(track: ShakaTextTrack): void;
  addTextTrackAsync(
    uri: string, language: string, kind: string,
    mimeType?: string, codec?: string, label?: string, forced?: boolean
  ): Promise<ShakaTextTrack>;

  getStats(): ShakaStats;
  getNetworkingEngine(): ShakaNetworkingEngine;
  retryStreaming(retryDelaySeconds?: number): boolean;

  addEventListener(type: string, listener: (event: never) => void): void;
  removeEventListener(type: string, listener: (event: never) => void): void;
}

export interface ShakaPlayerConstructor {
  new (
    mediaElement?: HTMLMediaElement | null,
    videoContainer?: HTMLElement | null
  ): ShakaPlayer;
  isBrowserSupported(): boolean;
  probeSupport(promptsOkay?: boolean): Promise<Record<string, unknown>>;
  readonly LoadMode: {
    readonly DESTROYED: 0; readonly NOT_LOADED: 1;
    readonly MEDIA_SOURCE: 2; readonly SRC_EQUALS: 3;
  };
}

export interface ShakaNamespace {
  readonly Player: ShakaPlayerConstructor;
  readonly polyfill: { installAll(): void };
  readonly net: {
    readonly NetworkingEngine: {
      readonly RequestType: {
        readonly MANIFEST: 0; readonly SEGMENT: 1; readonly LICENSE: 2; readonly APP: 3;
        readonly TIMING: 4; readonly SERVER_CERTIFICATE: 5; readonly KEY: 6; readonly ADS: 7;
      };
    };
  };
  readonly util: {
    readonly Error: {
      readonly Severity: { readonly RECOVERABLE: 1; readonly CRITICAL: 2 };
      readonly Code: Readonly<Record<string, number>>;
    };
  };
  readonly offline: {
    readonly Storage: {
      new (player?: ShakaPlayer): ShakaStorage;
      support(): Promise<{ basic: boolean; encrypted: Record<string, boolean> }>;
      deleteAll(): Promise<void>;
    };
  };
}

/** store() returns an abortable operation - await `.promise`, not the operation. */
export interface ShakaAbortableOperation<T> {
  readonly promise: Promise<T>;
  abort(): Promise<void>;
}

export interface ShakaStoredContent {
  /** null while the download is still in progress or incomplete. */
  readonly offlineUri: string | null;
  readonly originalManifestUri: string;
  readonly duration: number;
  readonly size: number;
  /** Milliseconds; Infinity when clear or never expiring. */
  readonly expiration: number;
  readonly appMetadata: Record<string, unknown>;
  /** There is no resume API. This flag is the only record that a store was interrupted. */
  readonly isIncomplete: boolean;
}

export interface ShakaStorage {
  configure(config: Record<string, unknown>): void;
  /** Storage has its OWN engine. Filters on the Player's engine do not apply to downloads. */
  getNetworkingEngine(): ShakaNetworkingEngine;
  store(
    uri: string, appMetadata?: Record<string, unknown>, mimeType?: string
  ): ShakaAbortableOperation<ShakaStoredContent>;
  list(): Promise<ShakaStoredContent[]>;
  remove(contentUri: string): Promise<void>;
  /** Call on application startup: cleans orphaned persistent DRM sessions. */
  removeEmeSessions(): Promise<boolean>;
  destroy(): Promise<void>;
}
