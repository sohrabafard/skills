import { defineStore } from 'pinia'

export type UploadQueueStatus =
  | 'queued'
  | 'creating-session'
  | 'uploading'
  | 'paused'
  | 'completed-upload'
  | 'processing'
  | 'ready-asset'
  | 'failed'
  | 'cancelled'
  | 'expired'

export interface UploadQueueItem {
  appUploadId: string
  displayName?: string
  size: number
  mimeType?: string
  status: UploadQueueStatus
  progressPercent: number
  bytesUploaded: number
  bytesTotal: number
  safeErrorCode?: string
  createdAt: string
  updatedAt: string
}

export const useUploadQueueStore = defineStore('uploadQueue', {
  state: () => ({
    items: [] as UploadQueueItem[],
  }),

  getters: {
    activeItems: (state) => state.items.filter((item) => item.status === 'uploading' || item.status === 'paused'),
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

    patch(appUploadId: string, patch: Partial<Omit<UploadQueueItem, 'appUploadId' | 'createdAt'>>) {
      const item = this.items.find((existing) => existing.appUploadId === appUploadId)
      if (!item) return
      Object.assign(item, patch, { updatedAt: new Date().toISOString() })
    },

    remove(appUploadId: string) {
      this.items = this.items.filter((item) => item.appUploadId !== appUploadId)
    },

    clearFinished() {
      this.items = this.items.filter(
        (item) => item.status !== 'ready-asset' && item.status !== 'completed-upload' && item.status !== 'cancelled',
      )
    },

    clearForLogoutOrProjectSwitch() {
      this.items = []
    },
  },
})
