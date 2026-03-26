import type { ScheduleItem } from '../types/player'

export type PlaybackConductorConfig = {
  now: () => Date
  schedule: () => ScheduleItem[]
  load: (manifestUri: string, startOffsetSec: number) => Promise<void>
  onItemChange?: (item: ScheduleItem) => void
  tickIntervalMs?: number
}

export class PlaybackConductor {
  private timer: number | null = null
  private activeItemId: string | null = null

  constructor(private config: PlaybackConductorConfig) {}

  start() {
    if (this.timer) return

    this.timer = window.setInterval(() => {
      void this.tick()
    }, this.config.tickIntervalMs ?? 1000)

    void this.tick()
  }

  stop() {
    if (this.timer) {
      window.clearInterval(this.timer)
      this.timer = null
    }
  }

  private async tick() {
    const nowMs = this.config.now().getTime()

    const items = this.config
      .schedule()
      .map((item) => ({
        item,
        startMs: new Date(item.startAtIso).getTime(),
        endMs: item.endAtIso ? new Date(item.endAtIso).getTime() : Number.POSITIVE_INFINITY,
      }))
      .sort((a, b) => a.startMs - b.startMs)

    const active = items.find((entry) => nowMs >= entry.startMs && nowMs < entry.endMs)

    if (!active) return
    if (active.item.id === this.activeItemId) return

    this.activeItemId = active.item.id
    this.config.onItemChange?.(active.item)

    const baseOffset = active.item.startOffsetSec ?? 0
    const computedOffset = baseOffset + (nowMs - active.startMs) / 1000

    await this.config.load(active.item.media.manifestUri, Math.max(0, computedOffset))
  }
}
