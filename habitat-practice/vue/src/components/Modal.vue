<script setup>
import { ref, watch, onMounted } from 'vue'
import { SelfBuildingSquareSpinner  } from 'epic-spinners'
import StepProgress from 'vue-step-progress';
import './untitled-font-1.svg'

import 'vue-step-progress/dist/main.css';
import { Head } from '@vueuse/head';
import LineChart from './LineChart.vue';
import StackedAreaChart from './StackedAreaChart.vue';
import GraphModal from './GraphModal.vue';
import ColorInput from 'vue-color-input';
import Multiselect from '@vueform/multiselect'

// Define Props, Emits & Key Variables
// ----------------------------------------------------

const emit = defineEmits(['closedmodal','openedfullawaitscrape','openedfull','closedfull'])

const props = defineProps({
  open: Boolean,
  openFull: Boolean,
  tocdata: Object,
  rawtextdata: String,
  selectedTitle: String,
  selectedAuthor: String,
  // graphstate: String
});

const currentTextData = ref([]);
const selectedRow = ref(0);
const selectedXAxisRef = ref();
const selectedYAxisRef = ref();
const xIsIndexAxis = ref(true);
const yIsIndexAxis = ref(false);
const yAxisFramingLast = ref(false);


const secondTextRef = ref();
secondTextRef.value = false;

const graphstateRef = ref(0);
const axisColorMatchBool = ref(false);

// graphstate.value = "singleText";

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
    sentenceId: {
      sentimentCompound: Number,
      sentimentNegative: Number,
      sentimentNeutral: Number,
      sentimentPositive: Number,
      entitiesInSentence: Array,
      sentenceGrammarArray: Array
    }
  },
  linesArray: Array,
})

initialHumanReadableTextRef.value.textObj.mostCommonWords = [];

const currentStepRef = ref(null);

