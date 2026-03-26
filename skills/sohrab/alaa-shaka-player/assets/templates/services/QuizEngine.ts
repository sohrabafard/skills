import type { QuizCue } from '../types/player'

export type QuizEngineConfig = {
  videoEl: HTMLVideoElement
  cues: () => QuizCue[]
  showQuiz: (cue: QuizCue) => Promise<{ status: 'submitted' | 'skipped'; answer?: any }>
  sendEvent?: (name: string, payload?: any) => void
}

export class QuizEngine {
  private triggered = new Set<string>()
  private lastTimeSec = 0

  constructor(private config: QuizEngineConfig) {}

  start() {
    this.lastTimeSec = this.config.videoEl.currentTime || 0
    this.config.videoEl.addEventListener('timeupdate', this.onTimeUpdate)
    this.config.videoEl.addEventListener('seeked', this.onSeeked)
  }

  stop() {
    this.config.videoEl.removeEventListener('timeupdate', this.onTimeUpdate)
    this.config.videoEl.removeEventListener('seeked', this.onSeeked)
  }

  private onTimeUpdate = async () => {
    const currentTimeSec = this.config.videoEl.currentTime || 0
    const cues = this.config.cues()

    if (currentTimeSec < this.lastTimeSec) {
      this.lastTimeSec = currentTimeSec
      return
    }

    for (const cue of cues) {
      if (this.triggered.has(cue.id)) continue

      if (cue.timeSec > this.lastTimeSec && cue.timeSec <= currentTimeSec + 0.25) {
        await this.fireCue(cue)
      }
    }

    this.lastTimeSec = currentTimeSec
  }

  private onSeeked = () => {
    this.lastTimeSec = this.config.videoEl.currentTime || 0
  }

  private async fireCue(cue: QuizCue) {
    this.triggered.add(cue.id)
    this.config.videoEl.pause()

    this.config.sendEvent?.('quiz_open', {
      quizId: cue.id,
      timeSec: cue.timeSec,
    })

    try {
      const result = await this.config.showQuiz(cue)

      this.config.sendEvent?.('quiz_close', {
        quizId: cue.id,
        result,
      })
    } finally {
      await this.config.videoEl.play().catch(() => {})
    }
  }
}
