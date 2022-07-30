<script setup>
import { ref, watch, onMounted, watchEffect } from 'vue'
import { SelfBuildingSquareSpinner  } from 'epic-spinners'
import StepProgress from 'vue-step-progress';

// import the css (OPTIONAL - you can provide your own design)
import 'vue-step-progress/dist/main.css';



const currentStepRef = ref(null);
let currentStep = 0;
onMounted(()=>{
  currentStepRef.value = 0;
})

watchEffect(() => {
  if (currentStepRef.value) {
    console.log("I FUCKING HATE VUE: ", currentStepRef.value)
    currentStep = currentStepRef.value;
    console.log("what the fuck is currentStep ", currentStep);
    return currentStep;
  } else {
    // not mounted yet, or the element was unmounted (e.g. by v-if)
  }
})



const socket = new WebSocket('ws://localhost:5000/ws');

socket.onopen = function (event) {
  socket.send("Here's some text that the server is urgently awaiting!");
}

const mySteps = ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5', 'Step 6','Step 7','Step 8','Step 9','Step 10','Step 11','Step 12','Step 13']

// socket.addEventListener('message', ev => {
//   console.log("EVENT DATA ", ev.data);

let stepMessage = '';

// });

socket.onmessage = event => {
  console.log(`WHAT THE FUCK??? ${event.data} AND ${typeof event.data}`);

    if(event.data === 'first_msg'){
      currentStepRef.value = 1;
      console.log("door");
      currentStep = 1;
      stepMessage = "gecko's garage is so cool";

      // if(document.getElementById("progressMsg")){
      //   document.getElementById("progressMsg").innerText = stepMessage;
      // }
      // return currentStepRef.value;
    }
    if(event.data === 'second_msg'){
      currentStepRef.value = 2;
      console.log("guitar");
      stepMessage = "Bobby the bus had a pump to do!"
      // document.getElementById("progressMsg").innerText = stepMessage;
      console.log("WHAT IS GODDAM STEP MSG: ", stepMessage);
      console.log("GOFDAM what is count: ", currentStepRef.value);
      currentStep = 2;
      // return currentStepRef.value;
    }
    if(event.data === 'second_msg'){
      currentStepRef.value = 3;
      currentStep = 3;
      stepMessage = "Sammy the schoolbus ran out of fuel";
      // document.getElementById("progressMsg").innerText = stepMessage;
      console.log("fan");
      // return currentStepRef.value;
    }
    if(event.data === 'fourth_msg'){
      currentStepRef.value = 4;
      currentStep = 4;
      console.log("pants");
      // stepMessage = "Vicky the Van needed a hammer to fix her windscreen";
      document.getElementById("progressMsg").innerText = stepMessage;
      // return currentStepRef.value;
    }
    if(event.data === 'fifth_msg'){
      currentStepRef.value = 5;
      currentStep = 5;
      console.log("foot");
      stepMessage = "Sid had great time digging in the muck";
      // return currentStepRef.value;
      // document.getElementById("progressMsg").innerText = stepMessage;
    }
    if(event.data ===  'sixth_msg'){
      currentStepRef.value = 6;
      currentStep = 6;
      console.log("shelf");
      stepMessage = "Eric had a great time digging up loose rock";
      // return currentStepRef.value; 
      // document.getElementById("progressMsg").innerText = stepMessage;
    }
    if(event.data === 'seventh_msg'){
      currentStepRef.value = 7;
      currentStep = 7;
      console.log("mouse");
      stepMessage= "Dylan had a difficult time digging up loose rock";
      //return currentStepRef.value;
      // document.getElementById("progressMsg").innerText = stepMessage;
    }
    if(event.data === 'eighth_msg'){
      currentStepRef.value = 8;
      currentStep = 8;
      console.log("shakers");
      stepMessage = "Ryan the wrecking ball crane had a great time smashing down the walls";
      // return currentStepRef.value;
      console.log("WTF IS SELF: ", self);
      //document.getElementById("progressMsg").innerText = stepMessage;
    }
    if(event.data === 'ninth_msg'){
      currentStepRef.value = 9;
      currentStep = 9;
      console.log("computer");
      stepMessage = "Caroline had a great time picking up beams and blocks";
      //document.getElementById("progressMsg").innerText = stepMessage;
      //return currentStepRef.value;
    }
    if(event.data === 'tenth_msg'){
      currentStepRef.value = 10;
      currentStep = 10;
      console.log("pillow");
      stepMessage = "Rick had a time loosening some gravel";
      //return currentStepRef.value;
      //document.getElementById("progressMsg").innerText = stepMessage;
    }
    if(event.data === 'eleventh_msg'){
      currentStepRef.value = 11;
      currentStep = 11;
      console.log("pear");
      stepMessage = "Leo the limo had a great time styling his movies";
      // return currentStepRef.value;
      ///document.getElementById("progressMsg").innerText = stepMessage;
    }
    if(event.data === 'twelfth_msg'){
      currentStepRef.value = 12;
      currentStep = 12;
      console.log("MOM!!!!");
      stepMessage = "Trevor had a great time cutting down crops";
      //return currentStepRef.value;
      ///document.getElementById("progressMsg").innerText = stepMessage;
    }
    if(event.data === 'thirteenth_msg'){
      currentStepRef.value = 13;
      currentStep = 13;
      console.log("toes");
      stepMessage = "Celia only mixes muck, but Mia only digs it";
      // return currentStepRef.value;
      ///document.getElementById("progressMsg").innerText = stepMessage;
    }
    // else {
    //   console.log("why nothing here in step conditionals");
    //   console.log("event data is ", event.data);
    // }
  // } 
  
}

