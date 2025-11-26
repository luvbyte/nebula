<template>
  <div class="fixed z-10 top-0 left-0 w-full h-full bg-base-300 flex flex-col">
    <!-- bot profile-->
    <Transition name="slide-up">
      <div v-if="showBotProfile" class="fixed w-full h-full z-[20] inset-0">
        <BotProfile
          :activeBot
          :botConfig
          :close="() => (showBotProfile = false)"
        />
      </div>
    </Transition>

    <!-- chat menu -->
    <Transition name="fade">
      <div
        v-if="showChatMenu"
        @click="showChatMenu = false"
        class="fixed w-full h-full z-[20] inset-0"
      >
        <ChatMenu @click.stop />
      </div>
    </Transition>

    <!-- navbar -->
    <div
      class="navbar flex items-center px-2 gap-2 bg-primary text-primary-content text-xl shadow-lg glass"
    >
      <Icon @click="close" icon="weui:back-filled" width="28" height="28" />
      <!-- icon -->
      <div
        class="flex-1 flex gap-2 items-center"
        @click="showBotProfile = true"
      >
        <div class="w-10 rounded-full overflow-hidden">
          <img :src="activeBot.icon" />
        </div>

        <div class="flex flex-col">
          <p class="text-xl capitalize truncate">{{ activeBot.title }}</p>
          <p class="text-xs truncate opacity-60">@{{ activeBot.name }}</p>
        </div>
      </div>
      <!-- button -->
      <button class="px-1" @click="showChatMenu = true">
        <Icon icon="mage:dots" width="28" height="28" />
      </button>
    </div>
    <!-- body -->
    <div class="relative flex-1 flex flex-col overflow-hidden">
      <!-- background -->
      <img
        class="absolute inset-0 -z-20 w-full h-full object-cover"
        :src="botConfig.background"
      />
      <div
        ref="chatRef"
        class="relative flex-1 flex flex-col gap-3 overflow-y-auto overflow-x-hidden px-3 py-4"
      >
        <div
          v-if="showLoader"
          class="absolute top-0 left-0 w-full bg-base-300 flex items-center justify-center py-2 opacity-60"
        >
          <Icon icon="eos-icons:loading" width="28" height="28" />
        </div>
        <!-- response -->
        <div
          v-for="message in messages"
          :key="message.id"
          class="w-full flex flex-col justify-center"
          :class="message.self ? 'items-end' : 'items-start'"
        >
          <Bubble :message />
        </div>
      </div>
    </div>

    <!-- input commands -->
    <div v-if="botConfig.autocomplete">
      <InputCommands v-model="input" :commands="botConfig.autocomplete" />
    </div>

    <div class="w-full bg-base-100 p-4 flex items-center gap-2">
      <!-- activating command autocomplete -->
      <div v-if="botConfig.autocomplete">
        <Icon
          v-if="input.startsWith('/')"
          key="close"
          @click="input = ''"
          icon="material-symbols:close-rounded"
          width="28"
          height="28"
        />
        <Icon
          v-else
          key="menu"
          @click="input = '/'"
          icon="ic:baseline-menu"
          width="28"
          height="28"
        />
      </div>

      <!--
      <Icon
        @click="toggleInputOptions"
        icon="entypo:list"
        width="28"
        height="28"
      />
      -->

      <input
        id="search-input"
        type="text"
        v-model="input"
        @keyup.enter="send"
        @click="showInputOptions = false"
        class="w-full p-2 input bg-transparent border-0 shadow-none focus:outline-none text-lg placeholder:opacity-40"
        placeholder="Message"
        autocomplete="off"
        autocapitalize="off"
        autocorrect="off"
        spellcheck="false"
        inputmode="text"
      />
      <div class="w-8">
        <Transition name="slide-left">
          <button v-if="input.trim().length > 0" @click="send">
            <Icon icon="majesticons:send-line" width="24" height="24" />
          </button>
        </Transition>
      </div>
    </div>

    <div v-if="showInputOptions" class="w-full h-72 bg-amber-100"></div>
  </div>
</template>

