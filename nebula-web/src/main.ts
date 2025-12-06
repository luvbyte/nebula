import { createApp } from "vue";
// import { createPinia } from "pinia";
import App from "./App.vue";

import "./style.css";
import "toastify-js/src/toastify.css";

import { vSwipe, vSwipeStop } from "@/directives/swipe.js";

const app = createApp(App);

app.directive("swipe", vSwipe);
app.directive("swipe-stop", vSwipeStop);

// app.use(createPinia())

app.mount("#app");
