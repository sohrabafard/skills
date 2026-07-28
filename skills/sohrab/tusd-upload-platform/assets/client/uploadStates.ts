/**
 * The one canonical upload-state list for this skill.
 *
 * Every other file - the composable, the queue store, the UI, telemetry -
 * imports from here. Adding a state means editing this file only, and every
 * consumer then sees the addition as a type error instead of a silent gap.
 *
 * This skill owns this list because the states are protocol and lifecycle
 * facts. It does not own how a component or a store is shaped around them.
 */
export const UPLOAD_STATES = [
  /** Nothing selected yet. */
  'idle',
  /** Asking the control plane for an upload plan. No bytes have moved. */
  'creating-plan',
  /** A plan exists and the transfer has not started. */
  'ready',
  /** Bytes are moving. */
  'uploading',
  /** Deliberately stopped by the user, or stopped because the device is offline. Resumable. */
  'paused',
  /** A transient failure is being retried within the plan's retry budget. */
  'retrying',
  /** Every byte of this upload has been accepted by the server. Not the same as ready. */
  'completed-upload',
  /** Telling the control plane the asset's components are all transferred. */
  'completing-asset',
  /** The server is scanning, extracting, relaying, transcoding or registering. */
  'processing',
  /** The asset is usable by the product. This is the only state that means ready. */
  'asset-ready',
  /** Terminal failure for this upload. Starting again means a new plan. */
  'failed',
  /** Cancelled by the user. */
  'cancelled',
  /** The upload intent or the tus resource expired before the transfer finished. */
  'expired',
] as const

export type UploadState = (typeof UPLOAD_STATES)[number]

/** States in which the transfer is actively consuming the network. */
export const ACTIVE_UPLOAD_STATES: readonly UploadState[] = ['uploading', 'retrying']

/** States from which no further transport work happens. */
export const TERMINAL_UPLOAD_STATES: readonly UploadState[] = [
  'asset-ready',
  'failed',
  'cancelled',
  'expired',
]

export function isActiveUploadState(state: UploadState): boolean {
  return ACTIVE_UPLOAD_STATES.includes(state)
}

export function isTerminalUploadState(state: UploadState): boolean {
  return TERMINAL_UPLOAD_STATES.includes(state)
}
