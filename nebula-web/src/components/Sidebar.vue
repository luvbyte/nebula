<template>
  <div @click.self="close" class="fixed top-0 left-0 w-full h-full">
    <div class="w-[80%] h-full flex flex-col gap-2 p-2 bg-base-200 shadow-xl">
      <!-- nebula icon -->
      <Profile />
      <!-- version @ author -->
      <div v-if="false" class="flex justify-between gap-2 items-center p-2">
        <div>@kikku</div>
        <div class="flex-1 w-full h-0.5 bg-base-content/60 rounded"></div>
        <h1>v0.0.1</h1>
      </div>
      <!-- themes -->
      <div class="py-2 flex flex-col overflow-hidden text-xs">
        <div class="divider m-0">THEMES</div>
        <div
          class="rounded grid grid-rows-2 grid-flow-col space-x-1 space-y-1 py-2 overflow-x-auto scrollbar-hide"
        >
          <div
            v-for="theme in themes"
            :data-theme="theme"
            @click="applyTheme(theme)"
            class="w-12 h-12 shrink-0 rounded-full base-border flex items-center justify-center gap-1 p-1 active:border-base-content"
          >
            <div class="w-1 h-4 bg-primary rounded"></div>
            <div class="w-1 h-4 bg-secondary rounded"></div>
            <div class="w-1 h-4 bg-info rounded"></div>
            <div class="w-1 h-4 bg-primary rounded"></div>
          </div>
        </div>
        <div class="capitalize text-end divider m-0">{{ currentTheme }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted } from "vue";

  import Profile from "@/components/Profile.vue";

  defineProps(["close"]);

  const themes: string[] = [
    "light",
    "dark",
    "cupcake",
    "bumblebee",
    "emerald",
    "corporate",
    "synthwave",
    "retro",
    "cyberpunk",
    "valentine",
    "halloween",
    "garden",
    "forest",
    "lofi",
    "pastel",
    "fantasy",
    "wireframe",
    "black",
    "luxury",
    "dracula",
    "cmyk",
    "autumn",
    "business",
    "acid",
    "lemonade",
    "night",
    "coffee",
    "winter",
    "dim",
    "nord",
    "sunset",
    "caramellatte",
    "abyss",
    "silk"
  ];

  const currentTheme = ref<string>("dracula");

  // Apply theme to #main
  const applyTheme = theme => {
    currentTheme.value = theme;
    localStorage.setItem("theme", theme);

    document.getElementById("main")?.setAttribute("data-theme", theme);
  };

  onMounted(() => {
    const saved = localStorage.getItem("theme");
    applyTheme(saved || currentTheme.value);
  });
</script>
