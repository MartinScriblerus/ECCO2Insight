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
const ready : any = ref(false);
// const modalFull : any = ref(null);
// const modal : any = ref(Modal);

// if(props.items){


// }

const emit = defineEmits(["getWikiURL", "getImages", "in_toc_now"])

async function show_TOC(url:String, title:String, author:String){
  emit("in_toc_now");

//spinner
  let mainDiv : any = document.getElementById("main")
  if(mainDiv){
    mainDiv.style.opacity = 0.2;
  }
  selectedTitle.value = title;
  selectedAuthor.value = author;

  let jumbotron = document.getElementById("jumbotron");
  if(jumbotron){
    jumbotron.style.display = "none";
  }
  let main = document.getElementById("main")
  if(main){
    main.style.top = "0px";
  }
  
  
  // let searchForms = document.getElementById("headerDiv");
  // if(searchForms){
  //   searchForms.style.visibility = "hidden";
  // }
  tocData.value = await fetch('http://localhost:5000/scraper_get_toc', {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    method: "POST",
    body: JSON.stringify({title: title, author: author, titleUrl: url})
  }).then((x:any)=>{

    if(openFull.value === true){

      return Promise.all([])
    } else {
      return x;
    }
  }).then(response => response.json()).then(result => {

    if(result.length){
      tocData.value = result;
      return tocData.value;
    } else {
      return null;
    }
    }).catch(error => {
      // console.log('Error:', error);
    }); 
    //console.log("here's the table of contents: ", tocData.value);
    
    return tocData.value;
};

async function scrape_text(url:String){ 

    let wrapperTitle = document.getElementById("buttonsWrapperTitle");
    let wrapperSubtitle = document.getElementById("buttonsWrapperSubtitle");
    let wrapperBtns = document.getElementById("buttonsInnerWrapper");
    if(wrapperTitle){
      wrapperTitle.style.display = "inline-block";
    } else {
      //console.log("wrapper title missing");
    }
    if(wrapperSubtitle){
      wrapperSubtitle.style.display = "inline-block";
    } else {
      //console.log("wrapper subtitle missing");
    }
    if(wrapperBtns){
      wrapperBtns.style.display = "inline-block";
    } else {
      //console.log("wrapper btns missing");
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
            // console.log('Error:', error);
            }); 
      return rawTextData.value;
};

async function doCloseModal(){

  // document.getElementById("jumbotron").style.display = "flex";
  let main : any = document.getElementById("main");
  let headerDiv : any = document.getElementById("headerDiv");
  if(main){
    main.style.opacity = 1;
  }
  if(headerDiv){
    headerDiv.style.visibility = "visible";
  }
  open.value = false;

  // we don't want this here but can use to test->
  openFull.value = false; 
}

async function doCloseFullModal(){

    openFull.value = false;
   
    openGraph.value = true;
        
    ready.value = JSON.parse(JSON.stringify(openFull.value));
    return ready.value;
};

async function doOpenFullModal(){

  console.log("hit open full modal")
  // openFull.value = true;
};

async function gotLocalStorageText(url){
  let searchFields = document.getElementById("searchFields");
  if(searchFields){
    searchFields.style.display = "none";
  }
  
  openGraph.value = true;
  setTimeout(()=>{return ready.value = true},1000)
  
}

async function doOpenAwaitScrape(){
  let searchFields = document.getElementById("searchFields");
  if(searchFields){
    searchFields.style.display = "none";
  }
  openFull.value = true;
};

function scrapeAnotherUrl(url : String){
  return scrape_text(url);
};

// let propsItemsTemp :any = props.items || [];
// let propsItems = propsItemsTemp.map(i=>i) || [];
</script>


<template #heading>

<Modal 
  :open="open" 
  :openFull="openFull" 
 
  @openedfullawaitscrape="doOpenAwaitScrape" 
  @openedfull="doOpenFullModal" 
  @closedfull="doCloseFullModal" 
  @closedmodal="doCloseModal" 
  @closemodalgotlocal="gotLocalStorageText"
  :tocdata="tocData" 
  :rawtextdata="rawTextData" 
  :selectedTitle="selectedTitle" 
  :selectedAuthor="selectedAuthor" 
/>
  <!-- set up a scroll here to show as many as we need -->
  <div class="searchTextWrapper" v-if="props.items" v-for="item in (props.items)" :key="item.title" >
    <div class="bookSearchMainWrapper">

      <img class="author-image" :id="`authorImage_${item.id}`" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Blank_woman_placeholder.svg"/>
      

      <div class="bookSearchMainInfoWrapper">
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
        <button disabled id="fulltextSearch" v-on:click="open = true,scrape_text(item.title_url)" class="book-item button">Full Text</button>
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
  overflow-y:hidden;
  padding:2%;
  padding-left: 2%;
  padding-top: 2%;
  padding-right: 8%;
}
.book-author {
  font-size: 1.3rem;
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
  color: #E6CECA;
  display: flex;
  flex-direction: row;

}
.book-item {
  width: 34%;
  color: rgba(255,255,255,0.94);
  line-height: 1.8;
  font-size: 18px;
  font-weight: 100;
  top: 1px;
}
.book-item.button {
  display: flex;
  justify-content: center;
  width: 100%;
 
  background-color: var(--color-background-mute);
  min-height: 40px;
  flex-direction: column;
  /* top: 10%; */
  margin: 0px;
  font-weight: 300;
  font-size: 16px;
  min-width: 100px;
  align-items: center;
  border: black;
  margin: 4px;
  border-radius: 8px;
}

#fulltextSearch {
  pointer-events: none;
  opacity:0.5;
}

.bookSearchMainWrapper {
  display:flex;
  flex-direction:row;
  border-bottom: solid 1px var(--color-text);
  font-weight: 100;
  padding-right:2%;
  max-height:260px;

}
.bookSearchMainInfoWrapper {
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