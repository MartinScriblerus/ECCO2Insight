<script setup>
import { ref, watch, onMounted } from 'vue'
import { SelfBuildingSquareSpinner } from 'epic-spinners'
import StepProgress from 'vue-step-progress';
import './untitled-font-1.svg'

import 'vue-step-progress/dist/main.css';
import { Head } from '@vueuse/head';

import GraphModal from './GraphModal.vue';
import ColorInput from 'vue-color-input';
import Multiselect from '@vueform/multiselect'

// Define Props, Emits & Key Variables
// ----------------------------------------------------

const emit = defineEmits(["closemodalgotlocal","closedmodal","openedfullawaitscrape","openedfull","closedfull"]);

const props = defineProps({
  open: Boolean,
  openFull: Boolean,
  tocdata: Object,
  rawtextdata: String,
  selectedTitle: String,
  selectedAuthor: String,
  // inGraphsParent:Boolean
  // graphstate: String
});

const currentTextData = ref([]);
const selectedRow = ref(0);
const selectedXAxisRef = ref(0);
const selectedYAxisRef = ref(0);
const xIsIndexAxis = ref(true);
const yIsIndexAxis = ref(false);
const yAxisFramingLast = ref(false);

const inGraphs = ref(false);
const secondTextRef = ref();
secondTextRef.value = false;
const displayedSummary = ref('');
const displayedRhymes = ref([])
const graphstateRef = ref(0);
const axisColorMatchBool = ref(false);
const noLateUpdateAfterNLTK = ref(false);
const initialHumanReadableTextRef = ref({
  title: String,
  author: String,
  textId: Number,
  // europeanaEntityObj: {
  //   europeanaEntityId: Number,
  //   prefLabel: String,
  //   altLabels: Array,
  //   dateOfBirth: Date,
  //   dateOfDeath: Date,
  //   isShownBy: {
  //     id: String,
  //     source: String
  //   }
  // },
  // mostCommonWords: Array,
  textObj: {
    titleUrl: String,
    summary: String,
    averageLinesPerSentence: Number,
    percPoetrySyllables: Number,
    percPoetryRhymes: Number,
    spacyEntities: Array,
    // europeanaEntitiesArray: Array,
    placesEntitiesArray: Array,
    mostCommonWords: Array,

  },

  lineObj: {
    lineId: {
      lastWord: String,
      poeticForm: String,
      thisRhyme: String,
      lastRhyme: String,
      thisLine: String,
      lastLine: String,
      thisInterRhyme: String,
      lastInterRhyme: String,
      thisInterLine: String,
      lastInterLine: String,
      internalRhymes: Object,
      syllablesInLine: Number
    }
  },

  sentenceObj: {

  },
  linesArray: Array,
})

initialHumanReadableTextRef.value.textObj.mostCommonWords = [];

const currentStepRef = ref(null);
const mySteps = ['Text', 'Lines', 'Sentences', "Training"]
let stepMessage = '';
let searchModal;
const preservedDataLine1 = ref({});
onMounted(()=>{
  currentStepRef.value = 0;
  setTimeout(() => {
    searchModal = modal.value;
  }, 1);
  clearTimeout();
   
  const css = `
  @charset "UTF-8";
  @font-face {
    font-family: "untitled-font-1";
    src: url("untitled-font-1.svg#untitled-font-1") format("svg");
    font-weight: normal;
    font-style: normal;
    z-index: 10;
  }

  @font-face {
    font-family: 'Font Awesome 5 Free';
    font-style: normal;
    font-weight: 400;
    font-display: block;
    src: 'url(https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/webfonts/fa-brands-400.eot)';
    src: 'url(https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/webfonts/fa-brands-400.eot?#iefix) format("embedded-opentype"), url(https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/webfonts/fa-brands-400.woff2) format("woff2"), url(https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/webfonts/fa-brands-400.woff) format("woff"), url(https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/webfonts/fa-brands-400.ttf) format("truetype"), url(https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/webfonts/fa-brands-400.svg#fontawesome) format("svg")'
  }
  `
})

const connectedSocket = ref(false)
connectedSocket.value = false;
// // Initial soocket implementation 
// // ----------------------------------------------------
// Initial soocket implementation 
// ----------------------------------------------------
const socket = new WebSocket('ws://localhost:5000/ws');
function startSocket(){
  // const socket = new WebSocket('ws://localhost:5000/ws');
  // console.log('do we have a socket? ', socket);
  connectedSocket.value = true;
  socket.onopen = function (event) {
    console.log('****** Welcome to TCP Data Viz! ******');
    socket.send("Here's some text that the server is urgently awaiting!");
    // console.log('still going after opening salvo');
  }
  socket.onclose = function(event) {
      console.log("socket close: ", event);
      // need more thorough handling here to 
      // account for UI changes / DOM clashes
      // setTimeout(()=>{
      //   startSocket();
      // },2000);
      clearTimeout();
  }

  window.onbeforeunload = function() {
      console.log('close socket before exiting');
      socket.onclose = function () {}; // disable onclose handler first
      socket.close();
  };

// Text loading steps
// TODO => sort out which we need for initial text loading
// TODO => get these callback numbers in proper 1-2-3 order
// const mySteps = ['Text', 'Lines', 'Sentences', "Training"]
// let stepMessage = '';

const getCommonWordsExplanation = ref(false)

socket.onmessage = event => {

    // console.log("do we GET SOCKET MSGS!!@!!??? ", event.data);
    if(event.data === 'third_msg'){
      // console.log("got third socket msg");
      console.log("T");
      if(document.getElementById("modalFull") && document.getElementById("modalFull").style.display === "none"){
        document.getElementById("modalFull").style.display = "flex"
      }
      currentStepRef.value = 0;
      stepMessage = "Gathering text and preprocessing data"
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    }
    else if(event.data === 'fourth_msg'){
      // console.log("got fourth socket msg");
      // let dataPreviewDiv = document.getElementById("dataPreviewWrapper");
      // if(dataPreviewDiv){
      //   dataPreviewDiv.style.background = "#e6e4d6";
      // }
      console.log("C");
      currentStepRef.value = 1;
      stepMessage = "Line-level and poetic analysis";
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    }
    else if(event.data === 'eighth_msg'){
      currentStepRef.value = 2;
      stepMessage = "Sentence-level analysis"
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    }
    else if(event.data === 'eleventh_msg'){
      currentStepRef.value = 3;
      stepMessage = "Training"
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    } 
    else if(event.data === 'fifteenth_msg'){
      currentStepRef.value = 3;
      // console.log("HIT FIFTEENTH!");
      console.log("P");
      inGraphs.value = true;
      
      stepMessage = "Feature Extraction"
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    
      // We've got the text -> reorder the DOM
      // ----------------------------------------------------
      let results = document.getElementsByClassName('modal-single-text-results');
      console.log("results length= ", results.length)
      if(results.length > 0){
        // results[0].style.visibility = "visible";
        // inGraphs.value = true;
        try{
          if(document.getElementById('modal-textAnalysis-title')){
            document.getElementById('modal-textAnalysis-title').style.display = "none";
          }
          if(document.getElementById('progressCircles')){
            document.getElementById('progressCircles').style.display = "none";
          } else {
            // console.log("no prog circs");
          }
          if(document.getElementById('progressMsg')){
            document.getElementById('progressMsg').style.display = "none";
          } else {
            // console.log("no progress msgs");
          }
          if(document.getElementById('progressMsgExplanation')){
            document.getElementById('progressMsgExplanation').style.display = "none";
          } else {
            console.log("no prog explanations");
          }
          if(document.getElementById('main')){
            document.getElementById('main').style.display = "none";
          } else {
            console.log("no main");
          } 
          
          if(document.getElementById('graphs')){
            document.getElementById('graphs').style.display = "flex";
          } else {
            console.log("do we hit this 1?");
            inGraphs.value = true;
            //console.log("no graphs");
          }
          if(document.getElementById('progressMsgExplanation')){
            document.getElementById('progressMsgExplanation').style.display = "none";
          } else {
            console.log("no prog explanation");
          }
        
          try {
            if(document.getElementById('compareButton')){
              document.getElementById('compareButton').style.visibility = "visible";
            } else {
              console.log("no compare button...")
            }
            if(document.getElementById("textRowAuthor")){
              document.getElementById("textRowAuthor").style.display = "none";
            } else {
              console.log("no text row author");
            }
            if(document.getElementById("textRowTitle")){
              document.getElementById("textRowTitle").style.display = "none";
            } else {
              console.log("no text row title");
            }
            // document.getElementsByClassName("searchTextWrapper").style.display = "none";
            if(document.getElementById('headerDiv')){
              document.getElementById('headerDiv').style.display = 'none';
            } else {
              console.log("no header div...");
            }
            if(document.getElementById('headerDiv')){
              document.getElementById('headerDiv').style.visibility = 'hidden';
            } else {
              console.log("no header div... ");
            }
            if(document.getElementById('mainText')){
              document.getElementById('mainText').style.display = "none";
            } else {
              console.log("no main text");
            }
            // document.getElementById('mainTextSubheader').style.display = "none";
          } 
          catch(e){
           console.log("err_modal1 ", e);
          }
        } catch(e){
          console.log("err_modal1 outer", e);
        }
      }
    }  
    else if(event.data === "explain_tokens_and_lemmas"){
      let dataPreviewDiv = document.getElementById("dataPreviewWrapper");
      if(dataPreviewDiv){
        dataPreviewDiv.style.background = "#e6e4d6";
      }
      if(document.getElementById("progressMsgExplanationText")){
        document.getElementById("progressMsgExplanationText").innerText = "Splitting text into tokens and grouping the base forms of word variants";
      }
    } 
    else if(event.data === "explain_common_words"){ 
      if(document.getElementById("progressMsgExplanationText")){
        document.getElementById("progressMsgExplanationText").innerText = "Identifying most common words in the text";
      }
    } 
    // else if(event.data === "explain_poetry_intro"){
    //   if(document.getElementById("progressMsgExplanationText")){
    //     document.getElementById("progressMsgExplanationText").innerText = "Splitting text into lines and isolating poetic features";
    //   }
    // } 
    else if(event.data === "explain_last_words_per_line"){
      if(document.getElementById("progressMsgExplanationText")){
        document.getElementById("progressMsgExplanationText").innerText = "Checking for internal and end rhymes";
      }
    } 
    else if(event.data === "explain_internal_rhymes"){
      if(document.getElementById("progressMsgExplanationText")){
        document.getElementById("progressMsgExplanationText").innerText = "Checking internal rhymes here";
      }
    }
    else if(event.data === "explain_grammar"){
      if(document.getElementById("progressMsgExplanationText")){
        document.getElementById("progressMsgExplanationText").innerText = "Checking internal rhymes here";
      }
    }
    else if(event.data === "explain_entity_analysis"){
      if(document.getElementById("progressMsgExplanationText")){
        document.getElementById("progressMsgExplanationText").innerText = "Identifying entities and mapping grammar";
      }
    } 
    else if(event.data === "explain_sentiment_analysis"){
      if(document.getElementById("progressMsgExplanationText")){
        document.getElementById("progressMsgExplanationText").innerText = "Quantifying sentiment of each sentence on -1 to 1 scale";
      }
    } 
    else if(event.data === "explain_sentence_summary"){
      if(document.getElementById("progressMsgExplanationText")){
        document.getElementById("progressMsgExplanationText").innerText = "Using word frequencies to generate a summary of the text";
      }
    }
    else if(event.data === "explain_vectorized_vocab"){
      if(document.getElementById("progressMsgExplanationText")){
        document.getElementById("progressMsgExplanationText").innerText = "Here we should explain vectorized vocabulary!";
      }
    }
    else if(event.data === "explain_tfidf"){
      getCommonWordsExplanation.value = true;
      if(document.getElementById("progressMsgExplanationText")){
        document.getElementById("progressMsgExplanationText").innerText = "Converting words into numerical vectors";
      }
    }
    else if(event.data === "explain_euclidean_distance"){
      if(document.getElementById("progressMsgExplanationText")){
        document.getElementById("progressMsgExplanationText").innerText = "Plotting similarity distances";
      }
    }
    else if(event.data === "explain_progressive_feature_selection"){
      if(document.getElementById("progressMsgExplanationText")){
        document.getElementById("progressMsgExplanationText").innerText = "Unsupervised machine learning";
      }
    }
    else if(event.data.indexOf("SUMMARY_") !== -1){
      let holder = event.data
    
      let slicedHolder = (holder.split("_").slice(1)).toString();
      console.log("Generated Summary: ", holder)
      displayedSummary.value = slicedHolder;
      if(document.getElementById("progressMsgDataSummaryPreview")){
        document.getElementById("progressMsgDataSummaryPreview").innerHTML = slicedHolder;
      } 
    }
    else if(event.data.indexOf("RHYME_") !== -1){
      let holder = event.data;
      //console.log("RHYME HOLDER!!! ", holder);
      let holderIndex = holder.indexOf("RHYME_");
      let slicedHolder = holder.slice("RHYME_");
      singleRhymeArr = slicedHolder.split["_"]


    }
    else {
        if(document.getElementById("progressMsgDataPreview")){
          document.getElementById("progressMsgDataPreview").innerText = event.data;
        }
      }
    } 

}
window.onbeforeunload = function() {
      console.log('close socket before exiting');
      socket.onclose = function () {}; // disable onclose handler first
      socket.close();
  };

