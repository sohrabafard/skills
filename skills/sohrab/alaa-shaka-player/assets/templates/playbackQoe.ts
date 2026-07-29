/**
 * Playback QoE quantities, against Shaka v5.2.3.
 *
 * THIS FILE DEFINES NO WIRE NAME. Every field below is a local identifier. The event names,
 * field names, metric names and the idempotency key's name are requested from
 * /alaa-services-contract ($alaa-services-contract), references/24-metric-registry.md.
 * Requirement levels are /alaa-observability-soc ($alaa-observability-soc).
 *
 * Two WA pipeline facts bound every count derived from these records
 * (references/60-analytics-and-getstats.md):
 *  - sinks retry 20x against a plain MergeTree with block deduplication off, so count() is an
 *    UPPER bound - which is why every record carries an idempotency key;
 *  - Vector's disk buffer sits on an emptyDir with one replica, so buffered records are lost on
 *    pod replacement after clients were told 202, making count() also a LOWER bound.
 * No figure derived from these records may be reported as exact.
 */

import type { ShakaPlayer, ShakaStats } from "./shakaTypes";

/** NaN-safe read. Many Shaka stats are NaN, never 0; shipping NaN as 0 silently corrupts averages. */
const num = (value: number): number | null => (Number.isFinite(value) ? value : null);

/** One session's quantities. Names here are LOCAL; map them to contract names at the edge. */
export interface PlaybackQuantities {
  readonly idempotencyKey: string;
  // startup
  readonly loadLatencySeconds: number | null;
  readonly timeToFirstFrameSeconds: number | null;   // 5.2.0+; unset for audio-only
  readonly manifestTimeSeconds: number | null;
  readonly drmTimeSeconds: number | null;
  readonly licenseTimeSeconds: number | null;
  // watch time - playTime, never a wall-clock delta
  readonly watchTimeSeconds: number;
  readonly pauseTimeSeconds: number | null;
  readonly bufferingTimeSeconds: number;
  readonly rebufferRatio: number | null;
  readonly rebufferEventCount: number;
  // quality
  readonly widthPixels: number | null;
  readonly heightPixels: number | null;
  readonly currentCodecs: string;
  readonly streamBandwidthBps: number | null;        // incorporates playbackRate
  readonly estimatedBandwidthBps: number | null;
  readonly decodedFrameCount: number | null;
  readonly droppedFrameCount: number | null;
  readonly corruptedFrameCount: number | null;
  readonly abrSwitchCount: number;
  readonly userSwitchCount: number;
  // resilience
  readonly gapsJumpedCount: number | null;
  readonly stallsDetectedCount: number | null;
  readonly nonFatalErrorCount: number | null;
  readonly downloadFailures: readonly DownloadFailure[];
  // delivery
  readonly bytesDownloaded: number | null;
  readonly maxSegmentDurationSeconds: number | null;
  // live / VOD - each is NaN on the other kind
  readonly liveLatencySeconds: number | null;
  readonly completionPercent: number | null;
}

/** requestType and status only. `request.uris` is a presigned credential and never leaves here. */
export interface DownloadFailure {
  readonly requestType: number;
  readonly httpStatus: number | null;
  readonly aborted: boolean;
  readonly shakaCode: number | null;
}

interface CollectorEvents {
  buffering: { buffering: boolean };
  downloadfailed: {
    requestType: number; httpResponseCode?: number; aborted?: boolean; error?: { code?: number };
  };
}

export interface QoeCollector {
  snapshot(): PlaybackQuantities | null;
  dispose(): void;
}

/**
 * Subscribes to the player's read-only event surface and derives QoE quantities.
 * It cannot change playback: it holds no writable handle.
 */
