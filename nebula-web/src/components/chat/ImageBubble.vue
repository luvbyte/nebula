<template>
  <div
    class="rounded min-h-[200px] overflow-hidden shadow-lg relative"
    :class="
      isFullscreen
        ? 'fixed inset-0 bg-black flex justify-center items-center z-[9999]'
        : 'w-[80%]'
    "
    @click="toggleFullscreen"
  >
    <!-- Loader -->
    <div
      v-if="showLoader"
      class="absolute inset-0 flex items-center justify-center transition-opacity duration-500 ease-out"
      :class="isLoaded ? 'opacity-0' : 'opacity-100'"
    >
      <div class="loader"></div>
    </div>

    <!-- Image -->
    <img
      :src="props.message.message.url"
      @load="handleLoad"
      class="cursor-pointer transition-all duration-700 ease-out rounded overflow-hidden"
      :class="[
        isFullscreen ? 'max-h-full max-w-full' : 'w-full h-full object-contain',
        isLoaded
          ? 'opacity-100 blur-0 scale-100'
          : 'opacity-0 blur-md scale-105'
      ]"
      alt="image"
    />
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, onBeforeUnmount } from "vue";

  const props = defineProps(["message"]);

  const isFullscreen = ref(false);
  const isLoaded = ref(false);
  const showLoader = ref(true);

  const toggleFullscreen = () => {
    isFullscreen.value = !isFullscreen.value;
  };

  const handleLoad = () => {
    isLoaded.value = true;
    setTimeout(() => {
      showLoader.value = false;
    }, 500);
  };

  const handleEsc = (e: KeyboardEvent) => {
    if (e.key === "Escape" && isFullscreen.value) {
      isFullscreen.value = false;
    }
  };

  onMounted(() => window.addEventListener("keydown", handleEsc));
  onBeforeUnmount(() => window.removeEventListener("keydown", handleEsc));
</script>

<style scoped>
  /* Smooth loader spinner */
  .loader {
    width: 32px;
    height: 32px;
    border: 3px solid rgba(255, 255, 255, 0.25);
    border-top-color: white;
    border-radius: 50%;
    animation:
      spin 0.8s linear infinite,
      fadein 0.3s ease-out forwards;
    opacity: 0;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  @keyframes fadein {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
</style>
