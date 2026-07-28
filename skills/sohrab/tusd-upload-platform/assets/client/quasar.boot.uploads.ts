// Register the upload composable as a client-only boot file.
//
// The protocol fact this file carries: upload code must never evaluate during
// server render, because it touches File, Blob, navigator and local storage.
// Register it in quasar.config.ts with `server: false`.
//
// Boot-file convention and dependency-injection style belong to the frontend
// skill for the project.
import { boot } from 'quasar/wrappers'
import { useTusUpload } from './useTusUpload'

export default boot(({ app }) => {
  app.provide('createTusUpload', useTusUpload)
})
