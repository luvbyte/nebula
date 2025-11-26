<script setup lang="ts">
  import { ref, onMounted } from "vue";

  // All daisyui themes
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
    "aqua",
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

  const currentTheme = ref<string>("light");

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

<template>
  <div
    class="w-full h-full bg-base-300 grid grid-cols-2 sm:grid-cols-3 gap-2 p-4 overflow-y-auto"
  >
    <div
      v-for="theme in themes"
      :key="theme"
      :data-theme="theme"
      @click="applyTheme(theme)"
      class="flex justify-between bg-primary text-primary-content p-1 py-3 rounded shadow-lg cursor-pointer hover:shadow-md hover:-translate-y-0.5 transition-all"
      :class="currentTheme === theme ? 'border border-white' : ''"
    >
      <span class="font-medium tracking-wide capitalize truncate">{{
        theme
      }}</span>
      <div class="flex gap-1">
        <div class="bg-secondary rounded w-1 h-2"></div>
        <div class="bg-accent rounded w-1 h-2"></div>
        <div class="bg-info rounded w-1 h-2"></div>
        <div class="bg-success rounded w-1 h-2"></div>
      </div>
    </div>
  </div>
</template>
