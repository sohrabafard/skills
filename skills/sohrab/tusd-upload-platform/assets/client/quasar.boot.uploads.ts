import { boot } from 'quasar/wrappers'
import { useTusUpload } from './useTusUpload'

export default boot(({ app }) => {
  app.provide('createTusUpload', useTusUpload)
})
