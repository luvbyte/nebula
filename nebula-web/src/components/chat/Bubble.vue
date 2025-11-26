<template>
  <ImageBubble v-if="message.type === 'image'" :message />
  <TextBubble v-else :message />
</template>

<script setup lang="ts">
  import TextBubble from "./TextBubble.vue";
  import ImageBubble from "./ImageBubble.vue";

  defineProps(["message"]);
</script>
