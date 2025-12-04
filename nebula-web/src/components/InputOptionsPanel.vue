<template>
  <!-- add file btn  -->
  <!-- button once on single file upload  -->
  <div
    v-if="!multiple && filesLength <= 0"
    class="absolute inset-0 bg-base-300 w-full h-full flex items-center justify-center"
  >
    <label for="filePicker" class="btn btn-lg btn-primary shadow-2xl">
      <Icon icon="formkit:add" width="24" height="24" /> Add File
    </label>
  </div>
  <!-- static button if multiple  -->
  <label
    v-if="multiple"
    for="filePicker"
    class="bg-primary text-primary-content py-2 shadow-lg flex items-center justify-center text-2xl cursor-pointer"
  >
    Add File
  </label>

  <div class="p-4">
    <!-- Grid -->
    <div v-if="files.length" class="grid grid-cols-3 gap-3">
      <div
        v-for="item in files"
        :key="item.id"
        class="relative group rounded-lg overflow-hidden bg-gray-100 shadow-sm"
      >
        <!-- image preview -->
        <img
          v-if="item.previewUrl"
          :src="item.previewUrl"
          class="w-full h-28 object-cover"
        />

        <!-- filename preview -->
        <div
          v-else
          class="flex flex-col justify-center items-center w-full h-28 text-xs text-gray-500"
        >
          {{ item.file.name }}
        </div>

        <!-- remove btn -->
        <button
          class="absolute top-1 right-1 bg-black/60 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs hover:bg-black transition"
          @click="removeFile(item.id)"
        >
          ✕
        </button>
      </div>
    </div>
  </div>
  <!-- file picker -->
  <input
    id="filePicker"
    type="file"
    :multiple="multiple"
    :accept="accept"
    class="hidden"
    @change="handleFiles"
  />
</template>

<script setup lang="ts">
  import { ref, computed, onBeforeUnmount } from "vue";

  import { Icon } from "@iconify/vue";

  interface UIFile {
    id: number;
    file: File;
    previewUrl: string | null;
  }

  const props = defineProps({
    accept: {
      type: String,
      default: () => "*/*"
    },
    multiple: {
      type: Boolean,
      default: () => false
    }
  });

  const files = ref<UIFile[]>([]);
  const idCounter = ref(0);

  function handleFiles(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files) return;

    const list = Array.from(input.files);

    // clear old preview
    if (!props.multiple) {
      files.value.forEach(
        f => f.previewUrl && URL.revokeObjectURL(f.previewUrl)
      );
      files.value = [];
    }

    for (const f of list) {
      const isImage = f.type.startsWith("image/");
      const previewUrl =
        isImage && typeof URL !== "undefined" ? URL.createObjectURL(f) : null;

      files.value.push({
        id: idCounter.value++,
        file: f,
        previewUrl
      });

      // if not multiple files
      if (!props.multiple) break;
    }

    input.value = "";
  }

  function removeFile(id: number) {
    const index = files.value.findIndex(item => item.id === id);
    if (index === -1) return;
    const item = files.value[index];

    if (item.previewUrl && typeof URL !== "undefined") {
      URL.revokeObjectURL(item.previewUrl);
    }
    files.value.splice(index, 1);
  }

  onBeforeUnmount(() => {
    // cleanup
    for (const item of files.value) {
      if (item.previewUrl && typeof URL !== "undefined") {
        URL.revokeObjectURL(item.previewUrl);
      }
    }
  });

  const getFiles = () => files.value.map(f => f.file);
  const filesLength = computed(() => files.value.length);

  // exposed
  defineExpose({ getFiles });
</script>
