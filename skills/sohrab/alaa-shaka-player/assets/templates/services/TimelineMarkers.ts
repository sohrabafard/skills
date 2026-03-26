import type { Marker } from '../types/player'

export type TimelineMarkersConfig = {
  getMarkers: () => Marker[]
  saveMarker: (marker: Marker) => Promise<void> | void
  deleteMarker: (markerId: string) => Promise<void> | void
  buildShareUrl: (timeSec: number) => string
}

export class TimelineMarkers {
  constructor(private config: TimelineMarkersConfig) {}

  list() {
    return this.config.getMarkers()
  }

  async add(marker: Marker) {
    await this.config.saveMarker(marker)
  }

  async remove(markerId: string) {
    await this.config.deleteMarker(markerId)
  }

  share(timeSec: number) {
    return this.config.buildShareUrl(timeSec)
  }
}