let searchModal;
onMounted(()=>{
  currentStepRef.value = 0;
  setTimeout(() => {
    searchModal = modal.value;
  }, 10);
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


// Initial soocket implementation 
// ----------------------------------------------------
const socket = new WebSocket('ws://localhost:5000/ws');
console.log('do we have a socket? ', socket);
socket.onopen = function (event) {
  console.log('sent opening salvo');
  socket.send("Here's some text that the server is urgently awaiting!");
  console.log('still going after opening salvo');
}

window.onbeforeunload = function() {
    console.log('are we closing the socket now???');
    socket.onclose = function () {}; // disable onclose handler first
    socket.close();
};

// Text loading steps
// TODO => sort out which we need for initial text loading
// TODO => get these callback numbers in proper 1-2-3 order
const mySteps = ['Text', 'Lines', 'Sentences', 'Vectors', 'Clusters', "Features"]
let stepMessage = '';

socket.onmessage = event => {
    console.log("do we GET SOCKET MSGS!!@!!???");
    if(event.data === 'third_msg'){
      console.log("got third socket msg");
      currentStepRef.value = 0;
      stepMessage = "Gathering text and preprocessing data"
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    }
    if(event.data === 'fourth_msg'){
      console.log("got fourth socket msg");
      currentStepRef.value = 1;
      stepMessage = "Begin line-level and poetic analysis";
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    }
    if(event.data === 'eighth_msg'){
      currentStepRef.value = 2;
      stepMessage = "Begin sentence-level analysis"
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    }
    if(event.data === 'eleventh_msg'){
      currentStepRef.value = 3;
      stepMessage = "Vectorizing"
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    }
    if(event.data === 'twelfth_msg'){
      currentStepRef.value = 4;
      stepMessage = "Clustering"
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    }
    if(event.data === 'thirteenth_msg'){
      currentStepRef.value = 5;
      stepMessage = "Time Series Analysis"
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    }  
    if(event.data === 'fifteenth_msg'){
      currentStepRef.value = 6;
      console.log("HIT FIFTEENTH!");
      stepMessage = "Feature Extraction"
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    
// We've got the text -> reorder the DOM
// ----------------------------------------------------
    let results = document.getElementsByClassName('modal-single-text-results');
      if(results.length > 0){
        console.log("why are we here????????? results length: ", results.length)
        results[0].style.visibility = "visible";
        try{
          if(document.getElementById('progressCircles')){
            document.getElementById('progressCircles').style.display = "none";
          } else {
            console.log("no prog circs");
          }
          if(document.getElementById('progressMsg')){
            document.getElementById('progressMsg').style.display = "none";
          } else {
            console.log("no progress msgs");
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
            console.log("no graphs");
          }
          if(document.getElementById('progressMsgExplanation')){
            document.getElementById('progressMsgExplanation').style.display = "none";
          }
          try {
          document.getElementById('compareButton').style.visibility = "visible";
        // document.getElementById("buttonsInnerWrapper").style.display = "flex"; 
          // document.getElementsByClassName('modal-textAnalysis-title').classList.add("hide");
          document.getElementById("textRowAuthor").style.display = "none";
          document.getElementById("textRowTitle").style.display = "none";
          document.getElementById("searchTextWrapper").style.display = "none";

          // document.getElementsByClassName('wrapper-outer').classList.add("hide");
          // document.getElementsByClassName('wrapper-outer').style.display = "none";

          document.getElementById('headerDiv').style.display = 'none';
          document.getElementById('headerDiv').style.visibility = 'hidden';
          document.getElementById('mainText').style.display = "none";
          document.getElementById('mainTextSubheader').style.display = "none";
          } 
          catch(e){
            console.log("err_modal1 ", e);
          }
        } catch(e){
          console.log("err_modal1 ", e);
        }
      }
    }  
    // let showExplanation = document.getElementById('progressMsgExplanation')
    // if(showExplanation){
    //   showExplanation.style.display = "flex";
    // }
}

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
color0.value = "#00bd7e";

const color1 = ref("");
color1.value = "#00bd7e";

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

additionalTexts.value = [
  {
    title:'',
    author:'',
    titleUrl:'',
    variableX: "varX",
    variableY: "varY"
  },
  {
    title:"1",
    author:"1",
    titleUrl: "1",
    variableX: "X",
    variableY: "Y"
  },
  {
    title:"2",
    author:"2",
    titleUrl: "2",
    variableX: "X",
    variableY: "Y"
  },
  {
    title:"3",
    author:"3",
    titleUrl: "3",
    variableX: "X",
    variableY: "Y"
  },
]

watch(() => [graphstateRef, additionalTexts, color0, color1, color2, color3, colorX, colorY, optionsX, valueX,valueY,optionsY, numberXMax,numberXMin, numberYMax,numberYMin,props.selected, currentLinesCount, currentTextData,axisColorMatchBool,selectedXAxisRef,selectedYAxisRef,props.openFull,yAxisFramingLast],(tocdata,rawtextdata,selectedTitle,selectedAuthor) => {
    
    if(selectedXAxisRef.value){
      console.log("selected x axis ref: ", selectedXAxisRef.value);
      console.log("TRY THIS XREF!!! ", JSON.parse(JSON.stringify(selectedXAxisRef.value)));
    }
    if(props.selected){
      console.log("Props selected: ", JSON.parse(JSON.stringify(props.selected)))
    }
    if(numberXMin.value && Object.values(JSON.parse(JSON.stringify(numberXMin.value))).filter(i=>typeof i === "number").length > 0){
      console.log("WTF IS XMIN VAL? ", Math.max(...Object.values(JSON.parse(JSON.stringify(numberXMin.value)))));
    }

    ready.value = JSON.parse(JSON.stringify(props.openFull));
    console.log("what is props openfull? ", JSON.parse(JSON.stringify(props.openFull)));

      if(currentLinesCount.value === 1){
        showOne.value = true;
      } else if (currentLinesCount.value === 2){
        showTwo.value = true;
        showThree.value = false;
      } else if (currentLinesCount.value === 3){
        showThree.value = true;
        showFour.value = false;
      } else if (currentLinesCount.value === 4){
        showFour.value = true;
      } else {
        console.log("how did we arrive in current count else? ", currentLinesCount.value);
      } 
    });

// Begin process for adding a new text...
// ----------------------------------------------------
function tryAddNewText(){
  console.log("CHECK!!!");
  doCloseFullModalChild();
  secondTextRef.value = true;
  
  console.log("second text is ... ", secondTextRef.value);

}

// Opens Keybuilder Popup
// ----------------------------------------------------
function openKeyPopup(){

  let newTextPopup = document.getElementById("newTextPopup")
  console.log("why ar we checking for modal full? ", modalFull.value);
  if(newTextPopup){
    newTextPopup.style.display = "flex";
    resetRows();
  }
}


// Closes Keybuilder Popup
// ----------------------------------------------------
function closeKeyModal () {
  let popup = document.getElementById("newTextPopup");
  if(popup){
    console.log("closed the key modal");
    popup.style.display = "none";
  }
}

// Reset row count if # of lines changes 
// ----------------------------------------------------
async function resetRows(){
  console.log("resetting rows");
  document.getElementById("newTextPopup").style.display = "none";
  // const open = await openUpdatePopup()


  document.getElementById("newTextPopup").style.display = "flex";

  if(currentLinesCount.value === 4){
    let row4 = document.getElementById("newRow_3");
    if(row4){
      row4.style.display = "flex";
    } else {
      row4.style.display = "none";
      console.log("what is row 4 ", document.getElementById("newRow_3"));
    }
    
  }
  if(currentLinesCount.value >= 3){
    let row3 = document.getElementById("newRow_2");
    if(row3){
      row3.style.display = "flex";
    } else {
      row3.style.display = "none";
      console.log("what is row 3 ", document.getElementById("newRow_2"));
    }
  }
  if(currentLinesCount.value >= 2){
    let row2 = document.getElementById("newRow_1");
    if(row2){
      row2.style.display = "flex";
    } else {
      row2.style.display = "none";
      console.log("what is row 2 ", document.getElementById("newRow_1"));
    }
  }
}

// Remove line from Keybuilder 
// TODO=> carry implementation down into actual graph
// ----------------------------------------------------
function removeLine(){
  console.log('better not be hitting this');
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
  // TODO=> rename or rework this variable to accomodate new flow
  graphstateRef.value = graphstateRef.value + 1;
  console.log("??? ", currentLinesCount.value);

  if(currentLinesCount.value < 5){
    console.log("adding a keybuilder row / graph line here: ", currentLinesCount.value);
    // document.getElementById("addLineButton").disabled = false;
    let popup = document.getElementById("newTextPopup");
    if(popup){
      popup.style.top = 0 - ((currentLinesCount.value) * 4) + "%";
    }
    currentLinesCount.value = currentLinesCount.value + 1;

    resetRows();


  } else {
    // TODO fix this disabling of button
    // document.getElementById("addLineButton").disabled = true;
  }
  console.log("hit comparative: ", graphstateRef.value);
}


function tryGetFullModal(){
    console.log("innnnn try get full modal... ");
    setTimeout(()=>{
      let fullModal = modalFull.value;
      // emit('closedmodal')
      emit('closedmodal')
      console.log("FULL MODAL? ", fullModal);
      if(fullModal && fullModal.classList){
        fullModal.classList.add("awaiting");
        // hide thee text search
        let main = document.getElementById("main");
        if(main){
          main.style.visibility = "hidden";
        }
        console.log("MAIN STYLE VISIBILITY: ", main.style.visibility);
      } else {
        console.log("hit the else");
        
       // console.log("what is the else for full modal? ", fullModal);
      }
    },10)
    clearTimeout();
  };

// Close full modal & return to initial search setup...
// ----------------------------------------------------
function doCloseFullModalChild(){
  console.log('in close modal child');
  emit('closedfull')
  
  let jumbotron = document.getElementById('jumbotron');
  if(jumbotron){
    jumbotron.style.display = "flex";
    jumbotron.style.display = "visible";
  }
  // show the text search again
  let main = document.getElementById("main");
  if(main){
    main.style.visibility = "visible";
    main.style.display = "flex";
  }
  let headerDiv = document.getElementById("headerDiv");
  if (headerDiv && headerDiv.classList){
    headerDiv.classList.remove("noDisplay");
    headerDiv.style.visibility = "visible";
  } else {
    console.log("in the else for headerdiv classlist");
  }
}

// TODO: componentize and DRY this function (see TheWelcome)
async function scrape_text(url){
    console.log("DO WE HAVE NO FUCKING URL??? ", url);
    if(!url){
      return;
    }  
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
    // setTimeout(()=>{console.log("jeesh")},2000);
    // clearTimeout();
    console.log("do we have a fucking url? ", url);
    let localStorageDataAvailable = localStorage.getItem(url);
    if(localStorageDataAvailable !== null){
        console.log("THIS WOULD CAUSE A PROBLEM!!");
        initialHumanReadableTextRef.value = JSON.parse(localStorageDataAvailable);
        console.log("GOT IT!!! ", initialHumanReadableTextRef.value)
          emit('closedmodal');
          emit('openedfull');

          let fullModal = await modalFull.value;
          if(fullModal && fullModal.classList){
            fullModal.classList.remove("awaiting");
            fullModal.classList.add("receivedSingleTextData");
            let main = document.getElementById("main");
            if(main){
              main.visibility = "visible";
            }
          } else {
            console.log("in else for fullmodal: ", fullModal);
          }

        let graphs = document.getElementById('graphs')
        let results = document.getElementsByClassName('modal-single-text-results')
        if(results){
          if(graphs){
            graphs.style.display = "flex";
            console.log("FLEXING GRAPHS NOW!");
          } else {
            console.log("NO GRAPHS NOW!");
            console.log("not any graphs");
          }
          if(document.getElementById('main')){
            console.log("HIDE MAIN NOW!")
            document.getElementById('main').style.display = "none";
          } else {
            console.log("no main to hide!");
            console.log("not any main");
          }
          if(document.getElementById('progressCircles')){
            console.log("HIDE PROG CIRCLES NOW!")
            document.getElementById('progressCircles').style.display = "none";
          } else {
            console.log("no progress circles");
          }
          if(document.getElementById('progressMsg')){
            console.log("HIDE PROG CIRCLES NOW!");
            document.getElementById('progressMsg').style.display = "none";
          } else {
            console.log("no progress msg");
          }
          if(document.getElementById('progressMsgExplanation')){
            document.getElementById('progressMsgExplanation').style.display = "none";
          } else {
            console.log("no progress msg explanation");
          }
          
          
          if(document.getElementById('compareButton')){
          document.getElementById('compareButton').style.visibility = "visible";
          } else {
            console.log("no compare button");
          }
          if(document.getElementById("textRowAuthor")){
            document.getElementById("textRowAuthor").style.display = "none";
          } else {
            console.log("no text row author")
          }
          if(document.getElementById("textRowTitle")){
            document.getElementById("textRowTitle").style.display = "none";
          } else {
            console.log("no textRowTitle");
          }
          if(document.getElementById("searchTextWrapper")){
            document.getElementById("searchTextWrapper").style.display = "none";
          } else {
            console.log("no search text wrapper");
          }
          // document.getElementsByClassName('wrapper-outer').classList.add("hide");
          // document.getElementsByClassName('wrapper-outer').style.display = "none";

          // document.getElementById('headerDiv').style.display = 'none';
          if(document.getElementById('headerDiv')){
            document.getElementById('headerDiv').style.visibility = 'hidden';
          } else {
            console.log("no header div");
          }
          if(document.getElementById('mainText')){
            console.log("HIDE MAIN TEXT NOW");
            document.getElementById('mainText').style.display = "none";
          } else {
            console.log("no main text");
          }
          if(document.getElementById('mainTextSubheader')){
            document.getElementById('mainTextSubheader').style.display = "none";
          } else {
            console.log("no mainTextSubheader");
          }  
        }
        return;
    } 
    // else { 
    //   // TESTING THIS OUT...
    //   emit('closedmodal');
    //   emit('openedfull');
    // }

    // console.log("do we make it here?");
  
    emit('openedfullawaitscrape');
    // setTimeout(()=>{console.log("timeout up!!!")},4000);
    // retract this when modal is closed...
    document.body.style.overflowY = "hidden";
    close();
    setTimeout(()=>{},2000);    
    clearTimeout();
    tryGetFullModal();

    console.log("CONTACT!!!");
    //document.getElementById("modal-full").classList.add("awaiting")
    rawtextfromtoc.value = await fetch('http://localhost:5000/scraper_get_text', {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      method: "POST",
      body: JSON.stringify({titleUrl: url})
    }).then(response => response.json()).then(result => {
        if(result){
          console.log("hey, got a response from server!");
          rawtextfromtoc.value = result;
          console.log("hhhere's the text: ", JSON.parse(JSON.stringify(rawtextfromtoc.value)));
          // document.getElementById("modalFull").classList.add("awaiting")
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
          temp.value.last_word_per_line.forEach((li,lineIndex)=>{
            
            initialHumanReadableTextRef.value.lineObj[JSON.parse(JSON.stringify(lineIndex))] = {};
            initialHumanReadableTextRef.value.lineObj[JSON.parse(JSON.stringify(lineIndex))]['lastWord'] = li;
            temp.value.poetic_form.forEach(form=>{
              if(form['index'] === lineIndex){
                initialHumanReadableTextRef.value.lineObj[lineIndex] = {};
              }
            })
            
            temp.value.poetic_form.forEach(pf=>{
              try {
                if(JSON.parse(JSON.stringify(pf))['index'] === JSON.parse(JSON.stringify(lineIndex))){
                  initialHumanReadableTextRef.value.lineObj[JSON.parse(JSON.stringify(lineIndex))] = {
                    "thisRhyme": JSON.parse(JSON.stringify(pf))['this_rhyme'] || '',
                    "lastRhyme": JSON.parse(JSON.stringify(pf))['last_rhyme'] || '',
                    "thisLine": JSON.parse(JSON.stringify(pf))['this_line'] || '',
                    "lastLine": JSON.parse(JSON.stringify(pf))['last_line'] || '',
                    "thisInterRhyme": JSON.parse(JSON.stringify(pf))['this_interrhyme'] || '',
                    "lastInterRhyme": JSON.parse(JSON.stringify(pf))['last_interrhyme'] || '',
                    "thisInterLine": JSON.parse(JSON.stringify(pf))['this_interline'] || '',
                    "lastInterLine": JSON.parse(JSON.stringify(pf))['last_interline'] || '',
                    "poeticForm": JSON.parse(JSON.stringify(pf))['form'] || 'None' 
                  }
                }
              } catch {
              }
            })
            temp.value.internal_rhyme_most_recent.forEach(ry=>{
              try {
                if(JSON.parse(JSON.stringify(ry))['index'] === JSON.parse(JSON.stringify(lineIndex))){
                  try {
                      initialHumanReadableTextRef.value.lineObj[JSON.parse(JSON.stringify(lineIndex))]['internalRhymes'] = {
                        "endRhyme": JSON.parse(JSON.stringify(ry))['end_rhyme'] || '',
                        "internalRhyme": JSON.parse(JSON.stringify(ry))['internal_rhyme']
                    }
                  } catch (e) {
                    console.warn("error getting internal rhymes: ", e);
                  }
                }
              } catch(e){
              console.log("error: ", e);
              } finally {
              }  
              try {
                initialHumanReadableTextRef.value.lineObj[JSON.parse(JSON.stringify(lineIndex))]['syllablesInLine'] = JSON.parse(JSON.stringify(temp.value.syllables_per_line))[lineIndex]
              } catch {
                console.log("error getting syllables in line *** ");
              }
            })         
        })
          const tempGramArr = ref([])
   
          temp.value.most_common_words.forEach((word, rank) => {
    
            initialHumanReadableTextRef.value.textObj.mostCommonWords[rank]={"word":JSON.parse(JSON.stringify(word[0])),"occurances":JSON.parse(JSON.stringify(word[1]))};
          });
         
          temp.value.sentence_id.forEach(sentence => {
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
            initialHumanReadableTextRef.value.sentenceObj[JSON.parse(JSON.stringify(wordGram))['sentence_index']]['sentenceGrammarArray'].push({
              "sentenceIndex":JSON.parse(JSON.stringify(wordGram))['sentence_index'],
              "tokenTag":JSON.parse(JSON.stringify(wordGram))['token_tag'],
              "tokenPos":JSON.parse(JSON.stringify(wordGram))['token_pos'],
              "tokenText":JSON.parse(JSON.stringify(wordGram))['token_text']
            })    
          });
          temp.value.spacy_entities.forEach(entity=>{
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
        console.log('Error:', error);
        }); 
    // }  
      return rawtextfromtoc;
};

function selected(e){
  console.log("received SELECTED emit in the modal parent: ", e);
};

const lineThickness = 3;

function colorInputMountedHandler(){
  // if(!rawtextfromtoc.value){
  //   return;
  // }
  console.log("additional texts val[0]: ", additionalTexts.value[0])
  if(currentLinesCount.value === 1){
    console.log("LINE COUNT IS ONE")
  } else if(currentLinesCount.value === 2){
    console.log("LINE COUNT IS TWO")
    
  } else if(currentLinesCount.value === 3){
    console.log("LINE COUNT IS THREE")
  } else if((currentLinesCount.value === 4)){
    console.log("LINE COUNT IS FOUR")
  } else {
    console.log("how did this happen to current lines count? ", (currentLinesCount.value === 1));
  }
    // Update Graph Keys
    if(additionalTexts.value[0].title === ''){
      additionalTexts.value[0].title = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).title;
      additionalTexts.value[0].author = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).author;
      additionalTexts.value[0].titleUrl = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).titleUrl;
    // } else if(additionalTexts.value[1].title === ''){
    //   additionalTexts.value[1].title = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).title;
    //   additionalTexts.value[1].author = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).author;
    //   additionalTexts.value[1].titleUrl = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).titleUrl;
    } else {
      //ADD OPTIONS FOR NEWLY SCRAPED TEXTS HERE
      console.log("LINE COUNT: ", currentLinesCount.value);
      additionalTexts.value[currentLinesCount.value].title = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).title;
      additionalTexts.value[currentLinesCount.value].author = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).author;
      additionalTexts.value[currentLinesCount.value].titleUrl = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)).titleUrl;
    }
    return additionalTexts.value;      
   // console.log("LOOK: ", document.getElementById("text-input-hex"));
} 

