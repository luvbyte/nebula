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
      <button @click="showTS = true">
        <Icon icon="lineicons:colour-palette-3" width="30" height="30" />
      </button>
      <!-- button -->
      <button @click="showChatMenu = true">
        <Icon icon="mage:dots" width="28" height="28" />
      </button>
    </div>
  </div>
  <Transition name="slide-left">
    <div
      v-show="showTS"
      @click="showTS = false"
      class="fixed top-0 left-0 w-full h-full"
    >
      <div @click.stop class="absolute z-40 top-16 right-0 w-[80%] h-[400px]">
        <ThemeSwitcher />
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
  import { Icon } from "@iconify/vue";

  import { ref } from "vue";

  import ThemeSwitcher from "@/components/ThemeSwitcher.vue";

  const props = defineProps(["showSidebar"]);

  const showTS = ref(false);
</script>
