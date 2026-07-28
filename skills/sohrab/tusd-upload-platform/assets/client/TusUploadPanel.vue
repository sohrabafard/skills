<script setup lang="ts">
// Minimal example of wiring the composable to a UI.
//
// This skill owns the protocol facts here: a plan is fetched before any byte
// moves, cancel only terminates when the server permits it, and the panel
// says "transferred", not "ready". Component structure, styling, accessibility
// and layout belong to the frontend skill for the project.
import { computed, ref } from 'vue'
import { useTusUpload, type UploadPlanComponent } from './useTusUpload'

const props = defineProps<{
  createPlan: (file: File) => Promise<UploadPlanComponent>
  getFreshHeaders?: () => Promise<Record<string, string>> | Record<string, string>
}>()

const selectedFile = ref<File | null>(null)
const upload = useTusUpload()

const canStart = computed(() => Boolean(selectedFile.value) && !upload.isActive.value)

function onFileSelected(event: Event) {
  const input = event.target as HTMLInputElement
  selectedFile.value = input.files?.[0] ?? null
}

async function startUpload() {
  if (!selectedFile.value) return
  const plan = await props.createPlan(selectedFile.value)
  await upload.start({
    file: selectedFile.value,
    plan,
    getFreshHeaders: props.getFreshHeaders,
  })
}
</script>

<template>
  <section class="tus-upload-panel" aria-label="File upload">
    <input type="file" :disabled="upload.isActive.value" @change="onFileSelected" />

    <div v-if="selectedFile" class="tus-upload-panel__file">
      <strong>{{ selectedFile.name }}</strong>
      <span>{{ Math.ceil(selectedFile.size / 1024 / 1024) }} MiB</span>
    </div>

    <progress :value="upload.progressPercent.value" max="100">
      {{ upload.progressPercent.value }}%
    </progress>

    <div class="tus-upload-panel__actions">
      <button type="button" :disabled="!canStart" @click="startUpload">Start</button>
      <button type="button" :disabled="!upload.canPause.value" @click="upload.pause">Pause</button>
      <button type="button" :disabled="!upload.canResume.value" @click="upload.resume">Resume</button>
      <button
        type="button"
        :disabled="!upload.canCancel.value"
        @click="upload.cancel({ terminate: upload.allowTerminate.value })"
      >
        Cancel
      </button>
    </div>

    <p>Status: {{ upload.status.value }}</p>
    <!-- Transferred is not ready. The product learns readiness from the
         control plane, never from the transfer completing. -->
    <p v-if="upload.status.value === 'completed-upload'">Transferred. Waiting for the server to finish processing.</p>
    <p v-if="upload.terminalError.value">Upload failed. Try again from a new plan.</p>
  </section>
</template>
