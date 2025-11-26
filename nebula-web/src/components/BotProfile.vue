<template>
  <div class="w-full h-full bg-base-200">
    <div class="p-2 py-4">
      <button @click="close">
        <Icon icon="weui:back-filled" width="28" height="28" />
      </button>
    </div>
    <div class="flex flex-col items-center gap-3">
      <!-- icon big -->
      <div
        class="w-[50%] bg-secondary/60 p-4 rounded-full border-4 border-secondary overflow-hidden"
      >
        <img
          class="rounded-full shadow-2xl"
          :src="activeBot.icon"
        />
      </div>

      <div class="flex flex-col items-center justify-center">
        <!-- title -->
        <p class="text-2xl font-bold capitalize">
          {{ activeBot.title }}
        </p>
        <!-- name -->
        <p class="font-bold opacity-40">@{{ activeBot.name }}</p>
      </div>
    </div>

    <div class="p-2 flex gap-2 items-center px-4 rounded active:bg-base-300">
      <Icon icon="solar:wallpaper-outline" width="26" height="26" />
      <h1 class="text-lg">Theme</h1>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { Icon } from "@iconify/vue";

  const props = defineProps(["activeBot", "botConfig", "close"]);
</script>
