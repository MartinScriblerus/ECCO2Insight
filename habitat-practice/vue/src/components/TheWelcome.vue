<script setup lang="ts">
// import WelcomeItem from './WelcomeItem.vue'
// import TheWelcome from './TheWelcome.vue'
import Modal from './Modal.vue'
// import DocumentationIcon from './icons/IconDocumentation.vue'
// import ToolingIcon from './icons/IconTooling.vue'
// import EcosystemIcon from './icons/IconEcosystem.vue'
// import CommunityIcon from './icons/IconCommunity.vue'
// import SupportIcon from './icons/IconSupport.vue'
import moment from 'moment';
import { watch, ref, computed } from 'vue'
// import GraphModal from './GraphModal.vue'
const props = defineProps({
  items: Object,
  loaded: Boolean,
});


const selectedTitle : any = ref('');
const selectedAuthor : any = ref('')
const tocData : any = ref({});
const rawTextData : any = ref("");
const open : any = ref(false);
const openGraph : any = ref(false);
const openFull : any = ref(false);
// const modalFull : any = ref(null);
// const modal : any = ref(Modal);

if(props.items){
  emit("getImages", props.items)
  console.log("hitting this/////// ")
  watch(props.items, (currentValue, oldValue) => {
    console.log(currentValue);
    console.log(oldValue);
    console.log("OUTSIDE");
    if(props.items){
      console.log("INSIDE: ", props.items);
      console.log("emitting this... ", JSON.parse(JSON.stringify(props.items)))
      
      emit("getWikiUrl", props.items)
    }
    return;
  });
}

const emit = defineEmits(["getWikiURL", "getImages"])

async function show_TOC(url:String, title:String, author:String){
  selectedTitle.value = title;
  selectedAuthor.value = author;
  // console.log("selected title in welcome: ", selectedTitle.value);
  // console.log("selected author in welcome: ", selectedAuthor.value);
  let jumbotron = document.getElementById("jumbotron");
  if(jumbotron){
    jumbotron.style.display = "none";
  }
  let main = document.getElementById("main")
  if(main){
    main.style.top = "0px";
  }
  let searchForms = document.getElementById("headerDiv");
  if(searchForms){
    searchForms.style.visibility = "hidden";
  }
  tocData.value = await fetch('http://localhost:5000/scraper_get_toc', {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    method: "POST",
    body: JSON.stringify({title: title, author: author, titleUrl: url})
  }).then(response => response.json()).then(result => {
    if(result.length){
      tocData.value = result;
      return tocData.value;
    } else {
      return null;
    }
    }).catch(error => {
      console.log('Error:', error);
    }); 
    console.log("here's the table of contents: ", tocData.value);
    
    return tocData.value;
};

async function scrape_text(url:String){ 
    let wrapperTitle = document.getElementById("buttonsWrapperTitle");
    let wrapperSubtitle = document.getElementById("buttonsWrapperSubtitle");
    let wrapperBtns = document.getElementById("buttonsInnerWrapper");
    if(wrapperTitle){
      wrapperTitle.style.display = "inline-block";
    } else {
      console.log("wrapper title missing");
    }
    if(wrapperSubtitle){
      wrapperSubtitle.style.display = "inline-block";
    } else {
      console.log("wrapper subtitle missing");
    }
    if(wrapperBtns){
      wrapperBtns.style.display = "inline-block";
    } else {
      console.log("wrapper btns missing");
    }
    let jumbotron = document.getElementById("jumbotron");
    if(jumbotron){
      jumbotron.style.display = "none";
    }  

    let main = document.getElementById("main");
    if(main){
      main.style.top = "0px"; 
    }
  
    rawTextData.value = await fetch('http://localhost:5000/scraper_get_text', {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      method: "POST",
      body: JSON.stringify({titleUrl: url})
    }).then(response => response.json()).then(result => {
            if(result.length){
              rawTextData.value = result;
              console.log("here's the text: ", ...rawTextData.value);
              return rawTextData.value;
            } else {
              return null;
            }
            }).catch(error => {
            console.log('Error:', error);
            }); 
      return rawTextData.value;
};