function colorPickerShowHandler(){
  console.log("showpicker mounted: ", color0.value);
  //console.log("LOOK 2: ", document.getElementById("text-input-hex"));
}
function colorChanged(){
  console.log("color changed: ", color0.value);
  console.log("HERE IS TEXT INPUT: ", document.querySelector(`.text-input`))
}
console.log("additional texts : ", additionalTexts.value)

// THESE COUNTS WILL BE USED TO INFORM KEYBUILDER & SHAPE GRAPH
function trySetDataCountXLengthMax(num){

  num = Math.max.apply(Math, num);
  console.log("in MAX X! ", num);
  console.log("why are we here??")
  console.log("WHAT THE FUDE IS THIS: ", JSON.parse(JSON.stringify(numberXMax.value))[currentLinesCount.value - 1]);
  
 if(numberXMax.value[currentLinesCount.value - 1] && num > JSON.parse(JSON.stringify(numberXMax.value))[currentLinesCount.value -1]){
    numberXMax.value[currentLinesCount.value - 1] = num;
    // if(numberXMax.value[currentLinesCount.value - 1]){
    //   console.log("xmax: ", numberXMax.value[currentLinesCount.value - 1]);
    // }
 } else {
    console.log(';whut is num: ', num);
   numberXMax.value[currentLinesCount.value - 1] = num;
    // if(numberXMax.value[currentLinesCount.value - 1]){
    //   console.log("xmax sheesh: ", numberXMax.value[currentLinesCount.value - 1]);
    // }
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
    console.log(`${numberYMin.value[currentLinesCount.value - 1]} is smaller than ${num}`)
    numberYMin.value[currentLinesCount.value - 1] = JSON.parse(JSON.stringify(numberYMin.value[currentLinesCount.value - 1]));
  }

} 

