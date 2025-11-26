<!-- ImageSafe.vue -->
<template>
  <img :src="current" @error="current = fallback" />
</template>

<script>
  export default {
    props: ["src", "fallback"],
    data() {
      return { current: this.src };
    }
  };
</script>
