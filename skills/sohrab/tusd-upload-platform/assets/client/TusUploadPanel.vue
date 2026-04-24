<script setup lang="ts">
import { computed, ref } from 'vue'
import { useTusUpload, type TusUploadSession } from './useTusUpload'

const props = defineProps<{
  createSession: (file: File) => Promise<TusUploadSession>
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
  const session = await props.createSession(selectedFile.value)
  await upload.start({
    file: selectedFile.value,
    session,
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
      <button type="button" :disabled="!upload.canCancel.value" @click="upload.cancel({ terminate: true })">Cancel</button>
    </div>

    <p>Status: {{ upload.status.value }}</p>
    <p v-if="upload.terminalError.value">{{ upload.terminalError.value.message }}</p>
  </section>
</template>