export function createQoeCollector(player: ShakaPlayer): QoeCollector {
  const idempotencyKey = crypto.randomUUID();
  let rebufferEvents = 0;
  let rebufferStartedAt: number | null = null;
  let abrSwitches = 0;
  let userSwitches = 0;
  const downloadFailures: DownloadFailure[] = [];
  const disposers: Array<() => void> = [];

  const on = <K extends keyof CollectorEvents>(
    type: K, listener: (event: CollectorEvents[K]) => void
  ): void => {
    player.addEventListener(type, listener as (event: never) => void);
    disposers.push(() => player.removeEventListener(type, listener as (event: never) => void));
  };
  const onBare = (type: string, listener: () => void): void => {
    player.addEventListener(type, listener as (event: never) => void);
    disposers.push(() => player.removeEventListener(type, listener as (event: never) => void));
  };

  on("buffering", event => {
    if (event.buffering) { rebufferStartedAt = performance.now(); rebufferEvents += 1; return; }
    if (rebufferStartedAt !== null) { rebufferStartedAt = null; }
  });

  // `adaptation` is automatic; `variantchanged` is app-initiated. Mixing them corrupts any
  // quality-distribution metric, which is why they are counted separately.
  onBare("adaptation", () => { abrSwitches += 1; });
  onBare("variantchanged", () => { userSwitches += 1; });

  on("downloadfailed", event => {
    downloadFailures.push({
      requestType: event.requestType,
      httpStatus: typeof event.httpResponseCode === "number" ? event.httpResponseCode : null,
      aborted: event.aborted === true,
      shakaCode: typeof event.error?.code === "number" ? event.error.code : null
    });
  });

  function snapshot(): PlaybackQuantities | null {
    let stats: ShakaStats;
    try { stats = player.getStats(); } catch { return null; }

    const watchTimeSeconds = num(stats.playTime) ?? 0;
    const bufferingTimeSeconds = num(stats.bufferingTime) ?? 0;
    const denominator = watchTimeSeconds + bufferingTimeSeconds;

    return Object.freeze({
      idempotencyKey,
      loadLatencySeconds: num(stats.loadLatency),
      timeToFirstFrameSeconds: num(stats.timeToFirstFrame),
      manifestTimeSeconds: num(stats.manifestTimeSeconds),
      drmTimeSeconds: num(stats.drmTimeSeconds),
      licenseTimeSeconds: num(stats.licenseTime),
      watchTimeSeconds,
      pauseTimeSeconds: num(stats.pauseTime),
      bufferingTimeSeconds,
      rebufferRatio: denominator > 0 ? bufferingTimeSeconds / denominator : null,
      rebufferEventCount: rebufferEvents,
      widthPixels: num(stats.width),
      heightPixels: num(stats.height),
      currentCodecs: stats.currentCodecs,
      streamBandwidthBps: num(stats.streamBandwidth),
      estimatedBandwidthBps: num(stats.estimatedBandwidth),
      decodedFrameCount: num(stats.decodedFrames),
      droppedFrameCount: num(stats.droppedFrames),
      corruptedFrameCount: num(stats.corruptedFrames),
      abrSwitchCount: abrSwitches,
      userSwitchCount: userSwitches,
      gapsJumpedCount: num(stats.gapsJumped),
      stallsDetectedCount: num(stats.stallsDetected),
      nonFatalErrorCount: num(stats.nonFatalErrorCount),
      downloadFailures: [...downloadFailures],
      bytesDownloaded: num(stats.bytesDownloaded),
      maxSegmentDurationSeconds: num(stats.maxSegmentDuration),
      liveLatencySeconds: num(stats.liveLatency),
      completionPercent: num(stats.completionPercent)
    });
  }

  return Object.freeze({
    snapshot,
    dispose(): void { while (disposers.length > 0) disposers.pop()?.(); }
  });
}

/**
 * Buffer-and-retry delivery. The accumulator is cleared only AFTER the send resolves -
 * clearing before the await loses the interval permanently on a single rejection.
 * The endpoint and the payload's field names come from /alaa-services-contract.
 */
export function createQoeSink(
  send: (records: readonly PlaybackQuantities[]) => Promise<void>,
  maxBuffered = 50
): { enqueue(record: PlaybackQuantities): void; flush(): Promise<void> } {
  let pending: PlaybackQuantities[] = [];
  let inFlight = false;

  return {
    enqueue(record: PlaybackQuantities): void {
      pending.push(record);
      // Bounded: drop the OLDEST, so the most recent session is the one that survives.
      if (pending.length > maxBuffered) pending = pending.slice(pending.length - maxBuffered);
    },
    async flush(): Promise<void> {
      if (inFlight || pending.length === 0) return;
      inFlight = true;
      const batch = [...pending];
      try {
        await send(batch);
        // Only now is it safe to drop them.
        pending = pending.slice(batch.length);
      } catch {
        // Keep the batch. Every record carries an idempotency key, so a duplicate send
        // is deduplicable downstream even though the sink itself cannot dedupe.
      } finally {
        inFlight = false;
      }
    }
  };
}
