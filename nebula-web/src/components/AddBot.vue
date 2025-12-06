<template>
  <div
    class="fixed z-10 w-full h-full inset-0 bg-base-200 p-2 text-lg flex flex-col gap-1 overflow-hidden"
  >
    <div class="p-2 flex justify-between items-center gap-3">
      <div class="flex items-center gap-2">
        <Icon @click="close" icon="weui:back-filled" width="28" height="28" />
        <h1>Bots Store</h1>
      </div>

      <input
        ref="fileInput"
        type="file"
        accept=".zip .nebula"
        @change="uploadBot"
        style="display: none"
      />
      <button
        @click="fileInput.click()"
        :disabled="loading"
        class="btn btn-sm btn-primary"
      >
        <Icon
          v-if="loading"
          icon="line-md:downloading-loop"
          width="24"
          height="24"
        />
        <Icon v-else icon="clarity:install-line" width="24" height="24" />
      </button>
    </div>

    <!-- Bots Store -->
    <div class="p-2">
      <input
        type="search"
        class="input w-full placeholder:opacity-60"
        placeholder="Search bot"
      />
    </div>

    <!-- Category Buttons -->
    <div class="p-2 flex gap-2 items-center justify-center flex-wrap">
      <div
        class="rounded p-1 px-2 btn btn-xs btn-secondary btn-outline btn-active"
      >
        Featured
      </div>
      <div class="rounded p-1 px-2 btn btn-xs btn-secondary btn-outline">
        Tools
      </div>
      <div class="rounded p-1 px-2 btn btn-xs btn-secondary btn-outline">
        Featured
      </div>
      <div class="rounded p-1 px-2 btn btn-xs btn-secondary btn-outline">
        Featured
      </div>
      <div class="rounded p-1 px-2 btn btn-xs btn-secondary btn-outline">
        Featured
      </div>
      <div class="rounded p-1 px-2 btn btn-xs btn-secondary btn-outline">
        Featured
      </div>
    </div>
    <!-- Bots list Buttons -->
    <div class="p-2 flex-1 flex flex-col gap-2 overflow-y-auto">
      <div
        v-for="i in 50"
        class="w-full rounded border border-base-content/20 p-2 flex gap-2"
      >
        <div class="p-2 w-8"></div>
        <div class="p-2">Content</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from "vue";
  import { Icon } from "@iconify/vue";

  import { toast } from "@/api/utils";
  import { installBot } from "@/api/bot";

  const props = defineProps(["close"]);

  const fileInput = ref(null);
  const loading = ref(false);

  // upload bot to install
  const uploadBot = async e => {
    const file = e.target.files[0];
    if (!file) return;

    loading.value = true;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const data = await installBot(formData);
      console.log(data);
      // Toast response message
      toast(data.message);
      // close this panel
      props.close();
    } catch (err) {
      console.error(err);

      // toast error
      toast(err.toString(), "error");
    } finally {
      loading.value = false;
      e.target.value = null;
    }
  };
</script>
