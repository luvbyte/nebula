<template>
  <!-- navbar -->
  <div
    class="navbar navbar-xl glass flex justify-between px-2 gap-3 bg-primary text-primary-content text-xl"
  >
    <div class="flex items-center gap-3">
      <Icon
        @click="showSidebar"
        icon="solar:list-bold-duotone"
        width="28"
        height="28"
      />
      <h1>Nebula</h1>
    </div>

    <div class="flex gap-1 items-center">
      <!-- button -->
      <button @click="showChatMenu = true">
        <Icon icon="mage:dots" width="28" height="28" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { Icon } from "@iconify/vue";

  defineProps(["showSidebar"]);
</script>
