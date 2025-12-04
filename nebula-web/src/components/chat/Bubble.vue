<template>
  <ImageBubble v-if="message.type === 'image'" :message />
  <ChartBubble v-else-if="message.type === 'chart'" :message />
  <TextBubble v-else :message />
</template>

<script setup lang="ts">
  import TextBubble from "./TextBubble.vue";
  import ImageBubble from "./ImageBubble.vue";
  import ChartBubble from "./ChartBubble.vue";

  defineProps(["message"]);
</script>
