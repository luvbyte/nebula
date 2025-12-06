<template>
  <div v-if="profileConfig" class="flex flex-col justify-center items-center">
    <img class="w-64 h-64" :src="API_URL + profileConfig.profile" />

    <h1 class="p-2">[ {{ profileConfig.username }} ]</h1>
  </div>
</template>

<script setup lang="ts">
  import { ref, onBeforeMount } from "vue";
  import { getConfig, API_URL } from "@/api/config";

  const profileConfig = ref();

  onBeforeMount(async () => {
    profileConfig.value = await getConfig("user");
  });
</script>
