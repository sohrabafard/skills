import { defineStore } from 'pinia'
import { isTerminalUploadState, type UploadState } from './uploadStates'

/**
 * Multi-upload queue for screens that upload more than one file or keep
 * progress alive across navigation.
 *
 * This skill owns only the tus-protocol facts in this file: the state list,
 * which fields are safe to persist, and the rule that live `tus.Upload`
 * instances never enter store state. Store shape, naming and module layout
 * belong to the frontend skill for the project.
 */
export interface UploadQueueItem {
  appUploadId: string
  displayName?: string
  size: number
  mimeType?: string
  status: UploadState
  progressPercent: number
  bytesUploaded: number
  bytesTotal: number
  /** A safe code, never a message and never a URL. */
  safeErrorCode?: string
  createdAt: string
  updatedAt: string
}

export const useUploadQueueStore = defineStore('uploadQueue', {
  state: () => ({
    items: [] as UploadQueueItem[],
  }),

  getters: {
    activeItems: (state) =>
      state.items.filter((item) => item.status === 'uploading' || item.status === 'paused'),
    failedItems: (state) => state.items.filter((item) => item.status === 'failed'),
  },

  actions: {
    upsert(item: UploadQueueItem) {
      const index = this.items.findIndex((existing) => existing.appUploadId === item.appUploadId)
      if (index === -1) {
        this.items.push(item)
        return
      }
      this.items[index] = { ...this.items[index], ...item, updatedAt: new Date().toISOString() }
    },

    patch(
      appUploadId: string,
      patch: Partial<Omit<UploadQueueItem, 'appUploadId' | 'createdAt'>>,
    ) {
      const item = this.items.find((existing) => existing.appUploadId === appUploadId)
      if (!item) return
      Object.assign(item, patch, { updatedAt: new Date().toISOString() })
    },

    remove(appUploadId: string) {
      this.items = this.items.filter((item) => item.appUploadId !== appUploadId)
    },

    /** Drop everything that will not change again on its own. */
    clearFinished() {
      this.items = this.items.filter((item) => !isTerminalUploadState(item.status))
    },

    /**
     * Required on logout, account switch and project switch. Leaving items
     * behind is how a stored resume candidate from one tenant is offered
     * inside another.
     */
    clearForLogoutOrProjectSwitch() {
      this.items = []
    },
  },
})
