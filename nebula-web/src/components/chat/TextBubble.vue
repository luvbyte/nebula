<template>
  <div
    class="fade-in max-w-[60%] rounded-lg p-2 px-6"
    :class="
      message.self
        ? 'bg-base-100 text-base-content rounded-br-none shadow-lg'
        : 'bg-info text-info-content rounded-bl-none shadow-lg glass'
    "
  >
    <div class="text-lg break-words whitespace-break-spaces">
      {{ message.message }}
    </div>
    <!--
    <div class="text-xs mt-2 text-end opacity-60">
      {{ formatTimestamp(message.time) }}
    </div>
    -->
  </div>
</template>

<script setup lang="ts">
  // import { formatTimestamp } from "@/api/utils";

  defineProps(["message"]);
</script>
