<template>
  <div class="shaka-shell">
    <div ref="containerEl" class="shaka-container">
      <video
        ref="videoEl"
        class="shaka-video"
        playsinline
        controls
      />
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, shallowRef, watch } from 'vue'
import { useShakaCore, type ShakaCoreApi, type ShakaCoreConfig } from './useShakaCore'

type Props = {
  src: string
  startTime?: number
  autoplay?: boolean
  poster?: string
  extraHeaders?: Record<string, string>
  preferNativeHls?: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'ready', api: ShakaCoreApi): void
  (e: 'error', error: unknown): void
  (e: 'unsupported'): void
  (e: 'time', payload: { currentTime: number; duration: number }): void
  (e: 'stats', stats: any): void
}>()

const videoEl = shallowRef<HTMLVideoElement | null>(null)
const containerEl = shallowRef<HTMLDivElement | null>(null)

const core = useShakaCore()

onMounted(async () => {
  if (!videoEl.value) return

  const config: ShakaCoreConfig = {
    videoEl: videoEl.value,
    containerEl: containerEl.value ?? undefined,
    src: props.src,
    startTime: props.startTime ?? 0,
    autoplay: props.autoplay ?? false,
    poster: props.poster,
    extraHeaders: props.extraHeaders ?? {},
    preferNativeHls: props.preferNativeHls ?? false,
    onUnsupported: () => emit('unsupported'),
    onError: (error) => emit('error', error),
    onTime: (payload) => emit('time', payload),
    onStats: (stats) => emit('stats', stats),
  }

  const api = await core.init(config)
  emit('ready', api)
})

watch(
  () => props.src,
  async (src) => {
    if (!src) return
    await core.load({ src, startTime: props.startTime ?? 0 })
  }
)

onBeforeUnmount(async () => {
  await core.destroy()
})
</script>

<style scoped>
.shaka-shell {
  width: 100%;
  height: 100%;
}

.shaka-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.shaka-video {
  width: 100%;
  height: 100%;
}
</style>
