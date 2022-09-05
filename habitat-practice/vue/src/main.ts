// @ts-ignore
import { createApp, h } from 'vue'
// @ts-ignore
import App from './App.vue'
// import "./assets/icons/styles.css";
import { createHead } from '@vueuse/head';
import StoragePlugin from 'vue-web-storage';
// @ts-ignore
import ColorInput from 'vue-color-input'

const head : any = createHead()

createApp(App)
    .use(StoragePlugin)
    .use(head)
    .component('ColorInput', ColorInput)
    .mount('#app')
    


