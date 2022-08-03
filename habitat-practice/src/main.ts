import { createApp, h } from 'vue'
import App from './App.vue'
// import "./assets/icons/styles.css";
import { createHead } from '@vueuse/head';
const head = createHead()

createApp(App)
    .use(head)
    .mount('#app')

