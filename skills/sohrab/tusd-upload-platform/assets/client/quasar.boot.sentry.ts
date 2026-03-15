import { defineBoot } from '#q-app/wrappers'
import * as Sentry from '@sentry/vue'

export default defineBoot(({ app, router }) => {
  if (typeof window === 'undefined') {
    return
  }

  const dsn = import.meta.env.VITE_SENTRY_DSN
  if (!dsn) {
    return
  }

  Sentry.init({
    app,
    dsn,
    environment: import.meta.env.MODE,
    integrations: [
      Sentry.browserTracingIntegration({ router }),
    ],
    tracesSampleRate: 0.1,
    sendDefaultPii: false,
    // Uncomment if your platform tunnels browser events through your own app.
    // tunnel: '/monitoring/tunnel',
    beforeSend(event) {
      if (event.request?.headers) {
        delete event.request.headers.Authorization
        delete event.request.headers.authorization
        delete event.request.headers.Cookie
        delete event.request.headers.cookie
      }

      return event
    },
  })
})
