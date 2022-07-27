<script setup>
import { ref, watch, onMounted } from 'vue'
import { SelfBuildingSquareSpinner  } from 'epic-spinners'
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
      sanityLineId: Number,
      poeticForm: String,
      thisRhyme: String,
      lastRhyme: String,
      internalRhymes: Array,
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

watch(() => props.selected, (tocdata, rawtextdata,selectedTitle,selectedAuthor) => {
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
          ///////////////////////////////////////////////////////////////////////////////
          ///////////////////////////////////////////////////////////////////////////////
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
          

          // if(0 < lineIndex < (lineIndex-1)){
              // initialHumanReadableTextRef.value.lineObj[lineIndex-1] = {
              //   sanityLineId: JSON.parse(JSON.stringify(temp.value.poetic_form))[lineIndex-1]['index'],
              // }
            try{
              console.log("IS THIS GIVING US WHAT WE NEED for form?? ", JSON.parse(JSON.stringify(temp.value.poetic_form))[lineIndex]['form']);
              console.log(`HEEERERE: (wtf is lineIndex ${lineIndex-1}) `)
              initialHumanReadableTextRef.value.lineObj[lineIndex-1] = {
              sanityLineId: JSON.parse(JSON.stringify(temp.value.poetic_form))[lineIndex-1]['index'],
              poeticForm: JSON.parse(JSON.stringify(temp.value.poetic_form))[lineIndex-1]['form'],
              thisRhyme: JSON.parse(JSON.stringify(temp.value.poetic_form))[lineIndex-1]['this_rhyme'],
              lastRhyme: JSON.parse(JSON.stringify(temp.value.poetic_form))[lineIndex-1]['last_rhyme'],
              internalRhymes: [],
              syllablesInLine: JSON.parse(JSON.stringify(temp.value.syllables_per_line))[lineIndex-1]
            }
            } catch(e) {
              console.info("error is ", e)
            } finally {
              console.log("and here's the line we're at... ", lineIndex)
            }


            temp.value.internal_rhyme_most_recent.forEach(ry=>{
              try {
                if(JSON.parse(JSON.stringify(ry.index)) === lineIndex-1){
                  console.log(`hit a match! ${lineIndex-1} and ${JSON.parse(JSON.stringify(ry.index))}`)
                  // console.log("WHAT IS GOD DAMN INTERNAL RHYMES: ", initialHumanReadableTextRef.value.lineObj[lineIndex].internalRhymes);
                  console.log("FFFFUUUUCK WHAT IS THIS ", JSON.parse(JSON.stringify(initialHumanReadableTextRef.value.lineObj[lineIndex])).internalRhymes);
                  JSON.parse(JSON.stringify(initialHumanReadableTextRef.value.lineObj))[lineIndex]['internalRhymes'].push({
                    "endRhyme": JSON.parse(JSON.stringify(ry.end_rhyme)),
                    "internalRhyme": JSON.parse(JSON.stringify(ry.internal_rhyme))
                  })

                }
              } catch(e){
              console.log("error: ", e);
            } finally {
              console.log("what is internal rhymes looking like? ", JSON.parse(JSON.stringify(initialHumanReadableTextRef.value.lineObj))[lineIndex]);
            }  
            })  
          // }        
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
      <section class="modal-textAnalysis">
        <slot name="titleDiv">
            <span class="text-row">
              Title: {{props.selectedTitle}}
            </span>
            <span class="text-row">
              Author: {{props.selectedAuthor}}
            </span>
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
          <div id="singleTextAnalysisRow">
          Lorem Ipsum Lorem Ipsum Lorem Ipsum
          </div>
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
    padding: 16% 1%;
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
  }
  .self-building-square-spinner {
  
    top: 128px !important;
    position: absolute;
  }
  .text-row {
    width: 100%;
  }

  .modal-textAnalysis {
    /* this is the overarching modal */
    top: 72px;
    padding-left: 4%;
    padding-right: 4%;
    position: absolute;
    background: var(--color-background);;
    height: calc(100% - 164px);
  }
</style>