// console.log("FUUUUUUCK: ", self)

const props = defineProps({
  open: Boolean,
  openFull: Boolean,
  tocdata: Object,
  rawtextdata: String,
  selectedTitle: String,
  selectedAuthor: String,
  
});

// const mySteps = ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5', 'Step 6','Step 7','Step 8','Step 9','Step 10','Step 11','Step 12','Step 13']
// const currentStep = ref(0);
const temp = ref({})

console.log("blannnnket mmmmmmmmmmmmmmmmmmmmaaaaaaaaaaaaaammmmmmmmmmmmmmmaaaaa");

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

  // sentenceIndex: Number,
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
  // sentencesArray: Array,
})

// initialHumanReadableTextRef.value.textObj.spacyEntitiesArray = [];
initialHumanReadableTextRef.value.textObj.mostCommonWords = [];

const rawtextfromtoc= ref({});
console.log("HERE IS TOC: ", props.tocdata);
console.log("HERE IS RAW TEXT: ", rawtextfromtoc.value)
// console.log("HERE IS RAW TITLE: ", props.selectedTitle)


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

let searchModal;
onMounted(()=>{
  setTimeout(() => {
    searchModal = modal.value;
  }, 10)
})

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
  // CALL FULL SCREEN MODAL FUNCTION HERE ...
    
    emit('openedfullawaitscrape');
    // retract this when modal is closed...
    document.body.style.overflowY = "hidden";
    close();
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


          console.log("tEEEEEDST: ", initialHumanReadableTextRef.value)
          


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

</script>

<template>

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
      <div id="progressMsg">
    <!-- {{currentStepDynamicRef.value}} -->
    {{this.stepMessage}}
      </div>
      <div id="FUCK2">
      {{this.currentStep}}
      </div>
      <div id="progressCircles">
      {{"AHHHHHHHH ", currentStep}}
        <step-progress :steps="mySteps" :current-step="currentStepRef" icon-class="fa fa-check"> </step-progress>
      
      </div>
      <section class="modal-textAnalysis-title">
        <div id="FUCK"> 
          {{this.currentStep}}

        </div>
        <slot name="titleDiv">
            <span class="text-row">
              Title: {{props.selectedTitle}}
            </span>
            <span class="text-row">
              Author: {{props.selectedAuthor}}
            </span>
        </slot>
      </section>

      <section class="modal-single-text-results">
        <slot name="textAnalysis-results">
            <div class="results-col">
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
      <!-- <section class="modal-textAnalysis">
        <slot name="textDataDiv">
          <span class="text-row">
            Text Data
          </span>
          <span class="text-row">
            Text Data
          </span>
        </slot>
      </section> -->

      <!-- <section class="modal-textAnalysis"> -->
        <!-- <slot name="sentencesDataDiv">
          <span class="text-row">
            Sentences Data
          </span>
          <span class="text-row">
            Sentences Data
          </span>
        </slot>
      </section>

      <section class="modal-textAnalysis">
        <slot name="linesDataDiv">
          <span class="text-row">
            Lines Data
          </span>
          <span class="text-row">
            Lines Data
          </span>
        </slot>
      </section> -->
    
      <section class="modal-body">
        <slot name="body">
     
        
          <self-building-square-spinner
            v-if="!props.rawtextdata" 
            id="squareBuilderAnim"
            :animation-duration="6000"
            :size="48"
            color="rgba(255,255,255,1)"
          />
        </slot>
       </section>

      <footer class="modal-footer">
        <slot name="footer">
                  <button
          type="button"
          class="btn-green"
          @click="close"
        >
          Close Modal
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
body.modal-open {
  overflow-y: hidden;
  height: 100vh;
}
.modal {
    position: fixed;
    z-index: 999;
    top: 0%;
    bottom: 0%;
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
    font-family: 'Inter' Helvetica sans-serif;
    font-style:italic;
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



.modal.searching {

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
    padding: 1% 1%;
    max-width: 100%;
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
    top: 72px;
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
  }
  .results-col {
    width:33vw;
    background: green;
    margin-left: 8px;
    margin-right: 16px;
    min-height: 200px;
    border-radius: 8px;
    cursor: progress; 
    background: 
      linear-gradient(0.25turn, transparent, green, transparent),
      linear-gradient(green, var(--color-background)),
      radial-gradient(38px circle at 19px 19px, #eee 50%, transparent 51%),
      linear-gradient(green, var(--color-background));  
    background-repeat: no-repeat;

    background-position: -315px 0, 0 0, 0px 190px, 50px 195px; 
    animation: loading 1.5s infinite;
  }
  
  .step-progress, .step-progress__step, .step-progress__step.step-progress__step--active, .step-progress__step--active span   {
    margin:16px;
    --activeColor: green;
    color:green !important;
    background: black;
    --activeColor:blue !important; 
    --passiveColor:gray; 
    --activeBorder:5px; 
    --passiveBorder:5px;
  }
  .step-progress__wrapper {
    position: absolute;
  }
  #progressCircles {
    width: 100%;
  }
  #progressMsg {
    position: absolute;
    z-index: 1;
    bottom: 0px;
    font-size: 28px;
  }
  .step-progress__step--active span {
    color: "#ffffff";
  }
  #FUCK {
    index: 9999;

  }
</style>