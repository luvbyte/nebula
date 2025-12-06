<template>
  <div @click.self="editBot = null" class="flex-1 flex flex-col">
    <!-- bots list -->
    <div
      class="flex gap-4 p-2 items-center bg-base-200 border border-base-300"
      v-for="bot in bots"
      :key="bot.name"
      @click="selectBot(bot)"
      v-swipe="
        d => {
          d === 'right' ? (editBot = bot.name) : (editBot = null);
        }
      "
    >
      <Transition name="slide-right">
        <button
          @click.stop="showDialouge = true"
          v-if="editBot === bot.name"
          class="flex items-center justify-center p-2 rounded-full"
        >
          <Icon icon="proicons:delete" width="28" height="28" />
        </button>
      </Transition>
      <!-- Icon -->
      <div class="w-12 rounded-full overflow-hidden">
        <img :src="bot.icon" />
      </div>
      <!-- Body -->
      <div class="flex-1 flex flex-col">
        <div class="capitalize truncate">{{ bot.title }}</div>
        <div v-if="bot.last?.message" class="text-xs opacity-60 line-clamp-2">
          {{ resolveMessage(bot) }}
        </div>
      </div>
      <!-- Count & Time -->
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

    <!-- Confirm Dialouge -->
    <Transition name="scale">
      <div
        v-if="showDialouge"
        @click.self="shake"
        class="fixed inset-0 w-full h-full flex items-center justify-center"
      >
        <div
          ref="dialogueRef"
          class="w-[80%] max-w-sm p-4 bg-base-200 rounded base-border shadow-lg"
        >
          <!-- Title -->
          <div class="text-center text-lg font-semibold tracking-wide">
            Confirm Action
          </div>
          <div class="divider m-0"></div>

          <!-- Message -->
          <p class="text-center text-sm text-base-content/80">
            Are you sure you want to delete
            <span class="font-medium text-error">{{ editBot }}</span
            >?
          </p>

          <!-- Actions -->
          <div class="mt-4 flex justify-end gap-2">
            <button
              class="btn btn-success btn-sm rounded-sm"
              aria-label="Cancel delete"
              @click="onCancel"
            >
              Cancel
            </button>
            <button
              @click="onDelete"
              class="btn btn-error btn-sm rounded-sm"
              aria-label="Confirm delete"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
  import { ref, onBeforeMount } from "vue";
  import { Icon } from "@iconify/vue";

  import { connect, onMessage, sendEvent } from "@/api/ws";
  import { getBotsList, uninstallBot } from "@/api/bot";
  import { formatTimestamp, toast } from "@/api/utils";

  defineProps(["selectBot"]);

  const bots = ref([]); // all bots

  const editBot = ref(null); // bot edit mode
  const showDialouge = ref(false); // edit mode bot remove dialouge

  const dialogueRef = ref<HTMLElement | null>(null);

  // shake animation on outside dialouge click
  const shake = () => {
    const el = dialogueRef.value;
    if (!el) return;

    el.classList.remove("shake");
    void el.offsetWidth;
    el.classList.add("shake");
  };

  // on cancel dialouge
  const onCancel = () => {
    showDialouge.value = false;
    editBot.value = null;
  };

  // on delete dialouge
  const onDelete = async () => {
    showDialouge.value = false;
    if (!editBot.value) return;

    try {
      const data = await uninstallBot(editBot.value);
      console.log(data);
      // Toast message
      toast(data.message);
    } catch (err) {
      toast(err.toString(), "error");
    } finally {
      editBot.value = null;
      // update
      updateBots();
    }
  };

  // message short footer TODO
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

  // update bots list ui
  async function updateBots() {
    bots.value = await getBotsList();
  }

  onBeforeMount(async () => {
    updateBots();
    // watching bot-message to update bots list
    onMessage(async data => {
      if (data.event === "bot-message") {
        bots.value = await getBotsList();
      }
    });
  });
</script>

<style scoped>
  .shake {
    animation: shake 0.35s ease-in-out;
  }

  @keyframes shake {
    0% {
      transform: translateX(0);
    }
    20% {
      transform: translateX(-10px);
    }
    40% {
      transform: translateX(10px);
    }
    60% {
      transform: translateX(-10px);
    }
    80% {
      transform: translateX(10px);
    }
    100% {
      transform: translateX(0);
    }
  }
</style>
