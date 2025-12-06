<template>
  <img
    class="absolute inset-0 -z-20 w-full h-full object-cover"
    :src="botConfig.background"
  />
</template>

<script setup lang="ts">
  defineProps(["background"]);
</script>
