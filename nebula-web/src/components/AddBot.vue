<template>
  <div class="fixed z-10 w-full h-full inset-0 bg-base-200 p-2 text-lg">
    <div class="p-2 flex items-center gap-3">
      <Icon @click="close" icon="weui:back-filled" width="28" height="28" />
      <h1>Install Bot</h1>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { Icon } from "@iconify/vue";

  defineProps(["close"]);
</script>
