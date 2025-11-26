<template>
  <div
    class="absolute right-2 top-18 bg-base-100 text-base-content min-w-42 p-4 rounded"
  >
    <button
      class="flex gap-4 items-center rounded p-2 w-full active:bg-base-300 transition duration-300"
    >
      <Icon icon="hugeicons:clean" width="28" height="28" />
      <h1>Clear chat</h1>
    </button>
    <button
      class="flex gap-4 items-center rounded p-2 w-full active:bg-base-300 transition duration-300"
    >
      <Icon icon="solar:wallpaper-outline" width="26" height="26" />
      <h1>Change Wallpaper</h1>
    </button>
  </div>
</template>

<script setup>
  import { Icon } from "@iconify/vue";
</script>
