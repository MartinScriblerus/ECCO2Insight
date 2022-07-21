<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  open: Boolean,
  tocdata: Object,
  rawtextdata: String
});
const rawtextfromtoc= ref({});
console.log("HERE IS TOC: ", props.tocdata);
console.log("HERE IS RAW TEXT: ", rawtextfromtoc.value)

const emit = defineEmits(['closedmodal'])

watch(() => props.selected, (tocdata, rawtextdata) => {
      console.log(
        "Here Watch props.selected function called with args:",
        tocdata,
        rawtextdata
      );
    });

// TODO: componentize and DRY this function (see TheWelcome)
async function scrape_text(url){    
    rawtextfromtoc.value = await fetch('http://localhost:5000/scraper_get_text', {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      method: "POST",
      body: JSON.stringify({titleUrl: url})
    }).then(response => response.json()).then(result => {
            if(result){
                rawtextfromtoc.value = result;
                console.log("hhhere's the text: ", JSON.parse(JSON.stringify(rawtextfromtoc.value)));
                
                return rawtextfromtoc.value;
            } else {
              return null;
            }
            }).catch(error => {
            console.log('Error:', error);
            }); 
      return rawtextfromtoc;
};
</script>

<template>

<Teleport to="body">
  <div v-if="open" class="modal">
    <button id="closeBtn" @click="$emit('closedmodal')"
    >Close</button>
    <h1 id="tocHeader">Table of Contents</h1>
    <span id="tocSubtitle">Click any link below to load the text</span>
    <div id="tocDataWrapper">
        <div id="tocData" v-for="item in props.tocdata">
            <h3 @click="scrape_text(item.link_href)">{{
                item.link_text
            }}</h3>
        </div>
    </div>
    <!-- <p id="textData">{{rawtextfromtoc ? rawtextfromtoc.value : null}}</p> -->
    <div id="textData">
    {{rawtextfromtoc ? rawtextfromtoc.value : null}}
    </div>

  </div>
</Teleport>

</template>

<style scoped>
@keyframes animate-text-scrape {
  0%    { height: 0vh; opacity: 0 }
  100%  { height: 100vh; opacity: 1 }
}
.modal {
    position: fixed;
    z-index: 999;
    top: 0%;
    bottom: 0%;
    align-items: center;
    left: 0%;
    width: 50%;
    height: 100vh;
    animation: animate-text-scrape 1s linear;
    background: var(--color-background);
    backdrop-filter: blur(8px);
    overflow-y: scroll;
    padding: 16px;
}
#closeBtn {
    right: 12px;
    position: absolute;
    color: rgba(255,255,255,0.9);
    z-index: 30;
    top: 16px;
    position: fixed;
}
#tocHeader {
    width: 100%;
    text-align: center;
    font-weight: 500;
    border-bottom: solid 1px hsla(160, 100%, 37%, 0.7);
    padding-left: 48px;
    padding-right: 48px;
    color: rgba(255,255,255,1);
    padding:8px;
}
#tocSubtitle {
    padding-left: 4px;
    padding-right: 4px;

}
#tocData {
    margin-top: 8px;
    border-bottom: solid 1px rgba(255, 255, 255, 0.3);
    color: rgba(255,255,255,1);
    font-size: 1rem;

    margin-bottom: 0.1rem;
    font-weight: 500;

    color: var(--color-heading);
    padding-top: 12px;
}
#tocDataWrapper {
    margin: 12px;
    margin-top: 16px;
    padding-left: 24px;
    padding-right: 24px;
}
</style>