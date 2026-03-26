# Quiz overlays during playback

## Goal

Show an interactive quiz at specific timestamps without making the playback
wrapper itself responsible for quiz UI or business rules.

## Recommended data model

```ts
type QuizCue = {
  id: string
  timeSec: number
  type: 'single' | 'multi' | 'free'
  question: string
  options?: Array<{ id: string; text: string }>
  required?: boolean
  allowSkip?: boolean
  enforceOnSeek?: boolean
}
```

## Behavior

When playback passes a cuepoint:

1. pause the content
2. open a dialog or overlay
3. capture the result
4. send analytics
5. resume playback according to product rules

## Seek policy

Define this explicitly:

- should a required quiz reappear if the user seeks past it?
- should an optional quiz appear only once?
- should resume be blocked if required input is missing?

Do not leave these questions implicit.
