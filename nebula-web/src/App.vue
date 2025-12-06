<script setup lang="ts">
  import { ref, onBeforeMount } from "vue";
  import Bot from "@/components/Bot.vue";
  import Navbar from "@/components/Navbar.vue";
  import BotsList from "@/components/BotsList.vue";
  import AddBot from "@/components/AddBot.vue";
  import Sidebar from "@/components/Sidebar.vue";

  import { connect } from "@/api/ws";

  import { Icon } from "@iconify/vue";

  const activeBot = ref(null);
  const showSidebar = ref(false);

  const showAddBot = ref(false);

  function selectBot(bot) {
    activeBot.value = bot;
  }

  onBeforeMount(async () => {
    connect();
  });
</script>

<template>
  <div id="main" class="relative h-dvh flex flex-col overflow-hidden">
    <Navbar :showSidebar="() => (showSidebar = true)" />

    <Transition name="scale">
      <AddBot v-if="showAddBot" :close="() => (showAddBot = false)" />
      <Bot v-else-if="activeBot" :activeBot :close="() => (activeBot = null)" />
      <BotsList v-else :selectBot />
    </Transition>

    <!-- sidebar -->
    <Transition name="slide-right">
      <Sidebar v-show="showSidebar" :close="() => (showSidebar = false)" />
    </Transition>

    <!-- fab -->
    <div class="fixed bottom-3 right-3">
      <button
        @click="showAddBot = true"
        class="btn btn-circle btn-primary btn-xl"
      >
        <Icon icon="line-md:plus" width="28" height="28" />
      </button>
    </div>
  </div>
</template>