startSocket();



// these are options for the keybuilder dropdown
// ----------------------------------------------------
const optionsX = ref([]);

// these are values for axis labels
const valueX = ref('');
// valueX.value = "count_x";
// these are numbers for axes values
const numberXMax = ref([]);
const numberXMin = ref([]);
const numberYMax = ref([]);
const numberYMin = ref([]);
numberXMax.value = [];
numberXMin.value = [];
numberYMax.value = [];
numberYMin.value = [];
function updateReadOnlyXMax(v){
  numberXMax.value.push(v);
  numberXMax.value.filter(i=>i);
};
function updateReadOnlyXMin(v){
  numberXMin.value.push(v);
  numberXMin.value.filter(i=>i);
};
function updateReadOnlyYMax(v){
  numberYMax.value.push(v);
  numberYMax.value.filter(i=>i);
};
function updateReadOnlyYMin(v){
  numberXMin.value.push(v);
  numberXMin.filter(i=>i);
};
// do the same for Y axis
const optionsY = ref([]);
const valueY = ref('');
// valueY.value = "count_y";
const graphReady = ref(false);
graphReady.value = document.getElementById("graphs");

// console.log()
optionsX.value = []
optionsY.value = []

//Initial colors for lines and axes
const color0 = ref("");
color0.value = "#e6e4d6";

const color1 = ref("");
color1.value = "#9ea5e9";

const color2 = ref("");
color2.value = "#00bd7e";

const color3 = ref("");
color3.value = "#00bd7e";

const colorX = ref("");
colorX.value = "#ffffff";

const colorY = ref("");
colorY.value = "#ffffff";

const ready = ref(false);

// TODO -> need a less hard-coded implementation of keybuilder UI   
// TODO -> check if this (or other implementation below) can be removed
const showOne = ref(false);
const showTwo = ref(false);
const showThree = ref(false);
const showFour = ref(false);

const temp = ref({})
const rawtextfromtoc= ref({});

// Create fullscreen modal for scrape process / graph display
// ----------------------------------------------------
const modalFull = ref(null);
const modal = ref(null);
// graphstate = 'singleText';
const currentLinesCount = ref(0); 
const additionalTexts = ref([]);
currentLinesCount.value = 1;



async function trySetReady(){
  
  let test = await modalFull.value;
  // console.log("TEST!!! ", test);
  
  if(test && JSON.parse(JSON.stringify(props.openFull)) ){
    //console.log("WEE SHD MAKE IT HERE ON TEXT 2")
      inGraphs.value = false;
      secondTextRef.value = true;
      ready.value = true;
      if(JSON.parse(JSON.stringify(props.openFull))){
        document.getElementById("modalFull").style.display = "flex";
      }
      //ready.value = JSON.parse(JSON.stringify(props.openFull));
      //console.log("what is props openfull? ", JSON.parse(JSON.stringify(props.openFull)));
    } else {
      //console.log("AHA! are we reaching here???????????");
      let test = await modalFull.value;
      inGraphs.value = false;
      try {
        let searchFields = document.getElementById("searchFields");
        if(searchFields && secondTextRef.value !== true){
          searchFields.style.visibility = "hidden";
          //searchFields.style.display = "flex";
        } else if(searchFields && secondTextRef.value === true){
          secondTextRef.value = false;
        } else {

        }
        let headerDiv = document.getElementById("headerDiv");
        if(headerDiv){
          headerDiv.style.visibility = "visible";
        }
        if(document.getElementById("modalFull")){
          //document.getElementById("modalFull").style.display = "none"
        }
      } catch(e){

      }

      // ready.value = JSON.parse(JSON.stringify(props.openFull));
      // if(!test){
      //   trySetReady();
      // }
    }
}
additionalTexts.value = [
  {
    title:'',
    author:'',
    titleUrl:'',
    variableX: "",
    variableY: ""
  },
  {
    title:"",
    author:"",
    titleUrl: "",
    variableX: "",
    variableY: ""
  },
  
]
watch(() => [graphstateRef, 
inGraphs,
additionalTexts, 
color0, 
color1, 
color2, 
color3, 
colorX, 
colorY, 
optionsX, 
valueX,
valueY,
optionsY, 
numberXMax,
numberXMin, 
numberYMax,
numberYMin,
props.selected, 
currentLinesCount, 
currentTextData,
axisColorMatchBool,
selectedXAxisRef,
selectedYAxisRef,
props.inGraphsParent,
props.openFull,
yAxisFramingLast,
preservedDataLine1],(graphstateRef,inGraphs,rawtextdata,selectedTitle,selectedAuthor) => {

  // if(JSON.parse(JSON.stringify(props.inGraphsParent)) === true && inGraphs.value === false){
  //   inGraphs.value = true;
  // }

    trySetReady();
    if(JSON.parse(JSON.stringify(props.openFull)) !== true){
      return;
    }
    //console.log("ARE WE IN GRAPHS??? ", inGraphs.value);
      if(!JSON.parse(JSON.stringify(props.selectedAuthor)) || !JSON.parse(JSON.stringify(props.selectedTitle))){
        console.log("we are missing props selected author or props selected title")
        return;
      }
      if(currentLinesCount.value === 1 && inGraphs.value === true){
        showOne.value = true;
       // console.log("WHAT ARE ADDITIONAL TEXTS>> ", additionalTexts);
        additionalTexts[0].author = JSON.parse(JSON.stringify(props.selectedAuthor));
        additionalTexts[0].title = JSON.parse(JSON.stringify(props.selectedTitle));
       // console.log("SELEECTED X AXIS REF: ", selectedXAxisRef.value);
      } else if (currentLinesCount.value === 2 && inGraphs.value === true){
        additionalTexts[1].author = JSON.parse(JSON.stringify(props.selectedAuthor));
        additionalTexts[1].title = JSON.parse(JSON.stringify(props.selectedTitle));
       // console.log("GOT THIS! ", additionalTexts[1]);
        showTwo.value = true;
        showThree.value = false;
      }
        //else if (currentLinesCount.value === 3){
      //   showThree.value = true;
      //   showFour.value = false;
      // } else if (currentLinesCount.value === 4){
      //   showFour.value = true;
      // } 
      else {
        // console.log("how did we arrive in current count else? ", currentLinesCount.value);
      } 
    });

