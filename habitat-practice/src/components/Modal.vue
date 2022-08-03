<script setup>
import { ref, watch, onMounted, watchEffect } from 'vue'
import { SelfBuildingSquareSpinner  } from 'epic-spinners'
import StepProgress from 'vue-step-progress';
import './untitled-font-1.svg'
// import the css (OPTIONAL - you can provide your own design)
import 'vue-step-progress/dist/main.css';
import { Head } from '@vueuse/head'
import LineChart from './LineChart.vue';
import StackedAreaChart from './StackedAreaChart.vue';
import GraphModal from './GraphModal.vue'
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


const socket = new WebSocket('ws://localhost:5000/ws');

socket.onopen = function (event) {
  socket.send("Here's some text that the server is urgently awaiting!");
}

const mySteps = ['Text', 'Lines', 'Sentences', 'Vectors', 'Clusters', "Features"]

// const mySteps = ['Scrape and Process Text', 'Analyze Lines', 'Analyze Sentences', 'Analyze Entities']

let stepMessage = '';


socket.onmessage = event => {

    if(event.data === 'third_msg'){
      currentStepRef.value = 0;
      stepMessage = "Gathering text and preprocessing data"
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
    }
    if(event.data === 'fourth_msg'){
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

    // if(event.data === 'tenth_msg'){
    //   currentStepRef.value = 3;
    //   stepMessage = "Begin entity analysis";
    //   if(document.getElementById("progressMsg")){
    //     document.getElementById("progressMsg").innerText = stepMessage;
    //   }
    // }
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
    // if(event.data === 'fourteenth_msg'){
    //   currentStepRef.value = 7;
    //   stepMessage = "Beginning _plots?"
    //   if(document.getElementById("progressMsg")){
    //     document.getElementById("progressMsg").innerText = stepMessage;
    //   }
    // }  
    if(event.data === 'fifteenth_msg'){
      currentStepRef.value = 6;
      console.log("HIT FIFTEENTH!!!");
      stepMessage = "Feature Extraction"
      if(document.getElementById("progressMsg")){
        document.getElementById("progressMsg").innerText = stepMessage;
      }
      let results = document.getElementsByClassName('modal-single-text-results');
      if(results.length > 0){
        results[0].style.visibility = "visible";
        document.getElementById('progressCircles').style.display = "none";
        document.getElementById('progressMsg').style.display = "none";
        document.getElementById('progressMsgExplanation').style.display = "none";
        // emit('closedfull')
        document.getElementById('graphs').style.display = "flex";
      }
    }  
    let showExplanation = document.getElementById('progressMsgExplanation')
    if(showExplanation){
      showExplanation.style.display = "flex";
    }
}

const props = defineProps({
  open: Boolean,
  openFull: Boolean,
  tocdata: Object,
  rawtextdata: String,
  selectedTitle: String,
  selectedAuthor: String,
});

const temp = ref({})
  
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
      laastInterLine: String,
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

const rawtextfromtoc= ref({});

const emit = defineEmits(['closedmodal','openedfullawaitscrape','openedfull','closedfull'])

watch(() => props.selected,(tocdata,rawtextdata,selectedTitle,selectedAuthor) => {
      console.log(
        "Here Watch props.selected function called with args:",
        tocdata,
        rawtextdata,
        selectedTitle,
        selectedAuthor
      );
    });

// CREATE FULLSCREEN MODAL HERE ...

const modalFull = ref(null);
const modal = ref(null);

function tryGetFullModal(){
    setTimeout(()=>{
      let fullModal = modalFull.value;
      emit('closedmodal')
      if(fullModal && fullModal.classList){
        fullModal.classList.add("awaiting");
        let main = document.getElementById("main");
        if(main){
          main.visibility = "hidden";
        }
      } else {
        console.log("what is the else for full modal? ", fullModal);
      }
    },10)
    clearTimeout();
  };

function doCloseFullModalChild(){
  emit('closedfull')
  let headerDiv = document.getElementById("headerDiv");
  if (headerDiv && headerDiv.classList){
    headerDiv.classList.add("noDisplay");
  } else {
    console.log("in the else for headerdiv classlist");
  }
}

// TODO: componentize and DRY this function (see TheWelcome)
async function scrape_text(url){    
    
    emit('openedfullawaitscrape');
    // retract this when modal is closed...
    document.body.style.overflowY = "hidden";
    // close();
    setTimeout(()=>{},2000);
    clearTimeout();
    tryGetFullModal();

    
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
            initialHumanReadableTextRef.value.sentenceObj[JSON.parse(JSON.stringify(wordGram))['sentence_index']].sentenceGrammarArray.push({
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
            // TODO => do we need entities in the text obj (or do we need them here?)
            // initialHumanReadableTextRef.value.textObj.spacyEntities.push(
            //   {
            //     "text": Object.keys(JSON.parse(JSON.stringify(Object.values(Object.values(entity))))[0])[0],
            //     "type": Object.values(JSON.parse(JSON.stringify(Object.values(Object.values(entity))))[0])[0],
            //   }
            // )

          })






          console.log("tEEEEEDST: ", JSON.parse(JSON.stringify(initialHumanReadableTextRef.value)))
          //let finalObj = JSON.parse(JSON.stringify(initialHumanReadableTextRef.value));
          // document.getElementById('fullTextGraphWrapper').innerText = (finalObj.textObj);

          ///////////////////////////////////////////////////////////////////////////////
          ///////////////////////////////////////////////////////////////////////////////
          ///////////////////////////////////////////////////////////////////////////////
          
          let fullModal = modalFull.value;
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
          return rawtextfromtoc.value;
        } else {
          return null;
        }
        }).catch(error => {
        console.log('Error:', error);
        }); 
      return rawtextfromtoc;
};

