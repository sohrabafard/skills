export type MediaItem = {
  id: string
  title?: string
  manifestUri: string
  poster?: string
  headers?: Record<string, string>
  subtitles?: Array<{
    uri: string
    language: string
    label?: string
    mime?: string
  }>
}

export type QuizCue = {
  id: string
  timeSec: number
  type: 'single' | 'multi' | 'free'
  question: string
  options?: Array<{ id: string; text: string }>
  required?: boolean
  allowSkip?: boolean
  enforceOnSeek?: boolean
}

export type Marker = {
  id: string
  timeSec: number
  type: 'note' | 'comment' | 'bookmark'
  text?: string
  authorId?: string
  createdAt?: string
}

export type ScheduleItem = {
  id: string
  startAtIso: string
  endAtIso?: string
  media: MediaItem
  startOffsetSec?: number
}