// Begin process for adding a new text...
// ----------------------------------------------------
function tryAddNewText(){
  let moveableGrammarWrapper = document.getElementById("grammarDisplayWrapper");
      if(moveableGrammarWrapper){
        moveableGrammarWrapper.style.display = 'none';
      }
  let modalHead = document.getElementById("modalHead");
      if(modalHead){
        modalHead.style.display = 'none';
      }
  inGraphs.value = false;
  let searchArea = document.getElementById("searchFields");
  if(searchArea){
    searchArea.style.visibility="visible";
    searchFields.style.display = "flex";
  }
  let headerDiv = document.getElementById("headerDiv");
  if(headerDiv){
    headerDiv.style.visibility = "visible";
  }
  if(document.getElementById("modalFull")){
    document.getElementById("modalFull").classList.remove("receivedSingleTextData");
    document.getElementById("modalFull").style.display = "none"
  }
  inGraphs.value = false;
  secondTextRef.value = true;
  // noLateUpdateAfterNLTK.value = false;
  doCloseFullModalChild();
  
  
 // console.log("second text is ... ", secondTextRef.value);

}

// Opens Keybuilder Popup
// ----------------------------------------------------
function openKeyPopup(){
  let linepicker = document.getElementById("linePickerPopup");
  if(linepicker){
    linepicker.style.display = "inline-block";
  }
  let newTextPopup = document.getElementById("newTextPopup")
  
  if(newTextPopup ){
    newTextPopup.style.display = "flex";
    resetRows();
  }
}


// Closes Keybuilder Popup
// ----------------------------------------------------
function closeKeyModal () {
  let popup = document.getElementById("newTextPopup");
  if(popup){
    //console.log("closed the key modal");
    popup.style.display = "none";
  }
  let linepicker = document.getElementById("linePickerPopup");
  if(linepicker){
    linepicker.style.display = "none";
  }
}

// Reset row count if # of lines changes 
// ----------------------------------------------------
async function resetRows(){
  //document.getElementById("newTextPopup").style.display = "flex";
  // const open = await openUpdatePopup()


  //document.getElementById("newTextPopup").style.display = "flex";

  if(currentLinesCount.value === 4){
    let row4 = document.getElementById("newRow_3");
    if(row4){
      row4.style.display = "flex";
    } else {
      row4.style.display = "none";
      // console.log("what is row 4 ", document.getElementById("newRow_3"));
    }
    
  }
  if(currentLinesCount.value >= 3){
    let row3 = document.getElementById("newRow_2");
    if(row3){
      row3.style.display = "flex";
    } else {
      row3.style.display = "none";
      // console.log("what is row 3 ", document.getElementById("newRow_2"));
    }
  }
  if(currentLinesCount.value >= 2){
    let row2 = document.getElementById("newRow_1");
    if(row2 && inGraphs.value === true){
      
      row2.style.display = "flex";
      console.log("reaching heree!!!");
      if(!props.selectedAuthor || !props.selectedTitle){
        console.log(`either missing selected author ${props.selectedAuthor} or props selected title ${props.selectedTitle}`)
      }
      additionalTexts.value[1].author = props.selectedAuthor;
      additionalTexts.value[1].title = props.selectedTitle;
    } else {
      //row2.style.display = "none";
      // console.log("what is row 2 ", document.getElementById("newRow_1"));
    }
  }
}

// Remove line from Keybuilder 
// TODO=> carry implementation down into actual graph
// ----------------------------------------------------
function removeLine(){
  if(currentLinesCount.value > 1){
    currentLinesCount.value = currentLinesCount.value - 1;
    resetRows();
    let rowToHide = document.querySelector(`.new-text-popup-row#newRow_${currentLinesCount.value}`);
      if(rowToHide){
        rowToHide.style.display = "none";
      }
  }
}

// This linecount is the official tracking number...
// TODO => find a more performant and robust solution
// ----------------------------------------------------
function setLineCount(){
  frameLast();
  inGraphs.value = false;
  // // colorInputMountedHandler();
  // document.getElementById("addTextButton").click();
  tryAddNewText();
  // TODO=> rename or rework this variable to accomodate new flow
  graphstateRef.value = graphstateRef.value + 1;
  

  if(currentLinesCount.value < 5){
    //console.log("adding a keybuilder row / graph line here: ", currentLinesCount.value);
    // document.getElementById("addLineButton").disabled = false;
    let popup = document.getElementById("newTextPopup");
    if(popup){
      popup.style.top = `${0 - ((currentLinesCount.value) * 2)}%`;
    }
    currentLinesCount.value = currentLinesCount.value + 1;
    // if(inGraphs.value === true){
      resetRows();
    // } else {
    //   console.log("can't reset rows until in graphs... ")
    // }


  } else {
    // TODO fix this disabling of button
    // document.getElementById("addLineButton").disabled = true;
  }
  //console.log("hit comparative: ", graphstateRef.value);
}


async function tryGetFullModal(url){
      let fullModal = await modalFull.value !== null;
      let mainPage = document.getElementById("main");
      mainPage.style.opacity = 0;
          mainPage.style.visibility = "hidden";
      if(inGraphs.value === true){
        inGraphs.value = false;
        trySetReady();
      }
      console.log()
      if(fullModal && fullModal.classList){
        fullModal.classList.add("awaiting");
        
      } else {
        // console.log("hit the else");
      }
      // setTimeout(()=>{
      //   if(mainPage){
      //     mainPage.style.opacity = 0;
      //     mainPage.style.visibility = "hidden";
      //   }
      // },10)
      // clearTimeout();
     
      //console.log("URL IS! ", url);

      rawtextfromtoc.value = await fetch('http://localhost:5000/scraper_get_text', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({titleUrl: url})
      }).then(response => response.json()).then(result => {
          if(result){
            // console.log("hey, got a response from server!");
            let modalHeader = document.getElementById("modalHead");
            if(modalHeader){
              modalHeader.style.display = "flex";
            }
            rawtextfromtoc.value = result;
            console.log("hhhere's the text: ", JSON.parse(JSON.stringify(rawtextfromtoc.value)));
            
            // try{
            //   let stressesArr = [];
            //   let words = JSON.parse(JSON.stringify(rawtextfromtoc.value)).poetic_form.map(i=>i)
            //   console.log("WORDS? ", words);
            //   stressesArr.push(window.RiTa.stresses(words))
            //   console.log("STRESSES ARR: ", stressesArr);
            // } catch(e){
            //   console.log("err: ", e);
            // }
            //document.getElementById("modalFull").classList.add("awaiting")
            temp.value = JSON.parse(JSON.stringify(rawtextfromtoc.value));
            ///////////////////////////////////////////////////////////////////////////////
            // --> Catch Data in Complex Object (break this all up in future for better user exp)
            initialHumanReadableTextRef.value.title = props.selectedTitle;
            initialHumanReadableTextRef.value.author = props.selectedAuthor;
            // TODO:
            initialHumanReadableTextRef.value.textId = 0; 
            initialHumanReadableTextRef.value.textObj.summary = temp.value.summary
            initialHumanReadableTextRef.value.textObj.titleUrl = temp.value.title_url;
            initialHumanReadableTextRef.value.textObj.averageLinesPerSentence = temp.value.avg_tokens_sentence;
            initialHumanReadableTextRef.value.textObj.percPoetrySyllables = temp.value.perc_poetry_syllables;
            initialHumanReadableTextRef.value.textObj.percPoetryRhymes = temp.value.perc_poetry_rhymes;
            initialHumanReadableTextRef.value.textObj.placesEntitiesArray = temp.value.places;
          //   temp.value.last_word_per_line.forEach((li,lineIndex)=>{
          //     console.log("in line index loooooop 1");
          //     initialHumanReadableTextRef.value.lineObj[JSON.parse(JSON.stringify(lineIndex))] = {};
          //     initialHumanReadableTextRef.value.lineObj[JSON.parse(JSON.stringify(lineIndex))]['lastWord'] = li;
          //     // temp.value.poetic_form.forEach(form=>{
          //     //   console.log("in poetic form index loooooop 1");
          //     //   if(form['index'] === lineIndex){
          //     //     initialHumanReadableTextRef.value.lineObj[lineIndex] = {};
          //     //   }
          //     // })
              
       
          // })
          initialHumanReadableTextRef.value['poetic_form'] = [];
          console.log("TEMP VAL POETIC FORM CHECK: ", temp.value.poetic_form.length)
          initialHumanReadableTextRef.value['poetic_form'].push(temp.value.poetic_form)
          // temp.value.poetic_form.forEach(pf=>{
          //       console.log("in poetic form loop 2");
          //       try {
          //         if(JSON.parse(JSON.stringify(pf))['index'] === JSON.parse(JSON.stringify(lineIndex))){
          //           initialHumanReadableTextRef.value.lineObj[JSON.parse(JSON.stringify(lineIndex))] = {
          //             "thisRhyme": JSON.parse(JSON.stringify(pf))['this_rhyme'] || '',
          //             "lastRhyme": JSON.parse(JSON.stringify(pf))['last_rhyme'] || '',
          //             "thisLine": JSON.parse(JSON.stringify(pf))['this_line'] || '',
          //             "lastLine": JSON.parse(JSON.stringify(pf))['last_line'] || '',
          //             "thisInterRhyme": JSON.parse(JSON.stringify(pf))['this_interrhyme'] || '',
          //             "lastInterRhyme": JSON.parse(JSON.stringify(pf))['last_interrhyme'] || '',
          //             "thisInterLine": JSON.parse(JSON.stringify(pf))['this_interline'] || '',
          //             "lastInterLine": JSON.parse(JSON.stringify(pf))['last_interline'] || '',
          //             "poeticForm": JSON.parse(JSON.stringify(pf))['form'] || 'None' 
          //           }
          //         }
          //       } catch(e){
          //         // console.log("ARE WEE IN GRAPHS? ", inGraphs.value)
          //         // console.log("IS FULL MODAL OUT? ", modalFull.value)
          //       }
          //     })
          initialHumanReadableTextRef.value['internal_rhymes_most_recent'] = [];
          console.log("check on internal rhymes length ", temp.value.internal_rhyme_most_recent.length)
          initialHumanReadableTextRef.value['internal_rhymes_most_recent'].push(temp.value.internal_rhyme_most_recent)
              // temp.value.internal_rhyme_most_recent.forEach(ry=>{
              //   console.log("in internal rhyme most recent");
              //   try {
              //     if(JSON.parse(JSON.stringify(ry))['index'] === JSON.parse(JSON.stringify(lineIndex))){
              //       try {
              //           initialHumanReadableTextRef.value.lineObj[JSON.parse(JSON.stringify(lineIndex))]['internalRhymes'] = {
              //             "endRhyme": JSON.parse(JSON.stringify(ry))['end_rhyme'] || '',
              //             "internalRhyme": JSON.parse(JSON.stringify(ry))['internal_rhyme']
              //         }
              //       } catch (e) {
              //         console.warn("error getting internal rhymes: ", e);
              //       }
              //     }
              //   } catch(e){
              //   // console.log("error: ", e);
              //   } finally {
              //   }  
              //   try {
              //     initialHumanReadableTextRef.value.lineObj[JSON.parse(JSON.stringify(lineIndex))]['syllablesInLine'] = JSON.parse(JSON.stringify(temp.value.syllables_per_line))[lineIndex]
              //   } catch {
              //     console.log("error getting syllables in line *** ");
              //   }
              // })  
            const tempGramArr = ref([])
    
            // temp.value.most_common_words.forEach((word, rank) => {
      
            //   initialHumanReadableTextRef.value.textObj.mostCommonWords[rank]={"word":JSON.parse(JSON.stringify(word[0])),"occurances":JSON.parse(JSON.stringify(word[1]))};
            // });
          
            temp.value.sentence_id.forEach(sentence => {
              // console.log("in sentence ID loop");
              initialHumanReadableTextRef.value.sentenceObj[sentence] = {
                sentenceSentimentCompound: JSON.parse(JSON.stringify(temp.value.sentence_sentiment_compound[parseInt(sentence)])),
                sentenceSentimentNegative: JSON.parse(JSON.stringify(temp.value.sentence_sentiment_neg[parseInt(sentence)])),
                sentenceSentimentNeutral: JSON.parse(JSON.stringify(temp.value.sentence_sentiment_neu[parseInt(sentence)])),
                sentenceSentimentPositive: JSON.parse(JSON.stringify(temp.value.sentence_sentiment_pos[parseInt(sentence)])),
                sentenceGrammarArray: [],
                sentenceSpacyEntities: []
              }
            });
            temp.value.sentence_grammar.word_level_grammar_result.forEach(wordGram => {
              // console.log("in grammar loop");
              initialHumanReadableTextRef.value.sentenceObj[JSON.parse(JSON.stringify(wordGram))['sentence_index']]['sentenceGrammarArray'].push({
                "sentenceIndex":JSON.parse(JSON.stringify(wordGram))['sentence_index'],
                "tokenTag":JSON.parse(JSON.stringify(wordGram))['token_tag'],
                "tokenPos":JSON.parse(JSON.stringify(wordGram))['token_pos'],
                "tokenText":JSON.parse(JSON.stringify(wordGram))['token_text'],
                "idx_in_sent":JSON.parse(JSON.stringify(wordGram))['index_in_sent']
              })    
            });
            temp.value.spacy_entities.forEach(entity=>{
              console.log("in entities loop...")
              initialHumanReadableTextRef.value.sentenceObj[JSON.parse(JSON.stringify(Object.keys(entity)))].sentenceSpacyEntities.push(
                {
                  "text": Object.keys(JSON.parse(JSON.stringify(Object.values(Object.values(entity))))[0])[0],
                  "type": Object.values(JSON.parse(JSON.stringify(Object.values(Object.values(entity))))[0])[0],
                }
              )
        
            })

            // Update Local Storage
            if (!localStorage.getItem(url)){
              localStorage.setItem(url, JSON.stringify(JSON.parse(JSON.stringify(initialHumanReadableTextRef.value))));
            }
            
            // if(JSON.parse(JSON.stringify(props)).length > 1 && JSON.parse(JSON.stringify(props)).selectedAuthor && JSON.parse(JSON.stringify(props.selectedTitle)) && currentLinesCount.value){
            //   if(currentLinesCount.value < 2 && additionalTexts[0]){
            //     console.log(`AUTHOR ${JSON.parse(JSON.stringify(props)).selectedAuthor} / TITLE: ${JSON.parse(JSON.stringify(props)).selectedTitle}`)
            //     additionalTexts[0].author = JSON.parse(JSON.stringify(props)).selectedAuthor;
            //     additionalTexts[0].title = JSON.parse(JSON.stringify(props)).selectedTitle;
            //   } 
            //   if(currentLinesCount.value == 2 && additionalTexts[1]) {
            //     additionalTexts[1].author = props.selectedAuthor;
            //     additionalTexts[1].title = props.selectedTitle;
            //   }
            // }
            console.log("tEEEEEDST: ", JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)))
            //let finalObj = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value));
            // document.getElementById('fullTextGraphWrapper').innerText = (finalObj.textObj);
            ///////////////////////////////////////////////////////////////////////////////
            ///////////////////////////////////////////////////////////////////////////////
            ///////////////////////////////////////////////////////////////////////////////

            return rawtextfromtoc.value;
          } else {
            return null;
          }
          }).catch(error => {
          //console.log('Error:', error);
      }); 
    // }  

    return rawtextfromtoc;
  };

