# Frontend Integration for Vue, Quasar, and Vite

## Table of contents

- Default frontend stance
- Integration patterns
- Vue 3 component pattern
- Quasar guidance
- SSR guidance
- PWA guidance
- UI customization layers
- Useful commands and events
- Product integration rules
- When the IFrame API stops being enough

## Default frontend stance

For product integration, start with the Jitsi IFrame API unless the product truly needs a fully custom media experience.

Why this is the default:

- much lower maintenance than a Jitsi fork
- fast access to mature meeting UX
- supported runtime feature toggles and event hooks
- simpler upgrades than rebuilding meeting UI behavior yourself

Use a custom lower-level integration only when the product absolutely needs bespoke conference chrome, media layout, or direct low-level control that the IFrame API cannot provide.

Also keep recording in mind: Jibri is built around a full Jitsi Meet browser session. If the product plans to replace that surface entirely, recording design becomes harder and should be called out early.

## Integration patterns

### Best default for most teams

- your backend issues a room-scoped Jitsi JWT near join time
- your Vue route or page mounts a client-only meeting component
- the component loads `external_api.js` from your Jitsi deployment
- the component creates `JitsiMeetExternalAPI` with config overrides and event listeners
- the component relays meeting events into your app store or analytics collector
- the component disposes the API instance on unmount

### What the host app should own

- room metadata and permissions
- token fetch and refresh policy
- route guards and tenant checks
- watch-time heartbeats and analytics shipping
- post-meeting actions such as survey, replay links, or artifact pages

## Vue 3 component pattern

This pattern works well for Vite and plain Vue 3.

```ts
<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

const containerRef = ref<HTMLElement | null>(null)
let api: any = null

async function loadScript(src: string) {
  await new Promise<void>((resolve, reject) => {
    const existing = document.querySelector(`script[src="${src}"]`)
    if (existing) return resolve()
    const script = document.createElement('script')
    script.src = src
    script.async = true
    script.onload = () => resolve()
    script.onerror = () => reject(new Error(`Failed to load ${src}`))
    document.head.appendChild(script)
  })
}

onMounted(async () => {
  if (!containerRef.value) return

  const { domain, roomName, jwt, userInfo } = await fetch('/api/meet/join', {
    method: 'POST',
    credentials: 'include'
  }).then(r => r.json())

  await loadScript(`https://${domain}/external_api.js`)

  api = new (window as any).JitsiMeetExternalAPI(domain, {
    roomName,
    parentNode: containerRef.value,
    jwt,
    userInfo,
    configOverwrite: {
      prejoinPageEnabled: true,
      startWithAudioMuted: false,
      startWithVideoMuted: true
    },
    interfaceConfigOverwrite: {}
  })

  api.addListener('videoConferenceJoined', payload => {
    console.log('joined', payload)
  })

  api.addListener('readyToClose', () => {
    console.log('meeting closing')
  })
})

onBeforeUnmount(() => {
  if (api) {
    api.dispose()
    api = null
  }
})
</script>

<template>
  <div ref="containerRef" class="meeting-shell" />
