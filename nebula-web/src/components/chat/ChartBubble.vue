<template>
  <div
    class="fade-in w-full min-h-[200px] bg-base-100 text-base-content p-4 rounded flex items-center justify-center"
  >
    <canvas ref="canvas" class="w-full h-full"></canvas>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted } from "vue";
  import { Chart, registerables } from "chart.js";

  // Register everything Chart.js needs
  Chart.register(...registerables);

  const props = defineProps<{ message: any }>();

  const canvas = ref<HTMLCanvasElement | null>(null);

  onMounted(() => {
    if (canvas.value) {
      new Chart(canvas.value, props.message.message);
    }
  });
</script>