// Close full modal & return to initial search setup...
// ----------------------------------------------------
function doCloseFullModalChild(){
  //console.log('in close modal child');
  emit('closedfull')
  
  let jumbotron = document.getElementById('jumbotron');
  if(jumbotron){
    jumbotron.style.display = "flex";
    jumbotron.style.display = "visible";
  }
  // show the text search again

  if(main){
    main.style.visibility = "visible";
    main.style.opacity = 1;
    main.style.display = "flex";
  }
  let headerDiv = document.getElementById("headerDiv");

  if (headerDiv && headerDiv.classList){
    headerDiv.classList.remove("noDisplay");
    headerDiv.style.visibility = "visible";

  } else {
    //console.log("in the else for headerdiv classlist");
  }
}

// TODO: componentize and DRY this function (see TheWelcome)
async function scrape_text(url){
    if(!url){
      return;
    }  
     
    let localStorageDataAvailable = localStorage.getItem(url);
    if(localStorageDataAvailable !== null && noLateUpdateAfterNLTK.value !== true){
      if(noLateUpdateAfterNLTK.value === true){
        return;
      }
      emit('closedmodal');
      emit('openedfull');
      emit('closemodalgotlocal',url)
      // inGraphs.value = true;
      ready.value = true;
        
      /////////
      let updatePopup = document.getElementById("d3UpdateButtonsWrapper");

      if(updatePopup){
        // console.log("ADD A CHECK HERE FOR IN GRAPHS");
        updatePopup.classList.remove("animate-close");
      }
      let addTextButton = document.getElementById("addTextButton");
      if(addTextButton){
        addTextButton.classList.remove("animate-close");
      }
      let compareButton = document.getElementById("compareButton");
      if(compareButton){
        compareButton.classList.remove("animate-close");
      }
      let cycleBackBtn = document.getElementById("cycleReturnToSearch")
      if(cycleBackBtn){
        cycleBackBtn.classList.remove("animate-close");
      }
      /////////

      initialHumanReadableTextRef.value = JSON.parse(localStorageDataAvailable);
      // console.log("JUST CHECKING: ", JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)))
        // emit('closedmodal');
        // emit('openedfull');
        // emit('closemodalgotlocal')
        let fullModal = await modalFull.value;
        if(fullModal && fullModal.classList){
          fullModal.classList.remove("awaiting");
          fullModal.classList.add("receivedSingleTextData");
          fullModal.style.display = "visible"
          let main = document.getElementById("main");
          if(main){
            main.style.visibility = "visible";
            main.style.opacity = 1;
          }
        } else {
          //console.log("in else for fullmodal: ", fullModal);
          inGraphs.value = true;
          if(main){
            main.visibility = "hidden";
          }
        }

      let graphs = document.getElementById('graphs')
      // console.log("WHAT ARE GRAPHS? ", graphs);
      let results = document.getElementsByClassName('modal-single-text-results')
      
      console.log("what are results? ", results);
      if(results){
        inGraphs.value = true;
        if(results){
          if(document.getElementById("modalFull")){
            document.getElementById("modalFull").classList.remove("receivedSingleTextData");
            //document.getElementById("modalFull").style.display = "none"
          }
        }
        if(graphs){
          graphs.style.display = "flex";
        } else {
          //console.log("not any graphs");
        }
        if(document.getElementById('main')){
          document.getElementById('main').style.display = "none";
        } else {
          console.log("not any main");
        }
        if(document.getElementById('searchFields')){
          //console.log("HIDE SEARCH FIELD!")
          document.getElementById('searchFields').style.display = "none";
        } else {
          //console.log("no progress circles");
        } 
        if(document.getElementById("modalFull")){
          document.getElementById("modalFull").style.display = "flex";
        }
      }
      return;
    } else {
      noLateUpdateAfterNLTK.value = true
    }
    ready.value = true;
    inGraphs.value = false;
    emit('closedmodal');

    emit('openedfullawaitscrape');
 
    document.body.style.overflowY = "hidden";

      // close();
      
      //console.log("READY IS NOW TRUE");
     
    let fullModal = await modalFull.value;
      
    tryGetFullModal(url);
};
function selected(e){
  //console.log("received SELECTED emit in the modal parent: ", e);
};

const lineThickness = 3;

