<template>
  <q-page class="q-pa-md">
    <div class="text-h6 q-mb-md">Player Lab</div>

    <div style="width: 100%; max-width: 960px; aspect-ratio: 16 / 9;">
      <ShakaPlayer
        :src="src"
        :start-time="startTime"
        :prefer-native-hls="preferNativeHls"
        @ready="onReady"
        @error="onError"
        @time="onTime"
        @stats="onStats"
      />
    </div>

    <div class="q-mt-md column q-gutter-md">
      <q-input
        v-model="src"
        label="Manifest URL"
        filled
      />

      <q-input
        v-model.number="startTime"
        label="Start time (seconds)"
        type="number"
        filled
      />

      <q-toggle
        v-model="preferNativeHls"
        label="Prefer native HLS"
      />
    </div>

    <pre class="q-mt-md" style="white-space: pre-wrap;">{{ log }}</pre>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ShakaPlayer from 'src/components/player/ShakaPlayer.vue'

const src = ref('https://example.com/master.m3u8')
const startTime = ref(0)
const preferNativeHls = ref(false)
const log = ref('')

function appendLog(message: string) {
  log.value = `${message}\n${log.value}`
}

function onReady() {
  appendLog('Player ready')
}

function onError(error: any) {
  appendLog(`Player error: ${JSON.stringify(error)}`)
}

function onTime(payload: any) {
  void payload
}

function onStats(stats: any) {
  appendLog(`Stats: ${JSON.stringify(stats)}`)
}
</script>
