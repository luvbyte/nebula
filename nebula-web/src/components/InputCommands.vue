<template>
  <Transition name="slide-up">
    <div v-if="suggestions.length" class="w-full h-36 overflow-y-auto">
      <!-- Suggestions dropdown -->
      <ul>
        <li
          v-for="(s, i) in suggestions"
          :key="s"
          class="p-2 cursor-pointer flex items-center"
          :class="{ 'bg-primary text-primary-content': i === selectedIndex }"
          @mousedown.prevent="onClickSuggestion(i)"
        >
          {{ text.includes(" ") ? s : "/" + s }}
          <span class="opacity-60 ml-2">
            {{ getHelpText(s) }}
          </span>
        </li>
      </ul>
    </div>
  </Transition>
</template>

<script setup lang="ts">
  import { ref, computed, watch } from "vue";

  const props = defineProps<{
    modelValue: string;
    commands: any;
  }>();

  const emit = defineEmits<{
    (e: "update:modelValue", value: string): void;
  }>();

  // Local copy of text, synced with v-model
  const text = ref(props.modelValue ?? "");

  watch(
    () => props.modelValue,
    v => {
      if (v !== text.value) text.value = v ?? "";
    }
  );

  watch(text, v => {
    if (v !== props.modelValue) emit("update:modelValue", v);
  });

  const selectedIndex = ref(0);

  function parseCommand(text: string) {
    return text.replace("/", "").trim().split(" ");
  }

  const suggestions = computed(() => {
    const value = text.value ?? "";
    if (!value.startsWith("/")) return [];

    const raw = value.replace("/", "");
    const endsWithSpace = raw.endsWith(" ");
    const parts = raw.trim().split(" ");

    const main = parts[0];
    const sub = parts[1] ?? "";

    /* ---------- 1. Top-level suggestions ---------- */
    if (parts.length === 1 && !endsWithSpace) {
      return Object.keys(props.commands).filter(cmd => cmd.startsWith(main));
    }

    /* ---------- 2. Show subcommands when space after main ---------- */
    if (parts.length === 1 && endsWithSpace) {
      const subs =
        props.commands[main as keyof typeof props.commands]?.subcommands ?? {};
      return Object.keys(subs);
    }

    /* ---------- 3. Subcommand suggestions while typing ---------- */
    const subs =
      props.commands[main as keyof typeof props.commands]?.subcommands ?? {};

    if (sub && !endsWithSpace) {
      const filtered = Object.keys(subs).filter(cmd => cmd.startsWith(sub));

      if (filtered.length === 1 && filtered[0] === sub) {
        return [];
      }

      return filtered;
    }

    /* ---------- 4. Command is fully complete ---------- */
    if (sub && subs[sub as keyof typeof subs]) {
      return [];
    }

    return [];
  });

  /* ------------ Help text ------------ */
  function getHelpText(s: string) {
    const value = text.value ?? "";
    const parts = parseCommand(value);
    const main = parts[0];

    const mainCmd = props.commands[main as keyof typeof props.commands];
    const subHelp =
      mainCmd?.subcommands?.[s as keyof typeof mainCmd.subcommands]?.help;
    const topHelp = props.commands[s as keyof typeof props.commands]?.help;

    return subHelp || topHelp || "";
  }

  /* ------------ Selecting a suggestion ------------ */
  function applySuggestion() {
    const value = text.value ?? "";
    const raw = value.replace("/", "");
    const endsWithSpace = raw.endsWith(" ");
    const parts = raw.trim().split(" ");
    const list = suggestions.value;

    if (!list.length) return;

    const main = parts[0];
    const selected = list[selectedIndex.value];

    if (parts.length === 1 && !endsWithSpace && main !== selected) {
      text.value = `/${selected} `;
      return;
    }

    if (parts.length === 1 && endsWithSpace) {
      text.value = `/${main} ${selected} `;
      return;
    }

    if (parts.length >= 2) {
      text.value = `/${main} ${selected} `;
      return;
    }
  }

  function onClickSuggestion(i: number) {
    selectedIndex.value = i;
    applySuggestion();
  }

  /* ------------ Keyboard handling ------------ */
  function onKey(e: KeyboardEvent) {
    if (!suggestions.value.length) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      selectedIndex.value =
        (selectedIndex.value + 1) % suggestions.value.length;
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      selectedIndex.value =
        (selectedIndex.value - 1 + suggestions.value.length) %
        suggestions.value.length;
    } else if (e.key === "Tab" || e.key === "Enter") {
      // autocomplete instead of submitting
      e.preventDefault();
      applySuggestion();
    } else if (e.key === "Escape") {
      selectedIndex.value = 0;
    }
  }
</script>