// function handleSelect(e){
//   console.log("e t v ", e);
// }
const lineThickness = 5;
</script>

<template>
  <Head>
    <!-- <title>Hello World</title> -->
    <base href="/base" />
    <html lang="en-US" class="theme-dark" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.2/css/all.min.css" integrity="sha512-1sCRPdkRXhBV2PBLUdRb4tMg1w2YPf37qatUFeS7zlBy7jJI8Lf4VHwWfZZfpXtYSLy85pkm9GaYVYMfw5BC1A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  </Head>
<Teleport to="body">
  <div v-if="openFull" class="full-screen-modal modal-backdrop">
    <div id="modalFull" ref="modalFull">
      <header class="modal-header">
        <slot name="header">
          Single Text Analysis
        </slot>

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
 
          <GraphModal :dataObj="initialHumanReadableTextRef" :dataKey="'occurances'"></GraphModal>
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
              <span class="text-row">
                Title: {{props.selectedTitle}}
              </span>
              <span class="text-row">
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
          <button
            type="button"
            id="compareButton"
            class="btn-green"
            @click="close"
          >
          Compare
        </button>
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
    <!-- <p id="textData">{{rawtextfromtoc ? rawtextfromtoc.value : null}}</p> -->
    <div id="textData">
    {{rawtextfromtoc ? rawtextfromtoc.value : null}}
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


/*.modal-backdrop {
  pointer-events:none;
}*/

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





.modal.not-searching {
  background: teal;
  overflow-y: hidden;
}

#modalFull.receivedSingleTextData {
    background:blue;
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
    padding-left: 40px;
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
    top:72px;
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
    display: none;
    bottom:30px;
  }
  .btn-close {
    position: absolute;
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
    background: hsla(160, 100%, 37%, 0.7);;
    border: 1px solid hsla(160, 100%, 37%, 0.7);;
    border-radius: 2px;
    width: 200px;
    height: 60px;
    float: right;
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
  .text-row {
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
/*    font-family: "untitled-font-1";
    src: url("./untitled-font-1.svg#untitled-font-1") format("svg");*/
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



#compareButton {
  visibility: hidden;
}

#graphs {
  display: none;
  width: 100%;
  height: auto;
  top: 72px;
}

</style>