function trySetDataNameX(name){
  valueX.value=name;
  let labels = JSON.parse(JSON.stringify(optionsX.value)).map(x=>x.label);

  if(labels.indexOf(valueX.value) === -1){
      let tagX = {
        label: valueX.value,
        value: [Math.min(...JSON.parse(JSON.stringify(numberXMin.value)).filter(i=>typeof i === "number")), Math.max(...JSON.parse(JSON.stringify(numberXMax.value)).filter(i=>typeof i === "number"))],
        isIndex: xIsIndexAxis.value
      }
      optionsY.value.push(tagX)
      optionsX.value.push(tagX)
  }
  return valueX.value; 
}

function trySetDataNameY(name){
  valueY.value = name;
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

function openUpdatePopup(){

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
  console.log("WEE SHOULD BE HITTING THIS!!!! OPEN UPDATE POPUP", updatePopup);
  if(updatePopup){
    updatePopup.classList.remove("animate-close");
  }
  let updateDataBtn = document.getElementById("updatePopupButton");
  if(updateDataBtn){
    updateDataBtn.classList.add("animate-close");
  }
}

function closeUpdatePopup(){
  let wrapperTitle = document.getElementById("buttonsWrapperTitle");
  let wrapperSubtitle = document.getElementById("buttonsWrapperSubtitle");
  let wrapperBtns = document.getElementById("buttonsInnerWrapper");
  if(wrapperTitle){
    wrapperTitle.style.display = "none";
  } else {
    console.log("wrapper title missing");
  }
  if(wrapperSubtitle){
    wrapperSubtitle.style.display = "none";
  } else {
    console.log("wrapper subtitle missing");
  }
  if(wrapperBtns){
    wrapperBtns.style.display = "none";
  } else {
    console.log("wrapper btns missing");
  }
    let updatePopup = document.getElementById("d3UpdateButtonsWrapper");
    console.log("WEE SHOULD BE HITTING THIS!!!! CLOSE UPDATE POPUP", updatePopup);
    if(updatePopup){
      updatePopup.classList.add("animate-close");
    }
    let updateDataBtn = document.getElementById("updatePopupButton");
    if(updateDataBtn){
      updateDataBtn.classList.remove("animate-close");
    }
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
    keyPopupDisplay.innerText = JSON.parse(JSON.stringify(selectedXAxisRef.value)).label;
    xIsIndexAxis.value = JSON.parse(JSON.stringify(selectedXAxisRef.value)).isIndex;
    if(xIsIndexAxis.value){
      document.getElementById("xRangeDisplay").classList.add("is-index-axis");
    } else {
      document.getElementById("xRangeDisplay").classList.remove("is-index-axis");
    }
  } else {
    alert("no keybuilder div!");
  }
}

