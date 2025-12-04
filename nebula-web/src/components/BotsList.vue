<template>
  <div class="flex-1 flex flex-col">
    <!-- bots list -->
    <div
      class="flex gap-4 p-2 items-center bg-base-200 border border-base-300"
      @click="selectBot(bot)"
      v-for="bot in bots"
      :key="bot.id"
    >
      <!-- icon -->
      <div class="w-12 rounded-full overflow-hidden">
        <img :src="bot.icon" />
      </div>
      <!-- body -->
      <div class="flex-1 flex flex-col">
        <div class="capitalize truncate">{{ bot.title }}</div>
        <div v-if="bot.last?.message" class="text-xs opacity-60 line-clamp-2">
          {{ resolveMessage(bot) }}
        </div>
      </div>
      <!-- count & time -->
      <div class="flex flex-col items-end gap-2">
        <div class="text-xs">{{ formatTimestamp(bot.last?.time) }}</div>
        <div
          v-if="bot.unread > 0"
          class="inline text-xs bg-info text-info-content p-1 px-2 rounded-full"
        >
          {{ bot.unread }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onBeforeMount } from "vue";
  import { getBotsList, connect, onMessage, sendEvent } from "@/api";
  import { formatTimestamp } from "@/api/utils";

  const props = defineProps(["selectBot"]);
  const bots = ref([]);

  function resolveMessage(bot) {
    if (!bot.last?.message) return "";

    const finalCheck = msg => {
      if (bot.last.self) return "You: " + msg;

      return msg;
    };

    switch (bot.last.type) {
      case "image":
        return finalCheck("Sent a photo");
      case "chart":
        return finalCheck("Sent chart message");
      default:
        return finalCheck(bot.last.message);
    }
  }

  onBeforeMount(async () => {
    bots.value = await getBotsList();

    onMessage(async data => {
      if (data.event === "bot-message") {
        bots.value = await getBotsList();
      }
    });
  });
</script>
