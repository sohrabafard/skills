export type ShakaCoreConfig = {
  videoEl: HTMLVideoElement
  containerEl?: HTMLElement
  src: string
  startTime?: number
  autoplay?: boolean
  poster?: string
  extraHeaders?: Record<string, string>
  preferNativeHls?: boolean
  onUnsupported?: () => void
  onError?: (error: unknown) => void
  onTime?: (payload: { currentTime: number; duration: number }) => void
  onStats?: (stats: any) => void
}

export type ShakaCoreApi = {
  getPlayer: () => any
  load: (args: { src: string; startTime?: number }) => Promise<void>
  play: () => Promise<void>
  pause: () => void
  seek: (seconds: number) => void
  destroy: () => Promise<void>
}

type ShakaNamespace = any

export function useShakaCore() {
  let shaka: ShakaNamespace | null = null
  let player: any | null = null
  let videoEl: HTMLVideoElement | null = null
  let timeTimer: number | null = null
  let statsTimer: number | null = null
  const disposers: Array<() => void> = []

  async function ensureShakaLoaded(): Promise<ShakaNamespace> {
    if (shaka) return shaka

    if (typeof window === 'undefined') {
      throw new Error('Shaka must be initialized in the browser.')
    }

    const module: any = await import('shaka-player/dist/shaka-player.compiled.js')
    shaka = module.default ?? module
    return shaka
  }

  function clearTimers() {
    if (timeTimer) {
      window.clearInterval(timeTimer)
      timeTimer = null
    }

    if (statsTimer) {
      window.clearInterval(statsTimer)
      statsTimer = null
    }
  }

  async function init(config: ShakaCoreConfig): Promise<ShakaCoreApi> {
    const shakaLib = await ensureShakaLoaded()
    shakaLib.polyfill.installAll()

    if (!shakaLib.Player.isBrowserSupported()) {
      config.onUnsupported?.()
      throw new Error('The current browser is not supported by Shaka Player.')
    }

    videoEl = config.videoEl
    videoEl.autoplay = config.autoplay ?? false

    if (config.poster) {
      videoEl.poster = config.poster
    }

    player = new shakaLib.Player()
    await player.attach(videoEl)

    if (config.preferNativeHls) {
      player.configure({
        streaming: {
          preferNativeHls: true,
        },
      })
    }

    const networkingEngine = player.getNetworkingEngine?.()

    if (
      networkingEngine &&
      config.extraHeaders &&
      Object.keys(config.extraHeaders).length > 0
    ) {
      networkingEngine.registerRequestFilter((type: any, request: any) => {
        request.headers = request.headers || {}
        Object.assign(request.headers, config.extraHeaders)
      })
    }

    const onError = (event: any) => {
      config.onError?.(event?.detail ?? event)
    }

    player.addEventListener('error', onError)
    disposers.push(() => player?.removeEventListener('error', onError))

    timeTimer = window.setInterval(() => {
      if (!videoEl) return

      config.onTime?.({
        currentTime: videoEl.currentTime || 0,
        duration: videoEl.duration || 0,
      })
    }, 500)

    statsTimer = window.setInterval(() => {
      if (!player?.getStats) return
      config.onStats?.(player.getStats())
    }, 2000)

    await load({
      src: config.src,
      startTime: config.startTime ?? 0,
    })

    return {
      getPlayer: () => player,
      load,
      play: async () => {
        await videoEl?.play()
      },
      pause: () => {
        videoEl?.pause()
      },
      seek: (seconds: number) => {
        if (videoEl) {
          videoEl.currentTime = seconds
        }
      },
      destroy,
    }
  }

  async function load(args: { src: string; startTime?: number }) {
    if (!player) {
      throw new Error('Shaka has not been initialized yet.')
    }

    if (typeof args.startTime === 'number' && player.updateStartTime) {
      player.updateStartTime(args.startTime)
    }

    await player.load(args.src)
  }

  async function destroy() {
    clearTimers()

    for (const dispose of disposers.splice(0)) {
      try {
        dispose()
      } catch {
        // Ignore disposer failures during teardown
      }
    }

    if (player) {
      try {
        await player.destroy()
      } finally {
        player = null
      }
    }

    videoEl = null
    shaka = null
  }

  return {
    init,
    load,
    destroy,
  }
}
