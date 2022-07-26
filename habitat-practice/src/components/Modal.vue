<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  open: Boolean,
  openFull: Boolean,
  tocdata: Object,
  rawtextdata: String,
  selectedTitle: String,
  selectedAuthor: String,
});

const temp = ref({})

// let sentenceGrammarObj =
//   index: {
//     tokenPos:String,
//     tokenTag:String,
//     tokenText:String,
// }

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
    // placesEntitiesArray: Array,
    mostCommonWords: Array,

  },

  lineObj: {
    lineId: Number,
    poeticForm: String,
    thisRhyme: String,
    lastRhyme: String,
    internalRhymes: Array,
    syllablesPerLine: Number
  },

  sentenceIndex: Number,
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
  sentencesArray: Array,
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
      console.log("HERE IS THE MODAL TO UPDATE", fullModal);
      emit('closedmodal')
      fullModal.classList.add("awaiting");

      console.log("HERE IS PROPS TITLE: ", props.selectedTitle);
      console.log("HERE IS PROPS SELECTED AUTHOR: ", props.selectedAuthor);
    },10)
    clearTimeout();
  };

function doCloseFullModalChild(){
  emit('closedfull')
  // modalFull.value.classList.add("hideFullModal")
  console.log("HIT THIS!!!!")
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

          const tempGramArr = ref([])
          
          // temp.value.spacy_entities.forEach(seObj => {
          //   console.log("AHHHH ", seObj);
          //   console.log("KEYS-> ", Object.keys(seObj));
          //   console.log("VAL KEY => ", Object.keys(JSON.parse(JSON.stringify(Object.values(Object.values(seObj))))[0])[0])
          //   console.log("VAL VAL => ", Object.values(JSON.parse(JSON.stringify(Object.values(Object.values(seObj))))[0])[0])
          //   // initialHumanReadableTextRef.value.spacyEntityObj.spacyEntityIndex = Object.keys(seObj)[0];
          //   // initialHumanReadableTextRef.value.spacyEntityObj.text = Object.keys(JSON.parse(JSON.stringify(Object.values(Object.values(seObj))))[0])[0];
          //   // initialHumanReadableTextRef.value.spacyEntityObj.type = Object.values(JSON.parse(JSON.stringify(Object.values(Object.values(seObj))))[0])[0];
          //   //console.log(`WHAT THE FUCK IS ${initialHumanReadableTextRef.value.textObj.spacyEntitiesArray} OR ${initialHumanReadableTextRef.value.spacyEntityObj}`)
          //   // console.log("ABOUT TO PUSH: ", initialHumanReadableTextRef.value.spacyEntityObj[Object.keys(seObj)]);
          //   // console.log("ABOUT TO PUSH: ", JSON.parse(JSON.stringify(initialHumanReadableTextRef.value.spacyEntityObj)));
          //   // // console.log("PUSHING INTO: ", JSON.parse(JSON.stringify(initialHumanReadableTextRef.value.textObj.spacyEntitiesArray)));
          //   JSON.parse(JSON.stringify(initialHumanReadableTextRef.value.textObj.spacyEntitiesObj))[Object.keys(seObj)[0]] = 
          //     // JSON.parse(JSON.stringify(initialHumanReadableTextRef.value.spacyEntityObj))
          //     {
          //       "text": Object.keys(JSON.parse(JSON.stringify(Object.values(Object.values(seObj))))[0])[0],
          //       "type": Object.values(JSON.parse(JSON.stringify(Object.values(Object.values(seObj))))[0])[0],
          //     };
              
            
          // });
          temp.value.most_common_words.forEach((word, rank) => {
            console.log("WTF IS WORD??? ", word);
           // console.log("AND WTF IS THIS??? ", JSON.parse(JSON.stringify(initialHumanReadableTextRef.value.mostCommonWords)));
           
           console.log("what is word??? ", word[0]);
            initialHumanReadableTextRef.value.textObj.mostCommonWords[rank]={"word":JSON.parse(JSON.stringify(word[0])),"occurances":JSON.parse(JSON.stringify(word[1]))};
            // initialHumanReadableTextRef.value.mostCommonWordsObj[i].occurances = word[1]
          });
         
          temp.value.sentence_id.forEach(sentence => {
            //initialHumanReadableTextRef.value.sentenceObj[sentence].sentenceGrammarArray = [];
            console.log("so, what is sentence? ", sentence);
            
            // if(sentence.sentence_index)
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
            console.log("what is this spacy entity? ", initialHumanReadableTextRef.value.sentenceObj[JSON.parse(JSON.stringify(Object.keys(entity)))].sentenceSpacyEntities);
            initialHumanReadableTextRef.value.sentenceObj[JSON.parse(JSON.stringify(Object.keys(entity)))].sentenceSpacyEntities.push(
              {
                "text": Object.keys(JSON.parse(JSON.stringify(Object.values(Object.values(entity))))[0])[0],
                "type": Object.values(JSON.parse(JSON.stringify(Object.values(Object.values(entity))))[0])[0],
              }
            )
          })
           // initialHumanReadableTextRef.value.sentenceObj[tempGramArr.value.sentence_index].sentenceGrammarArray = tempGramArr.value;
//           temp.value.sentence_grammar.word_level_grammar_result.forEach((wordGram,index) => {
//             console.log("what is thisssss: ", initialHumanReadableTextRef.value.sentenceObj[JSON.parse(JSON.stringify(wordGram['sentence_index']))]);


// console.log("wtf is thisssss: ", {"tokenPos": JSON.parse(JSON.stringify(wordGram['token_pos'])), "tokenTag":JSON.parse(JSON.stringify(wordGram['token_tag'])),"tokenText":JSON.parse(JSON.stringify(wordGram['token_text']))});

// //console.log("check object...... ", JSON.parse(JSON.stringify(initialHumanReadableTextRef.value.sentenceObj[JSON.parse(JSON.stringify(wordGram['sentence_index']))].sentenceGrammarArray)))
//             // console.log("chripes: ", JSON.parse(JSON.stringify(initialHumanReadableTextRef.value.sentenceObj))[parseInt(JSON.parse(JSON.stringify(wordGram))[JSON.parse(JSON.stringify(wordGramsentence_index))])]);

//             // console.log("god dammit: ", JSON.parse(JSON.stringify(initialHumanReadableTextRef.value.sentenceObj))[JSON.parse(JSON.stringify(wordGram['sentence_index']))]);
//             JSON.parse(JSON.stringify(initialHumanReadableTextRef.value.sentenceObj[JSON.parse(JSON.stringify(wordGram['sentence_index']))])).push({"tokenPos": JSON.parse(JSON.stringify(wordGram['token_pos'])), "tokenTag":JSON.parse(JSON.stringify(wordGram['token_tag'])),"tokenText":JSON.parse(JSON.stringify(wordGram['token_text']))})
          // });
          // NEED TO ADD LINES HERE... this will prob break a few 
          // times before it works...
          


          // })
          // tempRef.value.entities.forEach(euObj => {
          //   initialHumanReadableTextRef.value.europeanaEntityObj.europeanaEntityId = euObj.id;
          //   initialHumanReadableTextRef.value.europeanaEntityObj.prefLabel = euObj.prefLabel;
          //   initialHumanReadableTextRef.value.europeanaEntityObj.dateOfBirth = euObj.dateOfBirth;
          //   initialHumanReadableTextRef.value.europeanaEntityObj.dateOfDeath = euObj.dateOfDeath;
          //   initialHumanReadableTextRef.value.europeanaEntityObj.isShownBy.id = 
          // })

             

          console.log("tEEEEEDST: ", initialHumanReadableTextRef.value)
          
// const initialHumanReadableTextRef = ref({
  // sentenceObj: {
  //   sentenceId: String,
  //   sentimentCompound: Number,
  //   sentimentNegative: Number,
  //   sentimentNeutral: Number,
  //   sentimentPositive: Number,
  //   entitiesInSentence: Array,
  //   sentenceGrammar: {
  //     sentenceLevel: String,
  //     wordLevel: A
  //     
  //       tokenPos: String,
  //       tokenTag: String,
  //       tokenText: String
  //     }
  //   }
  // },
//   textObj: {
//     titleUrl: String,
//     avgLinesPerSentence: Number,
//     percPoetrySyllables: Number,
//     percPoetryRhymes: Number,
//     spacyEntitiesArray: Array,
//     europeanaEntitiesArray: Array,
//     placesEntitiesArray: Array,
//     mostCommonWords: Array
//   },
//   lineObj: {
//     lineId: Number,
//     poeticForm: String,
//     thisRhyme: String,
//     lastRhyme: String,
//     internalRhymes: Array,
//     syllablesPerLine: Number
//   },
//   linesArray: Array,
//   sentencesArray: Array,
//   europeanaEntityObj: {
//     prefLabel: String,
//     altLabels: Array,
//     dateOfBirth: Date,
//     dateOfDeath: Date,
//     isShownBy: {
//       id: String,
//       source: String
//     }
//   },
// })

          ///////////////////////////////////////////////////////////////////////////////
          ///////////////////////////////////////////////////////////////////////////////
          ///////////////////////////////////////////////////////////////////////////////
          
          let fullModal = modalFull.value;
          fullModal.classList.remove("awaiting");
          fullModal.classList.add("receivedSingleTextData");

          // document.getElementById("main").style.overflowY = "hidden";
          // let mds = document.getElementsByClassName("modal")
          // mds.forEach(m=>{
          //   m.style.overflowY = "hidden";
          // })


          console.log("DID THIS FUCKER UPDATE>>>>>????  ", fullModal);
          //emit("openedfull")
          // not necessary -> raw text from toc is initial text daata (we'll just need to use parse / stringify pattern)
          // initial_text_data.value = JSON.parse(JSON.stringify(rawtextfromtoc.value))
          // console.log("HEY GOT THIS TO LOG FROM INITIAL TEXT DATA: ", initial_text_data.value);
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
          {{props.selectedTitle.split(/[\:.]+/)[0] 
          ? 
            props.selectedTitle.split(/[\:.]+/)[0] 
          : 
            props.selectedTitle}}
          / {{props.selectedAuthor.replace('.', '')}}
        </slot>

        <button
          type="button"
          class="btn-close"
          @click="doCloseFullModalChild"
        >
          x
        </button>
      </header>

      <section class="modal-body">
        <slot name="body">
          <span>
            Title: {{props.selectedTitle}}
            Author: {{props.selectedAuthor}}
            </span>
          <div id="singleTextAnalysisRow">
            <slot name="words">
              words
            </slot>
            <slot name="lines">
              lines
            </slot>
            <slot name="sentences">
              sentences
            </slot>
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
  overflow: hidden;
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
}

#modalFull.awaiting {
    background:grey;
    pointer-events:all;
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
    padding: 15px;
    display: flex;
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
    background: rgba(0, 0, 0, 1);
    transition: height 1s ease-in;
  
  }

  .modal-footer {
    border-top: 1px solid #eeeeee;
    flex-direction: row;
    justify-content: flex-end;
    background: blue;
    bottom:0px;
    left:0px;
    right:0px;
    position:absolute;
  }

  .modal-body {
    position: relative;
    padding: 20% 10%;

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
    color: #4AAE9B;
    background: purple;
  }

  .btn-green {
    color: white;
    background: #4AAE9B;
    border: 1px solid #4AAE9B;
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
  }
</style>