function selectYAxis(event){
  let keyPopupDisplay = document.querySelector('#newRow_Y > .rangeDisplay');
  if(keyPopupDisplay){
    keyPopupDisplay.innerText = JSON.parse(JSON.stringify(selectedYAxisRef.value)).label;
    yIsIndexAxis.value = JSON.parse(JSON.stringify(selectedYAxisRef.value)).isIndex;
    console.log("???? ", yIsIndexAxis.value);
    if(yIsIndexAxis.value){
      document.getElementById("yRangeDisplay").classList.add("is-index-axis");
    } else {
      document.getElementById("yRangeDisplay").classList.remove("is-index-axis");
    }
  }
}

function clickedLineRow(row){
  // alert('works!')
  console.log("is this hitting row: ", row);
  let sel = document.querySelector(`.selectedLine`);
  console.log("check on sel: ", sel);
  if(sel){
    console.log("selected: ", sel);
    sel.classList.remove("selectedLine");
  }
  if(row>0){
  let newSel = document.getElementById(`newRow_${row}`);
  console.log("check on newSel: ", newSel);
  newSel.classList.add('selectedLine');
  } else {
      let newSel = document.getElementById(`newRow_${row}`);
  console.log("check on newSel for zero: ", newSel);
  newSel.classList.add('selectedLine');
  }
  console.log("row: ", row);
  selectedRow.value = row;

  console.log('check on selected row in modal: ', selectedRow.value)
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
      <header class="modal-header">
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
            class="btn-green"
            @click="tryAddNewText"
          >
            Return
          </button>
          <button
            type="button"
            id="compareButton"
            class="btn-green"
            @click="openKeyPopup"
          >
            Key
          </button>
     
        <button
          type="button"
          class="btn-close"
          @click="doCloseFullModalChild"
        >
          x
        </button>
      </header>

      <section id="graphs">
        <slot  name="graphs">
 
          <GraphModal 
            :graphstate="graphstateRef" 
            :dataObj="initialHumanReadableTextRef" 
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
            @resetXMaxReadOnly="updateReadOnlyXMax"
            @resetYMaxReadOnly="updateReadOnlyYMax"
            @resetXMinReadOnly="updateReadOnlyXMin"
            @resetYMinReadOnly="updateReadOnlyYMin"
            @dataname_x="trySetDataNameX"
            @dataname_y="trySetDataNameY"

          ></GraphModal>
        </slot>
      </section>
      <section class="linePickerPopup">
        <slot>            
          <div id="newTextPopup" >
            <span id="newTextPopupTitle">Create Key <span id="keySelectorClose" @click="closeKeyModal">X</span></span>
            <!-- v-if="additionalTexts" v-for="item in additionalTexts" :key="item.titleUrl"  -->
            <td id="keyPopupCols" class="new-text-popup-row">
              <tr class="new-text-text">Text</tr>
              <tr class="rangeDisplay">Values</tr>
              <tr class="new-text-viz-variable">Display</tr>
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
              <tr class="rangeDisplay">
                <span class="rangeDisplayRow">
                  X-Range: <span id="xRangeDisplayXMin_0"></span> - <span id="xRangeDisplayXMax_0"></span> 
                </span>
                <span class="rangeDisplayRow">
                  Y-Range: <span id="yRangeDisplayYMin_0"></span> - <span id="yRangeDisplayYMax_0"></span>
                </span>              
              </tr>
          
              <tr id="newVariable_0" class="new-text-viz-variable">
                <span id="newVariable_0_xvar">{{additionalTexts[0].variableX}}</span>
                <!-- <span>{{JSON.parse(JSON.stringify(axisColorMatchBool)).value}}</span> -->
                <span id="newVariable_0_yvar">{{additionalTexts[0].variableY}}</span>
              </tr>
              <tr class="color-wrapper">
                <color-input id="colorInput_0" class="color-input" v-model="color0" position="left" ref="colorInput_0" changed="colorChanged()" @mounted="colorInputMountedHandler" @pickStart="colorPickerShowHandler"/>
              </tr>
            </td> 

            <td @click="clickedLineRow(1)" id="newRow_1" class="new-text-popup-row">
              <tr id="newText_1" class="new-text-text">
                <span id="newAuthor_1" class="new-text-author">
                {{additionalTexts[1].author}}
              <!-- {{item.author}} -->
                </span>
                <span id="newTitle_1" class="new-text-title">
                  {{additionalTexts[1].title}}
                </span>
              </tr>
              <tr class="rangeDisplay">
                <span class="rangeDisplayRow">
                  X-Range: <span id="xRangeDisplayXMin_1"></span> - <span id="xRangeDisplayXMax_1"></span>
                </span>
                <span class="rangeDisplayRow">
                  Y-Range: <span id="yRangeDisplayYMin_1"></span> - <span id="yRangeDisplayYMax_1"></span> 
                </span>
              </tr>
              <tr id="newVariable_1" class="new-text-viz-variable">
                <span id="newVariable_1_xvar">{{additionalTexts[1].variableX}}</span>
                <span id="newVariable_1_yvar">{{additionalTexts[1].variableY}}</span>
              </tr>
              <tr class="color-wrapper">
                <color-input id="colorInput_1" class="color-input" v-model="color1" position="left" ref="colorInput_1" changed="colorChanged" @mounted="colorInputMountedHandler" @pickStart="colorPickerShowHandler"/>
              </tr>
            </td> 

            <td @click="clickedLineRow(2)" id="newRow_2" class="new-text-popup-row">
              <tr id="newText_2" class="new-text-text">
                <span id="newAuthor_2" class="new-text-author">
                {{additionalTexts[2].author}}
                </span>
                <span id="newTitle_2" class="new-text-title">
                  {{additionalTexts[2].title}}
                </span>
              </tr>
              <tr class="rangeDisplay">
                <span class="rangeDisplayRow">
                  X-Range: <span id="xRangeDisplayXMin_2"></span> - <span id="xRangeDisplayXMax_2"></span>
                </span>
                <span class="rangeDisplayRow">
                  Y-Range: <span id="yRangeDisplayYMin_2"></span> - <span id="yRangeDisplayYMax_2"></span> 
                </span>
              </tr>
              <tr id="newVariable_2" class="new-text-viz-variable">
                  <span id="newVariable_2_xvar">{{additionalTexts[2].variableX}}</span>
                  <span id="newVariable_2_yvar">{{additionalTexts[2].variableY}}</span>
              </tr>
              <tr class="color-wrapper">
                <color-input id="colorInput_2" class="color-input" v-model="color2" position="left" ref="colorInput_2" changed="colorChanged" @mounted="colorInputMountedHandler" @pickStart="colorPickerShowHandler"/>
              </tr>
            </td> 

            <td @click="clickedLineRow(3)" id="newRow_3" class="new-text-popup-row">
              <tr id="newText_3" class="new-text-text">
                <span id="newAuthor_3" class="new-text-author">
                {{additionalTexts[3].author}}
              <!-- {{item.author}} -->
                </span>
                <span id="newTitle_3" class="new-text-title">
                  {{additionalTexts[3].title}}
                </span>
              </tr>
              <tr class="rangeDisplay">
                <span class="rangeDisplayRow">
                  X-Range: <span id="xRangeDisplayXMin_3"></span> - <span id="xRangeDisplayXMax_3"></span>
                </span>
                <span class="rangeDisplayRow">
                  Y-Range: <span id="yRangeDisplayYMin_3"></span> - <span id="yRangeDisplayYMax_3"></span> 
                </span>
              </tr>
              <tr id="newVariable_3" class="new-text-viz-variable">
                  <span id="newVariable_3_xvar">{{additionalTexts[3].variableX}}</span>
                  <span id="newVariable_3_yvar">{{additionalTexts[3].variableY}}</span>
              </tr>
              <tr class="color-wrapper">
                <color-input id="colorInput_3" class="color-input" v-model="color3" position="left" ref="colorInput_3" changed="colorChanged" @mounted="colorInputMountedHandler" @pickStart="colorPickerShowHandler"/>
              </tr>
            </td> 
              
            <td id="newRow_X" class="new-text-popup-row">
              <tr id="newText_X" class="new-text-text">
              Create X-Axis
              </tr>
              <tr class="rangeDisplay">
                X-Range: 
                <span class="rangeDisplayRow">
                  <span id="xAxisRangeDisplayMax"></span>
                  <span id="xAxisRangeDisplayMin"></span>
                </span>
              </tr>
              <tr id="newVariable_X" class="new-text-viz-variable">
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
              </tr>
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
                Y-Range: 
                <span class="rangeDisplayRow">
                  <span id="yAxisRangeDisplayMax"></span>
                  <span id="yAxisRangeDisplayMin"></span>
                </span>
              </tr>
              <tr id="newVariable_Y" class="new-text-viz-variable">
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
              </tr>
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
      <section class="modal-body">

        <slot name="body">   
          <!-- <self-building-square-spinner
            v-if="!props.rawtextdata" 
            id="squareBuilderAnim"
            :animation-duration="6000"
            :size="48"
            color="rgba(255,255,255,1)"
          /> -->
        <!-- </slot> -->
          <section class="modal-textAnalysis-title">
            <slot name="titleDiv">
              <span id="textRowTitle">
                Title: {{props.selectedTitle}}
              </span>
              <span id="textRowAuthor">
                Author: {{props.selectedAuthor}}
              </span>
            </slot>
          </section>
          <section class="progress-circle-section" id="progressCircles">
            <slot name="progressCircles">
              <step-progress icon-class="fa fa-square-check" :steps="mySteps" :current-step="currentStepRef" active-color="hsla(160, 100%, 37%, 0.7)" :line-thickness="1"> </step-progress>
            </slot>
          </section>

          <section id="progressMsg" class="progress-msg">
            <slot name="progressMsg">
              <!-- {{stepMessage}} -->
            </slot>
          </section>

          <section id="progressMsgExplanation" class="progress-msg-explanation">
            <slot name="progressMsgExplanation">
            <!-- <h4>Progress Msg Explanation</h4> -->
            <p>Lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum </p>
              <!-- {{stepMessage}} -->
            </slot>
          </section>

          <section class="modal-single-text-results">
            <slot name="textAnalysis-results">

                <div id="fullTextGraphWrapper" class="results-col">
                  Yo full text

                </div>
                <div class="results-col">
                  Yo sentences
                </div>
                <div class="results-col">
                  Yo Lines
                </div>
            </slot>
          </section>
        </slot>
      </section>

      <footer class="modal-footer">
        <slot name="footer">
          <!-- <button
            type="button"
            id="compareButton"
            class="btn-green"
            @click="openKeyPopup"
          >
          Extend
        </button> -->
          <!-- <button
            type="button"
            id="additiveButton"
            class="btn-green"
            @click="additiveMode"
          >
          Additive
        </button> -->
        </slot>

      </footer>
    </div>
  </div>
  <div v-if="open" ref="modal" class="modal" :class="open ? 'searching' : 'not-searching'">
    <button id="closeBtn" @click="$emit('closedmodal')"
    >Close</button>
    <h1 id="tocHeader">Table of Contents</h1>
    <span id="tocSubtitle">Click any link below to load the text</span>
    <div id="tocDataWrapper">
        <div id="tocData" v-for="item in props.tocdata">
            <i icon-class="fa-solid fa-ellipsis" />
            <!-- <h3 @click="scrape_text(item.link_href)">{{ -->
            <h3 @click="scrape_text(item.link_href)">{{
                item.link_text
            }}</h3>

        </div>
    </div>

    <!-- can we remove this??? -->
    <!-- <div id="textData">
    {{rawtextfromtoc ? rawtextfromtoc.value : null}}
    </div> -->

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
  z-index: 10;
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
    top: 0%;

    align-items: center;
    left: 0%;
    grid-template-columns: 1fr;
    width: 50%;
    height: 100vh;
    animation: animate-text-scrape 1s linear;
    background: var(--color-background);
    backdrop-filter: blur(8px);
    overflow-y: scroll;
}
  #squareBuilderAnim {
    transform: rotateX(3.142rad);
    top: 80px;   
    margin-left: 48%;
  }
#closeBtn {
    right: 12px;
    position: absolute;
    color: rgba(255,255,255,0.9);
    z-index: 1001;
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
    font-family: 'Inter' sans-serif;
    font-style:italic;
    margin-bottom: 0.1rem;
    font-weight: 500;
    cursor: pointer;
    color: var(--color-heading);
    padding-top: 12px;
}
#tocDataWrapper {
    margin: 12px;
    margin-top: 16px;
    padding-left: 24px;
    padding-right: 24px;
}