function colorInputMountedHandler(){
  if(!rawtextfromtoc.value){
    return;
  }
  //console.log("additional texts val[0]: ", JSON.parse(JSON.stringify(additionalTexts.value))[0])
  if(currentLinesCount.value === 1){
    // console.log("LINE COUNT IS ONE")
    additionalTexts.value[0].author = props.selectedAuthor;
    additionalTexts.value[0].title = props.selectedTitle;
  } else if(currentLinesCount.value === 2){
    additionalTexts.value[1].author = props.selectedAuthor;
    additionalTexts.value[1].title = props.selectedTitle;
    // console.log("LINE COUNT IS TWO")
  } else if(currentLinesCount.value === 3){
    console.log("LINE COUNT IS THREE")
  } else if((currentLinesCount.value === 4)){
    console.log("LINE COUNT IS FOUR")
  } else {
    //console.log("how did this happen to current lines count? ", (currentLinesCount.value === 1));
  }
  // Update Graph Keys
  if(JSON.parse(JSON.stringify(additionalTexts.value))[0].title === ''){
    additionalTexts.value[0].title = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).title;
    additionalTexts.value[0].author = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).author;
    additionalTexts.value[0].titleUrl = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).titleUrl;

  } else {
    //ADD OPTIONS FOR NEWLY SCRAPED TEXTS HERE
    //console.log("LINE COUNT: ", currentLinesCount.value);
    if(!JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).length){
      return;
    }
    additionalTexts.value[currentLinesCount.value].title = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).title;
    additionalTexts.value[currentLinesCount.value].author = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).author;
    additionalTexts.value[currentLinesCount.value].titleUrl = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).titleUrl;
  }
  return additionalTexts.value;      

} 

function colorPickerShowHandler(){

}
function colorChanged(){

}
//console.log("additional texts : ", JSON.parse(JSON.stringify(additionalTexts.value)))

// THESE COUNTS WILL BE USED TO INFORM KEYBUILDER & SHAPE GRAPH
function trySetDataCountXLengthMax(num){
  num = Math.max.apply(Math, num);
  // console.log("in MAX X! ", num);
  // console.log("why are we here??")

 if(numberXMax.value[currentLinesCount.value - 1] && num > JSON.parse(JSON.stringify(numberXMax.value))[currentLinesCount.value -1]){
    numberXMax.value[currentLinesCount.value - 1] = num;

 } else {
   numberXMax.value[currentLinesCount.value - 1] = num;

 }

}
function trySetDataCountXLengthMin(num){
  num = num.filter(w=>w || w === 0)[0]

  if(numberXMin.value && numberXMin.value.length > 0 && numberXMin.value[currentLinesCount.value - 1] && num <= numberXMin.value[currentLinesCount.value - 1]){    
    numberXMin.value[currentLinesCount.value - 1] = num;
  } else if (!numberXMin.value[currentLinesCount.value - 1]){
    numberXMin.value[currentLinesCount.value - 1] = num;
  } else {
    numberXMin.value[currentLinesCount.value - 1] = num;
  }
}

function trySetDataCountYLengthMax(num){
  if(Math.max.apply(Math, num) > num){
    num = Math.max.apply(Math,num);
  }
  if(numberYMax.value[currentLinesCount.value - 1] && num > JSON.parse(JSON.stringify(numberYMax.value[currentLinesCount.value - 1]))){
      numberYMax.value[currentLinesCount.value - 1] = num;
  } else {
    numberYMax.value[currentLinesCount.value - 1] = num;
  }
}
function trySetDataCountYLengthMin(num){
  num = Math.min.apply(Math,num)
  if(!numberYMin.value[currentLinesCount.value - 1]){
    return;
  }
  if(numberYMin.value[currentLinesCount.value - 1] && numberYMin.value[currentLinesCount.value - 1].length > num){
    numberYMin.value[currentLinesCount.value - 1] = num;
  } else if(!numberYMin.value[currentLinesCount.value - 1]){
    numberYMin.value[currentLinesCount.value - 1] = num
  } else {
    //console.log(`${numberYMin.value[currentLinesCount.value - 1]} is smaller than ${num}`)
    numberYMin.value[currentLinesCount.value - 1] = JSON.parse(JSON.stringify(numberYMin.value[currentLinesCount.value - 1]));
  }
} 

function trySetDataNameX(name){
  valueX.value=name;
  document.getElementById("xAxisRangeDisplay").innerText = name;
  // let labels = JSON.parse(JSON.stringify(optionsX.value)).map(x=>x.label);
  //console.log("CHECK XDATANAME! ", valueX.value)
  if(!JSON.parse(JSON.stringify(additionalTexts.value)).length){
    return;
  }
  let labels = JSON.parse(JSON.stringify(additionalTexts.value)).map(i=>i.author)
  if(labels.indexOf(valueX.value) === -1){
      let tagX = {
        label: valueX.value,
        value: [Math.min(...JSON.parse(JSON.stringify(numberXMin.value)).filter(i=>typeof i === "number")), Math.max(...JSON.parse(JSON.stringify(numberXMax.value)).filter(i=>typeof i === "number"))],
        isIndex: xIsIndexAxis.value
      }
      // if(optionsY.indexOf(tagX.label)===-1){
      // optionsY.value.push(tagX)
      if(optionsX.value.indexOf(tagX.label)===-1){
        optionsX.value.push(tagX.label);
      }
  }
  return valueX.value; 
}

function trySetDataNameY(name){
  valueY.value = name;
  document.getElementById("yAxisRangeDisplay").innerText = name;
  let labels = optionsY.value.map(x=>x.label);
  if(labels.indexOf(valueY.value) === -1){
      let tagY = {
        label: valueY.value,
        value:  [Math.min(...JSON.parse(JSON.stringify(numberXMin.value)).filter(i=>typeof i === "number")), Math.max(...JSON.parse(JSON.stringify(numberXMax.value)).filter(i=>typeof i === "number"))],
        isIndex: yIsIndexAxis.value
      }
      optionsY.value.push(tagY)
      optionsX.value.push(tagY)
  }
  return valueY.value;
}

function toggleMonochrome(){
  if(axisColorMatchBool.value === true){
    axisColorMatchBool.value = false;
  } else {
    axisColorMatchBool.value = true;
  }
}
function showUpdateButtons(){
  let wrapperTitle = document.getElementById("buttonsWrapperTitle");
  let wrapperSubtitle = document.getElementById("buttonsWrapperSubtitle");
  let wrapperBtns = document.getElementById("buttonsInnerWrapper");
  if(wrapperTitle){
    wrapperTitle.style.display = "inline-block";
  } 
  if(wrapperSubtitle){
    wrapperSubtitle.style.display = "inline-block";
  } 
  if(wrapperBtns){
    wrapperBtns.style.display = "inline-block";
  } 
}
function openUpdatePopup(){
  let graph = document.getElementById("svgId");
  if(graph){
    graph.style.bottom = "0%";
  }
  showUpdateButtons();
  document.getElementById("grammarDisplayWrapper").style.display = "none";
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
  let updatePopup = document.getElementById("d3UpdateButtonsWrapper");
  //console.log("WEE SHOULD BE HITTING THIS!!!! OPEN UPDATE POPUP", updatePopup);
  if(updatePopup){
    //console.log("ADD A CHECK HERE FOR IN GRAPHS");
    updatePopup.classList.remove("animate-close");
  }
  let updateDataBtn = document.getElementById("updatePopupButton");
  if(updateDataBtn){
    updateDataBtn.classList.add("animate-close");
  }
  let addTextButton = document.getElementById("addTextButton");
  if(addTextButton){
    addTextButton.classList.add("animate-close");
  }
  let compareButton = document.getElementById("compareButton");
  if(compareButton){
    compareButton.classList.add("animate-close");
  }
  let cycleBackBtn = document.getElementById("cycleReturnToSearch")
  if(cycleBackBtn){
    cycleBackBtn.classList.add("animate-close");
  }
}

function closeUpdatePopup(){
    let updatePopup = document.getElementById("d3UpdateButtonsWrapper");
    //console.log("WEE SHOULD BE HITTING THIS!!!! CLOSE UPDATE POPUP", updatePopup);
    if(updatePopup){
      updatePopup.classList.add("animate-close");
    }
    let updateDataBtn = document.getElementById("updatePopupButton");
    if(updateDataBtn){
      updateDataBtn.classList.remove("animate-close");
    }

    let addTextButton = document.getElementById("addTextButton");
    if(addTextButton){
      addTextButton.classList.remove("animate-close");
    }
    let compareButton = document.getElementById("compareButton");
    if(compareButton){
      compareButton.classList.remove("animate-close");
    }
    let cycleBackBtn = document.getElementById("cycleReturnToSearch")
      if(cycleBackBtn){
        cycleBackBtn.classList.remove("animate-close");
      }

      inGraphs.value = true;
}

function frameLast(){
  if(yAxisFramingLast.value === true){
    yAxisFramingLast.value = false;
  } else {
    yAxisFramingLast.value = true;
  }
}

function selectXAxis(){
  let keyPopupDisplay = document.querySelector('#newRow_X > .rangeDisplay');

  if(keyPopupDisplay){
    //console.log("WHAT IS SELECTED X AXIS??? ", selectedXAxisRef.value)
    keyPopupDisplay.innerText = JSON.parse(JSON.stringify(selectedXAxisRef.value)).label;
    xIsIndexAxis.value = JSON.parse(JSON.stringify(selectedXAxisRef.value)).isIndex;
    if(xIsIndexAxis.value){
      document.getElementById("xRangeDisplay").classList.add("is-index-axis");
    } else {
      document.getElementById("xRangeDisplay").classList.remove("is-index-axis");
    }
  } else {
    //alert("no keybuilder div!");
  }
}

function selectYAxis(event){
  let keyPopupDisplay = document.querySelector('#newRow_Y > .rangeDisplay');
  if(keyPopupDisplay){
    keyPopupDisplay.innerText = JSON.parse(JSON.stringify(selectedYAxisRef.value)).label;
    yIsIndexAxis.value = JSON.parse(JSON.stringify(selectedYAxisRef.value)).isIndex;
    //console.log("???? ", yIsIndexAxis.value);
    if(yIsIndexAxis.value){
      document.getElementById("yRangeDisplay").classList.add("is-index-axis");
    } else {
      document.getElementById("yRangeDisplay").classList.remove("is-index-axis");
    }
  }
}

