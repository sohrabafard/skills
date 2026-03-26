export type AdsManagerConfig = {
  getAdManager: () => any
  clientSideContainer: HTMLElement
  serverSideContainer?: HTMLElement
  getAdTagUrl: () => string | null
  onAdEvent?: (name: string, payload?: any) => void
  onError?: (error: any) => void
  adTimeoutMs?: number
}

export class AdsManager {
  private adPlaying = false
  private watchdogTimer: number | null = null

  constructor(private config: AdsManagerConfig) {}

  isAdPlaying() {
    return this.adPlaying
  }

  requestAds() {
    const adTagUrl = this.config.getAdTagUrl()
    if (!adTagUrl) return

    const adManager = this.config.getAdManager()
    if (!adManager) {
      throw new Error('Shaka AdManager is not available.')
    }

    adManager.setContainers(
      this.config.clientSideContainer,
      this.config.serverSideContainer
    )

    const adsRequest: any = {
      adTagUrl,
    }

    this.startWatchdog()

    try {
      adManager.requestClientSideAds(adsRequest)
      this.config.onAdEvent?.('ads_requested', { adTagUrl })
    } catch (error) {
      this.stopWatchdog()
      this.config.onError?.(error)
    }
  }

  onAdStarted() {
    this.adPlaying = true
    this.stopWatchdog()
    this.config.onAdEvent?.('ad_started')
  }

  onAdEnded() {
    this.adPlaying = false
    this.config.onAdEvent?.('ad_ended')
  }

  onAdError(error: any) {
    this.adPlaying = false
    this.stopWatchdog()
    this.config.onError?.(error)
  }

  private startWatchdog() {
    this.stopWatchdog()

    const timeoutMs = this.config.adTimeoutMs ?? 12000
    this.watchdogTimer = window.setTimeout(() => {
      this.adPlaying = false
      this.config.onError?.({ code: 'AD_TIMEOUT' })
    }, timeoutMs)
  }

  private stopWatchdog() {
    if (this.watchdogTimer) {
      window.clearTimeout(this.watchdogTimer)
      this.watchdogTimer = null
    }
  }
}
