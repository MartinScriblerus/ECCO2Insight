import { createApp, h } from 'vue'
import App from './App.vue'
// import "./assets/icons/styles.css";
import { createHead } from '@vueuse/head';
import StoragePlugin from 'vue-web-storage';
import ColorInput from 'vue-color-input'

const head = createHead()

createApp(App)
    .use(StoragePlugin)
    .use(head)
    .component('ColorInput', ColorInput)
    .mount('#app')
    