function clickedLineRow(row){
  // alert('works!')
  //console.log("is this hitting row: ", row);
  let sel = document.querySelector(`.selectedLine`);
  //console.log("check on sel: ", sel);
  if(sel){
    //console.log("selected: ", sel);
    sel.classList.remove("selectedLine");
  }
  if(row>0){
  let newSel = document.getElementById(`newRow_${row}`);
  //console.log("check on newSel: ", newSel);
  newSel.classList.add('selectedLine');
  } else {
      let newSel = document.getElementById(`newRow_${row}`);
  //console.log("check on newSel for zero: ", newSel);
  newSel.classList.add('selectedLine');
  }
  //console.log("row: ", row);
  selectedRow.value = row;

  //console.log('check on selected row in modal: ', selectedRow.value)
}
function cycleReturnToSearch(){
  graphstateRef.value = 0;
  currentLinesCount.value = 0;
  let moveableGrammarWrapper = document.getElementById("grammarDisplayWrapper");
      if(moveableGrammarWrapper){
        moveableGrammarWrapper.style.display = 'none';
      }
  let modalHead = document.getElementById("modalHead");
      if(modalHead){
        modalHead.style.display = 'none';
      }
  inGraphs.value = false;
  ready.value = false;
  let searchArea = document.getElementById("searchFields");
  if(searchArea){
    searchArea.style.visibility="visible";
    searchFields.style.display = "flex";
  }
  let headerDiv = document.getElementById("headerDiv");
  if(headerDiv){
    headerDiv.style.visibility = "visible";
  }
  if(document.getElementById("modalFull")){
    document.getElementById("modalFull").classList.remove("receivedSingleTextData");
    document.getElementById("modalFull").style.display = "none"
  }
  let main = document.getElementById("main");
  if(main){
    main.style.visibility = "visible";
    main.style.opacity=1;
  }
  inGraphs.value = false;
  secondTextRef.value = false;
 
  doCloseFullModalChild();
  
  
 // console.log("second text is ... ", secondTextRef.value);

}
function dataHolder1Grandparent(savedVal){
  console.log("THIS IS RIDICULOUS ", savedVal);

    preservedDataLine1.value = JSON.parse(JSON.parse(JSON.stringify(savedVal)));

}
</script>

<template>
  <Head>
    <!-- <title>Hello World</title> -->
    <base href="/base" />
    <html lang="en-US" class="theme-dark" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.2/css/all.min.css" integrity="sha512-1sCRPdkRXhBV2PBLUdRb4tMg1w2YPf37qatUFeS7zlBy7jJI8Lf4VHwWfZZfpXtYSLy85pkm9GaYVYMfw5BC1A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  </Head>
<Teleport to="body">

  <div v-if="ready" class="full-screen-modal modal-backdrop">
    <div id="modalFull" ref="modalFull">
     

      <section v-if="inGraphs" id="graphs">
        <slot  name="graphs">
 

          <header v-if="inGraphs" id="modalHead" class="modal-header">
            <slot name="header">
              <!-- Single Text Analysis -->
            </slot>
              <button
                type="button"
                id="updatePopupButton"
                class="btn-green animate-close"
                @click="openUpdatePopup"
              >
                Update
              </button>
              <button
                type="button"
                id="addTextButton"
                class="btn-green animate-close"
                @click="tryAddNewText"
              >
                ReturnOld
              </button>
              <button
                type="button"
                id="compareButton"
                class="btn-green animate-close"
                @click="openKeyPopup"
              >
                Key
              </button>

              <button
                type="button"
                id="cycleReturnToSearch"
                class="btn-green animate-close"
                @click="cycleReturnToSearch"
              >
                Return
              </button>
         
            <button
              type="button"
              class="btn-close"
              @click="doCloseFullModalChild"
            >
              x
            </button>
          </header>


          <GraphModal v-if="inGraphs" 
            :graphstate="graphstateRef" 
            :dataObj="initialHumanReadableTextRef"
            :preservedDataLine1="preservedDataLine1"
            :color0="color0"
            :color1="color1"
            :color2="color2"
            :color3="color3"
            :colorX="colorX"
            :colorY="colorY"
            :yAxisFramingLast="yAxisFramingLast"
            :currentLinesCount="currentLinesCount"
            :axisColorMatchBool="axisColorMatchBool"
            :selectedRow="selectedRow"
            :selectedXAxisRef="selectedXAxisRef"
            :selectedYAxisRef="selectedYAxisRef"
            @closeUpdatePopup="closeUpdatePopup"
            @numberXMin="trySetDataCountXLengthMin"
            @numberXMax="trySetDataCountXLengthMax"
            @numberYMin="trySetDataCountYLengthMin"
            @numberYMax="trySetDataCountYLengthMax"
            @dataHolder1Grandparent="dataHolder1Grandparent"
            @dataname_x="trySetDataNameX"
            @dataname_y="trySetDataNameY"

          ></GraphModal>
        </slot>
      </section>
      <section v-if="inGraphs" id="linePickerPopup">
        <slot>            
          <div id="newTextPopup" v-if="inGraphs">
            
            <span id="newTextPopupTitle">Key <span id="keySelectorClose" @click="closeKeyModal">X</span></span>
            <div id="scrollKeybuilder">
            <!-- v-if="additionalTexts" v-for="item in additionalTexts" :key="item.titleUrl"  -->
              <td id="keyPopupCols" class="small-col-labels-row new-text-popup-row">
                <tr class="new-text-text">Text</tr>
                <tr class="rangeDisplay">Values</tr>
                <!-- <tr class="new-text-viz-variable">Display</tr> -->
                <tr class="color-wrapper">Color</tr>
              </td>
              <td @click="clickedLineRow(0)" id="newRow_0" class="new-text-popup-row selectedLine">
                <tr id="newText_0" class="new-text-text">
                  <span id="newAuthor_0" class="new-text-author">
                  {{additionalTexts[0].author}}
                <!-- {{item.author}} -->
                  </span>
                  <span id="newTitle_0" class="new-text-title">
                    {{additionalTexts[0].title}}
                  </span>
                </tr>
                <tr id="newVariable_0" class="rangeDisplay">
                  <!-- <span>GONZOlast</span> -->
                  <!-- <span class="rangeDisplayRow">
                    X-Range: <span id="xRangeDisplayXMin_0"></span> - <span id="xRangeDisplayXMax_0"></span> 
                  </span>
                  <span class="rangeDisplayRow">
                    Y-Range: <span id="yRangeDisplayYMin_0"></span> - <span id="yRangeDisplayYMax_0"></span>
                  </span>               -->
                </tr>
            
                <!-- <tr id="newVariable_0" class="new-text-viz-variable">
                  GONE GONE

                </tr> -->
                <tr class="color-wrapper">
                  <color-input id="colorInput_0" class="color-input" v-model="color0" position="left" ref="colorInput_0" changed="colorChanged()" @mounted="colorInputMountedHandler" @pickStart="colorPickerShowHandler"/>
                </tr>
              </td> 

              <td  v-if="additionalTexts[1]" @click="clickedLineRow(1)" id="newRow_1" class="new-text-popup-row">
                <tr id="newText_1" class="new-text-text">
                  <span id="newAuthor_1" class="new-text-author">
                  {{additionalTexts[1].author}}
                <!-- {{item.author}} -->
                  </span>
                  <span id="newTitle_1" class="new-text-title">
                    {{additionalTexts[1].title}}
                  </span>
                </tr>
                
                <tr id="newVariable_1" class="rangeDisplay">
                  <!-- <span>GONZO AGAIN!</span> -->
                  <!-- <span class="rangeDisplayRow">
                    X-Range: <span id="xRangeDisplayXMin_1"></span> - <span id="xRangeDisplayXMax_1"></span>
                  </span>
                  <span class="rangeDisplayRow">
                    Y-Range: <span id="yRangeDisplayYMin_1"></span> - <span id="yRangeDisplayYMax_1"></span> 
                  </span> -->
                </tr>
                <!-- <tr id="newVariable_1" class="new-text-viz-variable">
                  GONE GONE
                </tr> -->
                <tr class="color-wrapper">
                  <color-input id="colorInput_1" class="color-input" v-model="color1" position="left" ref="colorInput_1" changed="colorChanged" @mounted="colorInputMountedHandler" @pickStart="colorPickerShowHandler"/>
                </tr>
              </td> 
              </div>

            <!-- we should not get these until postMVP -->
            <!-- ----------------------------------------------- -->
           
              <!-- ----------------------------------------------- -->
              
              
            <td id="newRow_X" class="new-text-popup-row">
              <tr id="newText_X" class="new-text-text">
              Create X-Axis
              </tr>
              <tr class="rangeDisplay">

     
                <span class="rangeDisplayRow">
                  <span id="xAxisRangeDisplay"></span>
                  <!-- <span id="xAxisRangeDisplayMin"></span> -->
                </span>
              </tr>
              <!-- <tr id="newVariable_X" class="new-text-viz-variable">
                  <span id="newAxis_X" >
                  <Multiselect                    
                    :placeholder="'Select'"
                    id="xSelectDropdown"
                    v-model="selectedXAxisRef"
                    :object="true"
                    :options="optionsX"
                    @select="selectXAxis()"
                    class="multiselect multiselect-tag is-user"
                  />
                </span>
              </tr> -->
              <tr class="color-wrapper">
                <color-input id="colorInput_X" class="color-input" v-model="colorX" position="left" ref="colorInput_X" changed="colorChanged()" @mounted="colorInputMountedHandler" @pickStart="colorPickerShowHandler"/>
              </tr>
            </td> 

            <td id="newRow_Y" class="new-text-popup-row">
              <tr id="newText_Y" class="new-text-text">
                Create Y Axis
                <button
                  type="button"
                  id="toggleMonochromeBtn"
                  class="green-btn"
                  @click="toggleMonochrome"
                >
                  <span v-if="axisColorMatchBool">Match</span>
                  <span v-else>Unmatch</span>
                </button>
              </tr>
              <tr class="rangeDisplay">
        

                <span class="rangeDisplayRow">
                  <span id="yAxisRangeDisplay"></span>
                  <!-- <span id="yAxisRangeDisplayMin"></span> -->
                </span> 
              </tr>
              <!-- <tr id="newVariable_Y" class="new-text-viz-variable">
                  <span id="newAxis_Y" >
                  <Multiselect                    
                    :placeholder="'Select'"
                    id="ySelectDropdown"
                    v-model="selectedYAxisRef"
                    :object="true"
                    :options="optionsY"
                    @select="selectYAxis(event)"
                    class="multiselect multiselect-tag is-user"
                  />
                </span>
              </tr> -->
              <tr class="color-wrapper">
                <color-input v-if="axisColorMatchBool" id="colorInput_Y" class="color-input" v-model="colorY" position="left" ref="colorInput_Y" changed="colorChanged()" @mounted="colorInputMountedHandler" @pickStart="colorPickerShowHandler"/>
                <color-input v-else id="colorInput_Y" class="color-input" v-model="colorX" position="left" ref="colorInput_Y" changed="colorChanged()" @mounted="colorInputMountedHandler" @pickStart="colorPickerShowHandler"/>
              </tr>
            </td> 

            <div id="keyButtonWrapper">
          
              <!-- <button 
                type="button"
                id="frameLastBtn"
                class="key-popup"
                @click="frameLast">
                Frame
              </button> -->
              <button
                  type="button"
                  id="removeLineButton"
                  class="key-popup"
                  @click="removeLine"
                >
                Remove Line
              </button>
              <button
                  type="button"
                  id="addLineButton"
                  class="key-popup"
                  @click="setLineCount"
                >
                Add Line
              </button>
            </div>

          </div>
          
        </slot>
      </section>

      <section v-if="!inGraphs" class="modal-body">

        <slot name="body">   

          <section id="progressMsg" class="progress-msg">
            <slot name="progressMsg">
              <!-- {{stepMessage}} -->
            </slot>
          </section>
          <section id="modal-textAnalysis-title">
            <slot name="titleDiv">
              
              <span id="textRowAuthor">
                {{props.selectedAuthor}}
              </span>
              
              <span id="textRowTitle">
                {{props.selectedTitle}}
              </span>

            </slot>
          </section> 
          <section id="progressMsgExplanation" class="progress-msg-explanation">
            <slot name="progressMsgExplanation">
            <!-- <h4>Progress Msg Explanation</h4> -->
            <div id="progressMsgExplanationText">
            <!-- <p ></p> -->
            </div>
            <div id="dataPreviewWrapper">
              <p id="progressMsgDataPreview"></p>
            </div> 

            <!-- {{stepMessage}} -->
            </slot>
            <br/>

          </section>

          <section class="progress-circle-section" id="progressCircles">
            <slot name="progressCircles">
              <step-progress icon-class="fa fa-square-check" :steps="mySteps" :current-step="currentStepRef" active-color="#9ea5e9" :line-thickness="1"> </step-progress>
            </slot>
          </section>

          <div id="summaryPreviewWrapper">
            <p id="progressMsgDataSummaryPreview"></p>
          </div>
          <section class="modal-single-text-results">
            <slot name="textAnalysis-results">
          
              <!-- <div id="summaryPreviewWrapper">
                <p id="progressMsgDataSummaryPreview">Lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum </p>
              </div> -->

            </slot>
          </section>
        </slot>
      </section>

      <footer class="modal-footer">
        <slot name="footer">

        </slot>

      </footer>
    </div>
  </div>
  <div v-if="open" ref="modal" class="modal" :class="open ? 'searching' : 'not-searching'">
    <button id="closeBtn" @click="$emit('closedmodal')">X</button>
    <h1 id="tocHeader">Table of Contents</h1>
    <h3 id="tocAuthor">{{props.selectedAuthor}}</h3>
    <h4 id="tocTitle">{{props.selectedTitle}}</h4>
    <span id="tocSubtitle">Click any link below to load the text</span>
    <div id="tocDataWrapper">
      <SelfBuildingSquareSpinner v-if="!JSON.parse(JSON.stringify(props.tocdata))[0]" class="self-building-square-spinner"/>
        <div id="tocData" v-for="item in props.tocdata || []">
            <i icon-class="fa-solid fa-ellipsis" />
 
            <h3 @click="scrape_text(item.link_href)">{{
                item.link_text
            }}</h3>

        </div>
    </div>


  </div>


