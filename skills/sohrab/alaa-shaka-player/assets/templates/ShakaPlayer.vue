<script setup lang="ts">
/**
 * Player component for Vue 3 + Quasar, against Shaka v5.2.3.
 *
 * Follows /alaa-vue-typescript-clean-code ($alaa-vue-typescript-clean-code),
 * references/10-vue-style-contract.md: `interface Props` + `withDefaults`, typed emits,
 * defaults stated exactly once.
 *
 * NOTE what is deliberately absent: there is no `headers` or `token` prop. A credential
 * never travels through the component tree - it enters the player through the request
 * filter that `getGrant` feeds. See references/42-media-url-trust-and-presigned.md.
 */
import { shallowRef, watch } from "vue";
import { useShakaPlayer, type MediaGrant, type PlayerError, type PlayerTuning } from "./useShakaPlayer";
import type { ShakaStats } from "./shakaTypes";

interface Props {
  /** Manifest URL. A change reloads playback; null tears playback down. */
  src: string | null;
  /** Returns a fresh read grant. Called on EVERY request attempt, which is what lets a
   *  retry recover from a 401 without the component knowing anything about it. */
  getGrant?: () => Promise<MediaGrant>;
  /** Overrides for the validated tuning defaults. Out-of-range values throw at setup. */
  tuning?: Partial<PlayerTuning>;
  poster?: string | null;
  autoplay?: boolean;
  muted?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  getGrant: undefined,
  tuning: undefined,
  poster: null,
  autoplay: false,
  muted: false
});

const emit = defineEmits<{
  ready: [];
  error: [value: PlayerError];
  /** Fires on `unloading` - the last moment getStats() holds this session's counters. */
  sessionEnd: [stats: ShakaStats];
}>();

// shallowRef: the element is a DOM node, never deep-proxied.
const videoEl = shallowRef<HTMLVideoElement | null>(null);
const source = shallowRef<string | null>(props.src);

watch(() => props.src, next => { source.value = next; });

const player = useShakaPlayer({
  source,
  videoEl,
  getGrant: props.getGrant,
  tuning: props.tuning,
  onSessionEnd: stats => emit("sessionEnd", stats)
});

// Emit exactly once per transition; the composable owns the state, this only forwards it.
watch(player.ready, isReady => { if (isReady) emit("ready"); });
watch(player.error, value => { if (value) emit("error", value); });

// The composable's onBeforeUnmount awaits dispose(); nothing to do here.
defineExpose({ dispose: player.dispose });
</script>

<template>
  <div class="alaa-shaka-player">
    <video
      ref="videoEl"
      class="alaa-shaka-player__video"
      :poster="props.poster ?? undefined"
      :autoplay="props.autoplay"
      :muted="props.muted"
      playsinline
    ></video>

    <div v-if="player.loading.value" class="alaa-shaka-player__state" role="status">
      <slot name="loading">Loading</slot>
    </div>

    <div v-else-if="player.buffering.value" class="alaa-shaka-player__state" role="status">
      <slot name="buffering">Buffering</slot>
    </div>

    <!--
      The error slot receives the stable `kind`, never a raw Shaka code and never the error
      object: `error.data` for a network failure carries the failing URI and its query string.
      Copy for each kind belongs to /alaa-ui-ux-design-system ($alaa-ui-ux-design-system),
      references/35-ux-writing-and-microcopy.md.
    -->
    <div v-else-if="player.error.value" class="alaa-shaka-player__state" role="alert">
      <slot name="error" :kind="player.error.value.kind">Playback failed</slot>
    </div>

    <slot name="controls"></slot>
  </div>
</template>

<style scoped>
.alaa-shaka-player {
  position: relative;
  inline-size: 100%;
  background: #000;
}
.alaa-shaka-player__video {
  display: block;
  inline-size: 100%;
  block-size: auto;
}
.alaa-shaka-player__state {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
}
</style>
