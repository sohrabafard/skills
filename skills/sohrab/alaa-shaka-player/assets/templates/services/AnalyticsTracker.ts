export type AnalyticsHeartbeat = {
  contentId: string
  positionSec: number
  watchedDeltaSec: number
  playbackRate: number
  muted: boolean
  volume: number
  quality?: {
    width?: number
    height?: number
    bandwidthEstimate?: number
  }
  isAdPlaying: boolean
  timestampMs: number
}

export type AnalyticsTrackerConfig = {
  videoEl: HTMLVideoElement
  getStats?: () => any
  contentId: () => string
  isAdPlaying?: () => boolean
  ignoreHiddenTab?: boolean
  heartbeatIntervalSec?: number
  sendHeartbeat: (heartbeat: AnalyticsHeartbeat) => Promise<void> | void
  sendEvent?: (name: string, payload?: any) => void
}

export class AnalyticsTracker {
  private timer: number | null = null
  private lastTickMs = 0
  private accumulatedSec = 0

  constructor(private config: AnalyticsTrackerConfig) {}

  start() {
    if (this.timer) return

    this.lastTickMs = Date.now()
    this.timer = window.setInterval(() => this.tick(), 1000)
    this.bind()
  }

  stop() {
    if (this.timer) {
      window.clearInterval(this.timer)
      this.timer = null
    }

    this.unbind()
  }

  async flush() {
    if (this.accumulatedSec <= 0.1) return

    const videoEl = this.config.videoEl
    const stats = this.config.getStats?.()

    const heartbeat: AnalyticsHeartbeat = {
      contentId: this.config.contentId(),
      positionSec: videoEl.currentTime || 0,
      watchedDeltaSec: this.accumulatedSec,
      playbackRate: videoEl.playbackRate || 1,
      muted: videoEl.muted,
      volume: videoEl.volume,
      quality: stats
        ? {
            width: stats?.width,
            height: stats?.height,
            bandwidthEstimate: stats?.estimatedBandwidth,
          }
        : undefined,
      isAdPlaying: this.config.isAdPlaying?.() ?? false,
      timestampMs: Date.now(),
    }

    this.accumulatedSec = 0
    await this.config.sendHeartbeat(heartbeat)
  }

  private tick() {
    const now = Date.now()
    const deltaSec = (now - this.lastTickMs) / 1000
    this.lastTickMs = now

    if (this.isCountingWatchTime()) {
      this.accumulatedSec += deltaSec
    }

    const interval = this.config.heartbeatIntervalSec ?? 15
    if (this.accumulatedSec >= interval) {
      void this.flush()
    }
  }

  private isCountingWatchTime() {
    const videoEl = this.config.videoEl
    const isPlaying = !videoEl.paused && !videoEl.ended && videoEl.readyState >= 2
    const isBuffering = videoEl.readyState < 3
    const isAdPlaying = this.config.isAdPlaying?.() ?? false
    const isHidden = document.visibilityState === 'hidden'
    const ignoreHiddenTab = this.config.ignoreHiddenTab ?? true

    return isPlaying && !isBuffering && !isAdPlaying && (!ignoreHiddenTab || !isHidden)
  }

  private bind() {
    const videoEl = this.config.videoEl

    videoEl.addEventListener('play', this.onPlay)
    videoEl.addEventListener('pause', this.onPause)
    videoEl.addEventListener('seeked', this.onSeeked)
    videoEl.addEventListener('ratechange', this.onRateChange)
    videoEl.addEventListener('volumechange', this.onVolumeChange)
    document.addEventListener('visibilitychange', this.onVisibilityChange)
  }

  private unbind() {
    const videoEl = this.config.videoEl

    videoEl.removeEventListener('play', this.onPlay)
    videoEl.removeEventListener('pause', this.onPause)
    videoEl.removeEventListener('seeked', this.onSeeked)
    videoEl.removeEventListener('ratechange', this.onRateChange)
    videoEl.removeEventListener('volumechange', this.onVolumeChange)
    document.removeEventListener('visibilitychange', this.onVisibilityChange)
  }

  private onPlay = () => {
    this.config.sendEvent?.('play')
  }

  private onPause = () => {
    this.config.sendEvent?.('pause')
  }

  private onSeeked = () => {
    this.config.sendEvent?.('seeked', {
      currentTime: this.config.videoEl.currentTime || 0,
    })
  }

  private onRateChange = () => {
    this.config.sendEvent?.('ratechange', {
      playbackRate: this.config.videoEl.playbackRate || 1,
    })
  }

  private onVolumeChange = () => {
    this.config.sendEvent?.('volumechange', {
      muted: this.config.videoEl.muted,
      volume: this.config.videoEl.volume,
    })
  }

  private onVisibilityChange = () => {
    if (document.visibilityState === 'hidden') {
      void this.flush()
    }
  }
}