</Teleport>

</template>

<style scoped>
  @charset "UTF-8";

@font-face {
  font-family: "untitled-font-1";
  src: url("untitled-font-1.svg#untitled-font-1") format("svg");
  font-weight: normal;
  font-style: normal;
 
}

[data-icon]:before {
  font-family: "untitled-font-1" !important;
  content: attr(data-icon);
  font-style: normal !important;
  font-weight: normal !important;
  font-variant: normal !important;
  text-transform: none !important;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  z-index:10;
}

[class^="icon-"]:before,
[class*=" icon-"]:before {
  font-family: "untitled-font-1" !important;
  font-style: normal !important;
  font-weight: normal !important;
  font-variant: normal !important;
  text-transform: none !important;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.icon-check-square-o:before {
  content: "\61";
}

@keyframes animate-text-scrape {
  0%    { height: 0vh; opacity: 0 }
  100%  { height: 100vh; opacity: 1 }
}
body.modal-open {
  overflow-y: hidden;
  height: 100vh;
}
.modal {
  position: fixed;
  z-index: 999;
  align-items: center;
  left: 0%;
  grid-template-columns: 1fr;
  animation: animate-text-scrape 1s linear;
  background: var(--color-background);
  backdrop-filter: blur(8px);
  overflow-y: scroll;
  width: 100vw;
  margin-left: 12%;
  margin-right: 12%;
  width: 76%;
  top: 4%;
  bottom: 4%;
  height: 92%;
  border-radius: 12px;
}

#summaryWrapper {
  display:flex;
  flex-direction:column;
  overflow-wrap: break-word;
  font-size:12px;
  font-weight:100;
  width:70%;
  text-align:center;
  min-block-size: 200px;
}

#squareBuilderAnim {
  transform: rotateX(3.142rad);
  top: 80px;   
  margin-left: 48%;
}

.small-col-labels-row {
  max-height:20px;
}

#closeBtn {
  right: 12px;
  position: absolute;
  color: rgba(255,255,255,0.9);
  z-index: 1001;
  top: 8px;
  position: fixed;
  width: 16px; 
}
#tocHeader {
    width: 100%;
    text-align: center;
    font-weight: 500;
    border-bottom: solid 1px #9ea5e9;
    padding-left: 48px;
    padding-right: 48px;
    color: rgba(255,255,255,1);
    padding:8px;
    color:#f6f6f6;
}


#tocData {
    margin-top: 8px;
    border-bottom: solid 1px rgba(255, 255, 255, 0.3);
    color: rgba(255,255,255,1);
    font-size: 16px;

    margin-bottom: 0.1rem;
    font-weight: 100;
    cursor: pointer;
    color: var(--color-text);
    padding-top: 12px;
}
#tocData:hover{
  color:rgba(255,255,255,1);
}
#tocDataWrapper {
  margin: 12px;
  margin-top: 16px;
  padding-left: 6%;
  padding-right: 6%;
  padding-bottom: 100px;
  padding-top: 24px;
  border-radius: 8px;
  background: var(--color-background-mute);
  margin-right: 6%;
  margin-left: 6%;
  margin-bottom: 100px;
}

#modalFull {
    background:transparent;
    top: 0px;
    bottom: 0px;
    left: 0px;
    right: 0px;
    box-shadow: 2px 2px 20px 1px;
    position: fixed;
    display: flex;
    flex-direction: column;
    width: 100vw;
    height: auto;
    justify-content: center;
    align-items: center;
    pointer-events:all;
    min-height:100vh;
    align-items: left;


}

#modalFull.awaiting {
    background: transparent;
    pointer-events:all;
 

    border: 6px solid red;
}

.rangeDisplayRow {
  flex-direction:row;
  display:flex;
}

.modal.not-searching {
  overflow-y: hidden;
  z-index:9999;
}

#modalFull.receivedSingleTextData {
  background:transparent;
  pointer-events: none;


}

.modal-header,
.modal-footer {
  width: 100vw;
/*  padding: 15px; */
  display: flex;
}