#modalFull {
    background:transparent;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
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
    background: var(--color-background);
    pointer-events:all;
    align-items: left;
}

.rangeDisplayRow {
  flex-direction:row;
  display:flex;
}



.modal.not-searching {
  background: teal;
  overflow-y: hidden;
}

#modalFull.receivedSingleTextData {

}

  .modal-header,
  .modal-footer {
    width: 100vw;
  /*  padding: 15px; */
    display: flex;
  }

  .modal-footer {
    padding: 16px;
  }

  .modal-header {
    width: 100%;
    position: absolute;
    z-index: 40;
    height: 68px;

    font-size: 48px;
    font-weight: 100;
    top: 0px;
    left: 0px;
    background: rgba(255, 255, 255, 0.078);
    transition: height 1s ease-in;
  }

  .modal-footer {
    border-top: 1px solid #eeeeee;
    flex-direction: row;
    justify-content: flex-end;
    background: rbga(0,0,0,1);
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
    background: rgba(0,0,0,0.4);
    justify-content: center;
    left: 16%;
    right: 16%;
    width: 68%;
    height: 16%;
    border-radius: 8px;
    bottom:30px;
  }
  .btn-close {
    position: absolute;
    display:none;
    top: 0;
    right: 0;
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
    background: hsla(193, 82%, 49%, 0.7);
    border: 1px solid hsla(160, 100%, 37%, 0.7);
    border-radius: 2px;
    width: 80px;
    height: 48px;
    float: right;
    margin-right:4px;
    margin-left:4px;
    position: absolute;
    right: 36px;
    top: 12px;
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
    top: -60px !important;
    position: absolute;
  }
  #textRowTitle, #textRowAuthor{
    width: 100%;
  }

  .modal-textAnalysis-title {
    /* this is the overarching modal */
    padding-left: 4%;
    padding-right: 4%;
    position: absolute;
    background: var(--color-background);
    height: calc(100% - 164px);
  }
  .modal-single-text-results {
    width: 100%;
    display: flex;
    text-align: center;
    top: 36px;
    visibility: hidden;
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
  #progressMsg {
    position: relative;
    z-index: 1;
    bottom: 0px;
    font-size: 28px;
    text-align: center;
    bottom:40px;
  }
  .step-progress__wrapper {
    width: 90vw;

  }
  .step-progress__step--active span {
   
    color: "#ffffff";
    z-index: 10;
  }
  .check-square-o {
    z-index: 10;
    font-family: "untitled-font-1";
    src: url("./untitled-font-1.svg#untitled-font-1") format("svg");
    
    z-index: 10;
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
  top: 45%;
  
}
.progress-msg {
  width:100%;
  z-index: 1;
}