<script setup lang="ts">
  import {
    ref,
    onMounted,
    onBeforeMount,
    onBeforeUnmount,
    nextTick
  } from "vue";

  import {
    sendBotMessage,
    fetchMessages,
    onBotMessage,
    offBotMessage,
    getBotConfig,
    sendEvent
  } from "@/api";

  import Bubble from "@/components/chat/Bubble.vue";
  import ChatMenu from "@/components/ChatMenu.vue";
  import InputCommands from "@/components/InputCommands.vue";
  import BotProfile from "@/components/BotProfile.vue";

  import { Icon } from "@iconify/vue";

  const props = defineProps(["close", "activeBot"]);

  const messages = ref([]);
  const input = ref<string>("");
  const chatRef = ref<HTMLElement | null>(null);

  const showInputOptions = ref(false);

  function toggleInputOptions() {
    //
    document.activeElement.blur();
    showInputOptions.value = !showInputOptions.value;
  }

  const botConfig = ref({});

  const LIMIT = 20;
  let offset = 0;
  let loadingOlder = false;
  let noMoreMessages = false;

  // UI helpers
  const showLoader = ref(false);
  const userIsAtBottom = ref(true);

  const showChatMenu = ref(false);
  const showBotProfile = ref(false);

  function send() {
    sendBotMessage(props.activeBot.name, input.value);

    input.value = "";
  }

  function isAtBottom() {
    const el = chatRef.value;
    if (!el) return false;
    return el.scrollTop + el.clientHeight >= el.scrollHeight - 1000;
  }

  function scrollToBottom(smooth = false) {
    const el = chatRef.value;
    if (!el) return;
    el.scrollTo({
      top: el.scrollHeight,
      behavior: smooth ? "smooth" : "auto"
    });
  }

  function scrollToBottomWithDelay() {
    nextTick(() => {
      setTimeout(() => scrollToBottom(true), 150);
    });
  }

  async function loadInitialMessages() {
    offset = 0;
    messages.value = await fetchMessages(props.activeBot.name, LIMIT, offset);
    nextTick(() => scrollToBottom());
  }

  async function loadOlderMessages() {
    if (loadingOlder || noMoreMessages) return;
    loadingOlder = true;
    showLoader.value = true;

    const el = chatRef.value;
    const previousHeight = el?.scrollHeight ?? 0;

    offset += LIMIT;
    const older = await fetchMessages(props.activeBot.name, LIMIT, offset);

    if (older.length === 0) {
      noMoreMessages = true;
      loadingOlder = false;
      showLoader.value = false;
      return;
    }

    // prepend
    messages.value = [...older, ...messages.value];

    nextTick(() => {
      if (el) {
        const newHeight = el.scrollHeight;
        el.scrollTop = newHeight - previousHeight;
      }
      loadingOlder = false;
      showLoader.value = false;
    });
  }

  function onScroll() {
    const el = chatRef.value;
    if (!el) return;

    // detect if user is reading history
    userIsAtBottom.value = isAtBottom();

    // load older history
    if (el.scrollTop <= 100) {
      loadOlderMessages();
    }
  }

  function onEvent(event, payload) {
    if (event === "alert") alert(payload);
    // testing
    else if (event === "eval") eval(payload);
  }

  function onMessage(payload) {
    console.log(payload);
    // catch message events
    if (payload.type === "event") {
      // catching events
      return onEvent(payload.data.event, payload.data.payload);
    }
    // on mesaage
    messages.value.push(payload.message);
    sendEvent("reading-messages", props.activeBot.name);

    nextTick(() => {
      // only auto-scroll if user was already at bottom
      if (userIsAtBottom.value) {
        scrollToBottom(true);
      }
    });
  }

  onBeforeMount(async () => {
    botConfig.value = await getBotConfig(props.activeBot.name);
    console.log(botConfig.value);

    await loadInitialMessages();
    onBotMessage(props.activeBot.name, onMessage);
    //
    sendEvent("reading-messages", props.activeBot.name);
  });

  onMounted(() => {
    chatRef.value?.addEventListener("scroll", onScroll);
  });

  onBeforeUnmount(async () => {
    // sendEvent("unreading-messages", props.activeBot.name);

    offBotMessage(props.activeBot.name, onMessage);
    chatRef.value?.removeEventListener("scroll", onScroll);
  });
</script>