.modal-header {
  width: 100%;
  position: relative;
  z-index: 40;
  height: 0px;
  font-size: 48px;
  font-weight: 100;

  left: 0px;
  background: rgba(255, 255, 255, 0.078);
  transition: height 1s ease-in;
  position: absolute;
}
  .modal-header:hover {
    background: hsla(193, 82%, 49%, 0.7);
  }

  .modal-footer {
    border-top: 1px solid #eeeeee;
    flex-direction: row;
    justify-content: flex-end;
   
    bottom:0px;
    left:0px;
    right:0px;
    position:absolute;
  }

  .modal-body {
    position: relative;
    padding: 0% 0%;
    max-width: 100%;
    height: 100%;
  }
  #progressMsgExplanation {
    text-align: center;
    justify-content: center;
    left: 0px;
    right: 0px;
    width: 100%;
    border-radius: 8px;
    position: relative;
    flex-direction: column;
    display: flex;
    padding: 0%;
    line-height: 1.5;
    font-size: 16px;
    font-family: monospace;
    flex-direction: row;
    padding-left:8px;
    padding-right:8px;

    height: 100px;
  }
  #progressMsgExplanationText {
    width: 40%;
    padding-top: 8px;
    padding-left:8px;
    padding-right:8px;
    left: 0px;
    font-size: 16px;
    font-family: monospace;
    position: absolute;
    overflow-y: scroll;
    text-align: center;
    height:100px;
    padding: 0px;
  }
  .btn-close {
    position: absolute;
    display:none;
    top: 0px;
    right: 0px;
    border: none;
    font-size: 20px;
    padding: 10px;
    cursor: pointer;
    font-weight: bold;
    color: rgba(255,255,255,0.92);
    background: var(--color-background);
  }

  .btn-green {
    color: white;
    background: #9ea5e9;
    border: 1px solid #9ea5e9;
    border-radius: 2px;
    width: 40px;
    height: 40px;
    float: right;
    margin-right: 4px;
    margin-left: 4px;
    position: absolute;
    background: 36px;
    z-index:9999;
  }
  
  #dataPreviewWrapper {
    position: absolute;
    left: 0px;
    height: 80px;
    top: -8px;
    width: 60%;
    left: 40%;
    /* overflow-y: scroll; */
    font-weight: 700;
    font-size: 22px;
    font-family: monospace;
    overflow-y: hidden;
    margin-top: 8px;
    color: #000;

    padding-top: 12px;
    height:100px;
  }

  .hideFullModal {
    display:none;
  }
  #singleTextAnalysisRow {
    grid-template-columns: 1fr 1fr 1fr;
    flex-direction: row;
    display: flex;
    width: 100vw;
    justify-content: center;
    top: 24px;
    font-size: 28px;
    color: blue;
  }
  .self-building-square-spinner {
    justify-content: center;
    position: absolute;
    text-align: center;
    align-items: center;
    left: calc(50% - 10px);
    margin-top: 32px;
  }
  #textRowTitle, #textRowAuthor{
    width: 100%;
    display:flex;
    overflow-y:scroll;
  }
  #textRowAuthor {
    font-size:18px;
    font-weight:500;
  }
  #textRowTitle {
    font-size:14px;
    font-weight:300;
    text-overflow: ellipsis;
    max-height: 48px;
  }

  #tocAuthor, #tocTitle, #tocSubtitle {
    position: relative;
    display: inherit;
    text-align: center;
    width: 100%;
    min-height: 32px;
    padding: 4px;
    flex-direction: row;
    font-weight: 500;
    font-family: monospace;
    padding-left: 12%;
    padding-right: 12%;

  }

  #tocSubtitle {
    background: rgba(158,165,233,.7);
    color:#000000;
    margin-bottom:12px;
    left: 12%;
    right: 12%;
    width: 76%;
  }

  #tocAuthor {
    font-size:18px;
  }

  #tocTitle {
    font-size:13px;
  }

  #modal-textAnalysis-title {
    /* this is the overarching modal */
    padding-left: 8%;
    padding-right: 8%;
    padding-top:2%;
    padding-bottom: 12%;
    position: relative;
    background: var(--color-background);
    height: 100px;
    overflow-y: scroll;
    border-top: solid 1px var(--color-heading);
    border-bottom: solid 1px var(--color-text);
  }
  .modal-single-text-results {
    width: 100%;
    display: flex;
    text-align: center;
    bottom: 32px;
    visibility: visible;
    height: 40px;
    position: absolute;
    flex-direction: row;
    pointer-events: none;
    background:transparent;
    pointer-events: none;
  }
  .results-col {
    width:33vw;
    background: #0AA0C9;
    margin-left: 8px;
    margin-right: 16px;
    min-height: 200px;
    border-radius: 8px;
    cursor: progress; 
    background: 
      linear-gradient(0.25turn, transparent, green, transparent),
      linear-gradient(var(--color-background),rgba(0,0,0,0.78)),
      radial-gradient(38px circle at 19px 19px, #eee 50%, transparent 51%),
      linear-gradient(var(--color-background), var(--color-background),grey);  
    background-repeat: no-repeat;

    background-position: -315px 0, 0 0, 0px 190px, 50px 195px; 
    animation: loading 1.5s infinite;
  }
  
  #progressCircles {

    /* max-width: 100%; */
    right: 0px;
    left: 0%;
  }

  .step-progress__wrapper {
    width: 90vw;
    
  }
  .step-progress__step--active span {
    color: #ffffff;
    z-index: 10;
  }
  .check-square-o {
    z-index: 10;
    font-family: "untitled-font-1";

    z-index: 10;
  }
  #summaryPreviewWrapper{
    display: none;
    flex-direction: row;
    object-fit: contain;
    width: 100%;
    height: 120px;
    bottom: 0px;
    position: absolute;
    overflow-y: scroll;
    transition: all 1s;
    padding-left: 8px;
    padding-right: 8px;
  }
  #progressMsgDataSummaryPreview {
    overflow-y: scroll;
    width: 99%;
    display: flex;
    text-align: center;
    visibility: visible;
    height: 140px;
    position: absolute;
    flex-direction:column;
    padding-right:1%;
    transition: all 2s;
    padding-top:24px;
  }

.new-font {
  font-family: untitled-font-1;
  color: #ffffff;

  -ms-transform: scaleX(-1) rotate(-35deg); /* IE 9 */
  -webkit-transform: scaleX(-1) rotate(-35deg); /* Chrome, Safari, Opera */
  transform: scaleX(-1) rotate(-35deg);
}

.progress-circle-section {
  width:100%;
  top: 8%;
}
.progress-msg {
  width:100%;
  z-index: 1;
}


#topBtns {
  visibility: hidden;
}

#addTextButton {
  display: none;
}
#cycleReturnToSearch{
  right:224px;
}
#graphs {
  width: 100%;
    height: 100%;

    bottom: 0px;
    z-index:9999;


}
#newTextPopup {
  display: none;
  flex-direction: column;
  top: 5%;
  left: 5%;
  right: 5%;
  width: 100%;
  bottom: 0%;
  height: auto;
  max-width: 800px;
  /* max-height: 452px; */
  /* overflow-y: scroll; */
  width: 90%;
}
.rangeDisplay {
  width:28%;
  justify-content: center;
  flex-direction: column;
  display: flex;
}
.picker-popup {
  background:var(--color-background);
  background-color:var(--color-background);
  width:calc(100% - 40px);
  left:0px;
  bottom:0px;
  position:fixed;
}
.color-input .picker-popup {
  background-color:var(--color-background) !important;
  color:#ffffff;
  --arrow-color:#ffffff;
  background:var(--color-background) !important;
}
.text-format-arrows,.arrow-up,.arrow-down {
  --arrow-color: #ffffff;
}
.color-input .slider-canvas {
  border-radius: 0 8px 0 0;
  border-top: solid 1px #ffffff;
  border-right: solid 1px #ffffff;
  border-bottom: solid 1px #ffffff;
} 
#linePickerPopup {
  background-color:var(--color-background);
  background:var(--color-background);
  color: #ffffff;
  border:solid 6px lightblue;
  z-index:  9999;
  display:none;

  border: 8px solid purple;
}
#toggleMonochromeBtn {
  max-width:120px;
  min-width:80px;
}
.saturation-area {
  background-color:var(--color-background) !important;
  background:var(--color-background) !important;
}
.box {
  float: right;
}
.color{
  color: #ffffff;
  background: #ffffff;  
}

.step-progress__step--active .step-progress__step-label, .step-progress__step--active span{
  background-color: #e6e4d6;

}
button#closeBtn {
  min-width:40px;
}
.new-text-popup-row {
  width: 100%;
  background-color:#484D45!important;
  background:#484D45!important;
  height:80px;
  color: #ffffff;
  flex-direction: row;
  display: flex;
  padding-left:8px;
  text-align: left;
  border-top: 1px solid;
  min-height:76px;
}
.new-text-text {
  flex-direction: column;
  display: flex;
  width:52%;
  overflow:hidden;
  padding-left: 4px;
  justify-content:center;
}
.new-text-viz-variable {
  width: 30%;
  text-align: left;
  overflow: auto;
  display: flex;
  flex-direction: column;
  padding-left: 24px;
  justify-content: center;
}

.color-input{
  width: 100%;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}



#newTextPopupTitle {
  width:100%;
  height:56px;
  color:#ffffff;
  font-weight:100;
  font-size:36px;
  background:#333;
  padding-left: 8px;
  border-radius: 8px 8px 0px 0px;
  display: flex;

}
#keySelectorClose {
    float: right;
    padding: 0px;
    cursor: pointer;
    right: 4px;
    position: absolute;
    font-size: 26px;
    padding-right: 8px;
}
.new-text-author, .new-text-title, .new-text-titleUrl {
    overflow-x: hidden;
    height: 24px;
    padding-right:4px;
}
#newVariable_X, #newVariable_Y {
  overflow:visible;
}
.multiselect {
  background: black !important;
  background-color: black !important;
  color: green !important;
  border: 1px solid green;
  border-radius: 8px;
}
 .multiselect-option {
  background: var(--color-background) !important;
  background-color: var(--color-background) !important;
  color: #ffffff;
  }
  
  .multiselect-tag.is-user {
    padding: 8px 8px;
    border-radius: 22px;
    margin: 10px -12px 20px;
    max-width: 204px;
  }

.multiselect-dropdown {
  background: var(--color-background) !important;
  background-color: var(--color-background) !important;
  color: black;
}

.is-pointed {
  background: #eee;
  background-color: #eee;
}

#keyButtonWrapper {
  display:flex;
  flex-direction:row;
  border-radius:0 0 8px 8px;
  background: #333;
}
.key-popup {
  width: 100%;
  background-color: rgba(0,0,0,0.88);
  color: #e6e4d6;
  height: 48px;
  margin: 16px;
  
}
.key-popup:hover {
  background: #9ea5e9;
  color: #181818;
}
#newRow_1, #newRow_2, #newRow_3 {
  display:none;
}
.hide {
  display: none;
}
#updatePopupButton {
  right: 8px;
}
#newAxis_X, #newAxis_Y {

}
button.green-btn {
  min-width: 160px;
  font-size: 20px;
  font-weight: 100;
  max-height: 30px;
}
.color-wrapper {
    justify-content: center;
    width: 16%;
    /* top: 25%; */
    flex-direction: column;
    display: flex;
    align-items: center;
}
#keyPopupCols {
  max-height:20px;
  min-height:20px;
}
.is-index-axis {

  background: #c1dbd7;
}
.selectedLine {
  border: solid 2px #E6CECA;
}
#compareButton {
  right: 116px;
}
</style>
<style src="@vueform/multiselect/themes/default.css"></style>