#topBtns {
  visibility: hidden;
}
#compareButton {
  
}
#addTextButton {
  right: 128px;
}

#graphs {
  display: none;
  width: 100%;
  height: auto;
}
#newTextPopup {
  display:none;
  flex-direction: column;
  left: 0%;
  bottom: 0%;
  top: 0%;
  padding: 105px;
  background: rgba(0,0,0,.9);
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

.linePickerPopup {
  background-color:var(--color-background);
  background:var(--color-background);
  color: #ffffff;
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
}
.new-text-text {
  flex-direction: column;
  display: flex;
  width:35%;
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
  background:rgba(255,255,255,0.078);

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
  background: rgba(255,255,255,0.078);
}
.key-popup {
  width: 50%;
  background-color: hsla(160, 100%, 37%, 1);
  color: #181818;
  height: 48px;
  margin: 16px;
}
#newRow_1, #newRow_2, #newRow_3 {
  display:none;
}
.hide {
  display: none;
}
#updatePopupButton {
  right: 220px;
}
#newAxis_X, #newAxis_Y {

}
button.green-btn {
  min-width: 160px;
  font-size: 14px;
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
}
.is-index-axis {

  background: hsla(160, 100%, 37%, 1);
}
.selectedLine {
  border: solid 2px hsla(160, 100%, 37%, 1);
}

</style>
<style src="@vueform/multiselect/themes/default.css"></style>