</template>
```

Important rules:

- create the API only after the client has mounted
- dispose it on route change or component teardown
- let your app own navigation outside the embedded meeting
- keep host app state separate from Jitsi UI state

## Quasar guidance

Quasar is a good host shell for Jitsi when you keep the boundary clean.

Recommended structure:

- route-level page controls access and room metadata
- a dedicated child component mounts Jitsi
- a Pinia store or equivalent holds platform meeting state
- Quasar dialogs and notifications react to platform events, not raw embed internals everywhere

Useful Quasar patterns:

- use `Notify` for join failure or reconnect state
- use `Dialog` for “leave room” and post-session actions
- keep the meeting view in a full-height page layout with minimal host chrome
- use `QNoSsr` or a client-only wrapper for SSR builds

## SSR guidance

Never instantiate Jitsi during server-side render.

### SSR-safe rules

- do not touch `window`, `document`, or `JitsiMeetExternalAPI` on the server
- render a placeholder shell during SSR
- mount the real meeting only in a client lifecycle
- load `external_api.js` only in the browser

### Useful pattern

- server renders a meeting shell with route metadata and access checks
- client fetches join data after hydration
- client mounts the Jitsi component only when token and room info are ready

### Token guidance for SSR

Prefer issuing the join token close to actual join time.

Do not embed long-lived join tokens into SSR HTML.

## PWA guidance

Treat the meeting route as network-sensitive rather than offline-first.

### PWA rules

- do not rely on service-worker-cached meeting state for active sessions
- avoid stale caching of `external_api.js`, meeting bootstrap HTML, or websocket-sensitive paths
- handle background throttling and visibility changes explicitly
- expect reconnects after app resume on mobile
- keep analytics heartbeats resilient to offline gaps and retries

### User-experience notes

- ask for mic and camera permissions at a deliberate moment
- surface reconnect state clearly
- treat app backgrounding as a meeting-state transition, not a no-op
- test installable PWA flows on real devices, not only desktop Chrome

## UI customization layers

Use the lightest layer that solves the request.

### Layer 1: deployment-level defaults

Use server-side config files when the behavior should apply broadly across tenants or rooms.

Typical files and patterns:

- `config.js`
- `custom-config.js`
- `interface_config.js` or newer equivalents when still used by the chosen packaging
- packaging-specific custom config append files in Docker setups

Use this for:

- feature defaults
- branding defaults
- analytics defaults
- host-level restrictions that must not be bypassed by embed callers

### Layer 2: embed-time overrides

Use IFrame constructor options for room-specific or product-context-specific behavior.

Useful fields and patterns:

- `configOverwrite`
- `interfaceConfigOverwrite`
- `jwt`
- `userInfo`
- `lang`
- `iceServers` only when you intentionally override platform ICE behavior
- `buttonsWithNotifyClick` when the host app wants to intercept selected toolbar actions
- `participantMenuButtonsWithNotifyClick` when the host app needs product-specific participant actions
- `useHostPageLocalStorage` when embed persistence should follow host-page storage behavior
- people-search or invite URLs only when the platform deliberately owns invite flows

### Layer 3: runtime commands

Use runtime commands only for dynamic user-flow behavior after mount.

A key tool is the `overwriteConfig` command. Use it carefully for runtime changes that are actually supported in the current version.

## Useful commands and events

These are especially useful for product integration.

### Commands

- `toggleShareScreen`
- `overwriteConfig`
- `setLargeVideoParticipant`
- `toggleAudio`
- `toggleVideo`
- moderator-related commands only when your deployment supports them as expected

### Events

- `videoConferenceJoined`
- `videoConferenceLeft`
- `participantJoined`
- `participantLeft`
- `screenSharingStatusChanged`
- `recordingStatusChanged`
- `breakoutRoomsUpdated`
- `audioMuteStatusChanged`
- `readyToClose`
- `log` if explicit Jitsi-side log capture is needed

### Functions

- `getSessionId()`
- `getNumberOfParticipants()`
- `getRoomsInfo()`
- `getSupportedCommands()`
- `getSupportedEvents()`

Use the supported-functions queries when a feature may vary across versions or deployments.

## Product integration rules

Keep these rules in place when integrating with the larger platform.

- host app remains the system of record for navigation, analytics, and post-session state
- do not mirror every Jitsi internal state into your store; keep only product-relevant state
- do not trust embed-time role hints unless they are backed by the server-minted JWT
- prefer platform-driven UI outside the meeting frame for billing, attendance, and lifecycle actions
- do not assume every config key can be overridden at embed time; some must stay in server config

Important examples:

- host and role semantics should not be assumed to be overrideable through `configOverwrite` in current Jitsi behavior
- some security-sensitive settings must remain in the deployment config
- lobby, visitor, and moderator behavior should be treated as deployment and auth concerns first, UI concerns second

## When the IFrame API stops being enough

Reconsider the architecture when the product requires any of these:

- a custom in-conference visual language that replaces most native meeting chrome
- deep media layout control beyond supported commands and config
- cross-room orchestration tightly embedded in your own meeting canvas
- custom moderation UX that diverges heavily from Jitsi’s built-in flows

At that point, be explicit about the maintenance cost of a Jitsi fork or a lower-level `lib-jitsi-meet` integration.