async function doCloseModal(){
  // document.getElementById("jumbotron").style.display = "flex";
  let main = document.getElementById("main");
  let headerDiv = document.getElementById("headerDiv");
  // if(main){
  //   main.style.top = "72px";
  // }
  if(headerDiv){
    headerDiv.style.visibility = "visible";
  }
  open.value = false;

  // we don't want this here but can use to test->
  // openFull.value = true; 
}

async function doCloseFullModal(){
    openFull.value = false;
    openGraph.value = true;
};

async function doOpenFullModal(){
  openFull.value = true;
};

async function doOpenAwaitScrape(){
  console.log("in do open await scrape");
  openFull.value = true;
};

function scrapeAnotherUrl(url : String){
  console.log("hit scrape another url...")
  return scrape_text(url);
};



</script>


<template #heading>

<Modal 
  :open="open" 
  :openFull="openFull" 
  @openedfullawaitscrape="doOpenAwaitScrape" 
  @openedfull="doOpenFullModal" 
  @closedfull="doCloseFullModal" 
  @closedmodal="doCloseModal" 

  :tocdata="tocData" 
  :rawtextdata="rawTextData" 
  :selectedTitle="selectedTitle" 
  :selectedAuthor="selectedAuthor" 
/>
  <!-- set up a scroll here to show as many as we need -->
  <div id="searchTextWrapper" v-if="props.items" v-for="item in (props.items)" :key="item.title">
    <div id="bookSearchMainWrapper">

      <img class="author-image" :id="`authorImage_${item.id}`" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Blank_woman_placeholder.svg"/>
      

      <div id="bookSearchMainInfoWrapper">
        <h3 class="book-title">
          {{ item ? item.title : null}}
        </h3>
        <div id="search-bottom-wrapper" class="book-items">
          <h4 class="book-author">
            {{ item ? item.author : null}}
          </h4> 
          <p class="book-item">
            Pub. {{ item ? moment(item.published).format('YYYY')  : null}}
          </p>
        </div>
      </div>
 
      <div id="bookSearchMainButtonsWrapper">
        <button v-on:click="open = true,show_TOC(item.title_url, item.title, item.author)" class="book-item button">Contents</button>
        <button v-on:click="open = true,scrape_text(item.title_url)" class="book-item button">Full Text</button>
      </div>
    </div>
    
      

  </div>

</template> 

<style>

.author-image {
  max-height: 320px;
  width: 180px;
  object-fit: cover;
  align-items: center;
  justify-content: center;
  min-width: 164px;
  min-height:200px;
}
.book-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 0.2rem;
  color: var(--color-heading);
  padding-top: 8px;
  height:90%;
  overflow-y:scroll;
  padding:2%;
}
.book-author {
  font-size: 1rem;
  font-weight: 300;
  margin-bottom: 0.1rem;
  color: var(--color-text);
  width: 100%;
  line-height: 1.5;
  padding-left: 2%;
}
.search-bottom-wrapper{
  max-height:32px;
}
.book-items {
  font-size: 0.8rem;
  font-weight: 100;
  color: hsla(160, 100%, 37%, 1);
  display: flex;
  flex-direction: row;

}
.book-item {
  width: 50%;
  color: rgba(255,255,255,0.94);
  line-height:1.8;
}
.book-item.button {
  display: flex;
  justify-content: center;
  width: 100%;
  color: hsla(160, 100%, 37%, 1);
  background-color: var(--color-background-mute);
  min-height: 40px;
  flex-direction: column;
  /* top: 10%; */
  margin: 0;
  font-weight: 100;
  font-size: 14px;
  min-width: 100px;
  align-items: center;
  border: black;
  margin: 4px;
  border-radius: 8px;
}

#bookSearchMainWrapper {
  display:flex;
  flex-direction:row;
  border-bottom: solid 1px var(--color-text);
  font-weight: 100;
  padding-right:2%;
  max-height:260px;
}
#bookSearchMainInfoWrapper {
  display:flex;
  flex-direction:column;
  width: 100%;
}
#bookSearchMainButtonsWrapper {
  display:flex;
  flex-direction:column;
  width:40%;
  padding-top:2%;
  padding-right: 2%;
}

</style>