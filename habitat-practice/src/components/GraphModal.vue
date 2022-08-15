<script>

import * as d3 from 'd3';

export default {
  name: "GraphModal",
  components: {
    AreaChart,
    TestChart
  },
  emits : ['dataname_y','dataname_x','dataCountX', 'dataCountY','closeUpdatePopup','numberXMax','numberXMin','numberYMax','numberYMin'],
  data() {
    return {
      data:[],
      currentXName: "X_",
      currentYName: "Y_",
      mode:[1],
      points: [],
      popupOpen: false,
      paths: {
        area: '',
        line: '',
        selector: '',
      },
      width:null,
      height:null,
      color:null,
      valueX: 'initX',
      valueY: 'initY',
    };
  },
  margin: {
    type: Object,
    default: () => ({
      left: 0,
      right: 0,
      top: 10,
      bottom: 10,
    }),
  },

  methods: {
    setup(props,{emit}){
      this.popupOpen = false;
    },
    setWidth(width){
      this.width = width;
      console.log("SET WIDTH TO ", this.width);
    },
    setHeight(height){
      this.height = height;
      console.log("SET HEIGHT TO ", this.height);
    },
    addData() {
      // add random value from 0 to 50 to array
      this.data = [...this.data, Math.round(Math.random() * 50)];
    },
    filterData() {
      this.data = this.data.filter((v) => v <= 35);
    },
    updateVizDataCommonWords(){
      this.data = JSON.parse(JSON.stringify(this.props.dataObj))['textObj']['mostCommonWords'].map(i=>i['occurances']);
        let tempData = this.data.map(i=>i)

        this.valueY = "Occurances";
        this.valueX = "Items";

        this.numberXMax[this.props.currentLinesCount] = tempData.length; 
        this.numberXMin[this.props.currentLinesCount] = 0;
        this.numberYMax[this.props.currentLinesCount] = Math.max(...tempData)

        this.numberYMin[this.props.currentLinesCount] = Math.min(...tempData);
        if(tempData.length > this.numberXMax[this.props.currentLinesCount]){
          this.numberXMax[this.props.currentLinesCount] = tempData.length; 
        }
        this.numberXMin[this.props.currentLinesCount] = 0;
        if(Math.max(...tempData) > this.numberYMax[this.props.currentLinesCount]){
          this.numberYMax[this.props.currentLinesCount] = Math.max(...tempData);
        }

        this.numberXMax[this.props.currentLinesCount] = tempData.length - 1; 
        this.numberYMin[this.props.currentLinesCount] = Math.min(...tempData);

        console.log("common words in GM: ", this.numberXMax[this.props.currentLinesCount - 1]);
    },
    updateVizDataLineObj(){
      Object.keys(JSON.parse(JSON.stringify(this.props.dataObj))['lineObj']).slice(-1)
      this.data = Object.values(JSON.parse(JSON.stringify(this.props.dataObj))['lineObj']).map(i=>i['syllablesInLine']);
        // this is only necessary if it is stopping point errors
        let tempData = this.data.map(i=>i)

        this.valueY = "Syllable Count";
        this.valueX = "Sentence Count";
        console.log("THIS CURR LINES COUNT: ", this.numberXMax[this.props.currentLinesCount]);
        console.log("TEMPDATA: ", tempData);
        this.numberXMax[this.props.currentLinesCount] = tempData.length; 
        this.numberXMin[this.props.currentLinesCount] = 0;
        this.numberYMax[this.props.currentLinesCount] = Math.max(...tempData)
        this.numberYMin[this.props.currentLinesCount] = Math.min(...tempData);
        if(tempData.length > this.numberXMax[this.props.currentLinesCount]){
          this.numberXMax[this.props.currentLinesCount] = tempData.length; 
        }
        
        this.numberXMin[this.props.currentLinesCount] = 0;

        if(Math.max(...tempData) > this.numberYMax[this.props.currentLinesCount]){
          this.numberYMax[this.props.currentLinesCount] = Math.max(...tempData) - 1;
        }
        this.numberYMin[this.props.currentLinesCount] = Math.min(...tempData);
      let lineObjVizPlaceholder1 = [];
      Object.values(JSON.parse(JSON.stringify(this.props.dataObj))['lineObj']).map(i=>lineObjVizPlaceholder1.push(i));
      console.log("LINE OBJECT !! ", lineObjVizPlaceholder1);
      let syllablesPerLinePlaceholder = [];
      Object.values(lineObjVizPlaceholder1).map(j=>{if(j['syllablesInLine']){syllablesPerLinePlaceholder.push(j['syllablesInLine'])}});
      this.data = syllablesPerLinePlaceholder;
    },

    updateVizDataSentiment(compound,negative,neutral,positive){
      let sentenceVizSentimentPlaceholder1 = [];
      Object.values(JSON.parse(JSON.stringify(this.props.dataObj))['sentenceObj']).map(i=>sentenceVizSentimentPlaceholder1.push(Object.values(i)));
      sentenceVizSentimentPlaceholder1.pop()
      console.log("SENTIMENT MATRIX: ", sentenceVizSentimentPlaceholder1);
      let sentenceVizSentimentPlaceholder2 = [];
      sentenceVizSentimentPlaceholder1.map(i=>sentenceVizSentimentPlaceholder2.push(i.map(j=>Object.values(j)[0])))
      console.log("NEW Matrix: ", sentenceVizSentimentPlaceholder2);
      let tempData = [];
      if(compound){
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[0])
        this.valueY = "Sentiment (Compound)";
        this.valueX = "Sentence Count";
        this.numberXMax[this.props.currentLinesCount] = tempData.length; 
        this.numberXMin[this.props.currentLinesCount] = 0;
        this.numberYMax[this.props.currentLinesCount] = Math.max(...tempData)
        this.numberYMin[this.props.currentLinesCount] = Math.min(...tempData);
        
      }
      if(negative){
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[1])
        this.valueY = "Sentiment (Negative)";
        this.valueX = "Sentence Count";
        this.numberXMax[this.props.currentLinesCount] = tempData.length;
        this.numberXMin[this.props.currentLinesCount] = 0;
        this.numberYMax[this.props.currentLinesCount] = Math.max(...tempData);
        this.numberYMin[this.props.currentLinesCount] = Math.min(...tempData); 
      }
      if(neutral){
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[2]);
        this.valueY = "Sentiment (Neutral)";
        this.valueX = "Sentence Count";
        this.numberXMax[this.props.currentLinesCount] = tempData.length;
        this.numberXMin[this.props.currentLinesCount] = 0;
        this.numberYMax[this.props.currentLinesCount] = Math.max(...tempData);
        this.numberYMin[this.props.currentLinesCount] = Math.min(...tempData); 
      }
      if(positive){
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[3])
        this.valueY = "Sentiment (Positive)";
        this.valueX = "Sentence Count";

        this.numberXMax[this.props.currentLinesCount] = tempData.length;
        this.numberXMin[this.props.currentLinesCount] = 0;
        this.numberYMax[this.props.currentLinesCount] = Math.max(...tempData);
        this.numberYMin[this.props.currentLinesCount] = Math.min(...tempData); 
        
        this.mode[0] = 1;
        this.mode = [4];
      }
      this.data = tempData;
    },
  },
};


</script>

<script setup>
import BarChart from './BarChart.vue';
import TestChart from './TestChart.vue';
import {watch, ref} from 'vue';
import AreaChart from './AreaChart.vue';
import LineChart from './LineChart.vue';
import StackedAreaChart from './StackedAreaChart.vue';

const props = defineProps({
  open: Boolean,
  dataObj: Object,
  graphstate: Number,
  color0: String,
  color1: String,
  color2: String,
  color3: String,
  colorX: String,
  colorY: String,
  secondTextRef: Boolean,
  currentLinesCount: Number,


  // numberX: Number,
  // numberY: Number,
  axisColorMatchBool: Boolean,
  selectedXAxisRef:{
    label:String,
    value:Array,
    isIndex:Boolean
  },
  selectedYAxisRef:{
    label:String,
    value:Array,
    isIndex:Boolean
  },
  selectedRow: Number
});

const emit = defineEmits(['numberXMin','numberXMax','numberYMin','numberYMax','dataname_y', 'dataname_x','closeUpdatePopup']); 

const valueX = ref('');
const valueY = ref('');
const numberXMax = ref([]);
const numberXMin = ref([]);
const numberYMax = ref([]);
const numberYMin = ref([]);
numberXMax.value = []; 
numberXMin.value = []; 
numberYMax.value = []; 
numberYMin.value = []; 
const tooltipMsg = ref();
tooltipMsg.value = ''
const resetXRef = ref(false);
const resetYRef = ref(false);

watch([props,props.dataObj, tooltipMsg, props.secondTextRef.value, valueX.value,valueY.value,props.currentLinesCount,props.colorX,props.axisColorMatchBool,numberXMax.value,numberXMin.value,numberYMax.value,numberYMin.value,props.selectedXAxisRef,props.selectedYAxisRef,props.selectedRow,resetXRef.value, resetYRef.value], ([currentValueA,currentData,currentTooltip,currentXLabel,currentYLabel,currentLineCount,currentColorX,currentMatchBool,currentXMax,currentXMin,currentYMax,currentYMin,currentXAxisData,currentYAxisData,currentSelectedRow,currentResetX,currentResetY], [oldValueA,oldData,oldTooltip,oldXLabel,oldYLabel,oldLineCount,oldColorX,oldMatchBool,oldXMax,oldXMin,oldYMax,oldYMin,oldXAxisData,oldYAxisData,oldSelectedRow,oldResetX,oldResetY]) => {

    if(resetXRef.value === true){
      let index = JSON.parse(JSON.stringify(numberXMax.value)).indexOf(Math.max(...JSON.parse(JSON.stringify(numberXMax.value))));
      JSON.parse(JSON.stringify(numberXMax.value)).slice(index);
      resetXRef.value = false;
      console.log("this should work for reset X");
    }
    if(resetYRef.value === true){
      let index = JSON.parse(JSON.stringify(numberYMax.value)).indexOf(Math.max(...JSON.parse(JSON.stringify(numberYMax.value))));
      JSON.parse(JSON.stringify(numberYMax.value)).slice(index);
      resetYRef.value = false;
      console.log("this should work for reset Y");
    }
    emit('numberXMax', JSON.parse(JSON.stringify(numberXMax.value)).filter(x=>typeof x === "number"));
    emit('numberXMin', JSON.parse(JSON.stringify(numberXMin.value)));
    emit('numberYMax', JSON.parse(JSON.stringify(numberYMax.value)).filter(z=>typeof z === "number"));
    emit('numberYMin', JSON.parse(JSON.stringify(numberYMin.value)).filter(a=>typeof a === "number"));

  if(currentXLabel !== oldXLabel){
    emit('dataname_x', this.valueX);
  }
  if(currentYLabel !== oldYLabel){
    emit('dataname_y',this.valueY);
  }

  let keyBuilder = document.getElementById("d3UpdateButtonsWrapper");
  console.log("here's keybuilder div");
  if(keyBuilder){
    keyBuilder.style.borderColor = props.colorX;
    }

  if(valueX.value){
    emit('dataname_x',valueX.value)
  } 
  if(valueY.value){
    emit('dataname_y',valueY.value)
  }

  return;
});

function resetX(){
  resetXRef.value = true;
}

function resetY(){
  resetYRef.value = true;
}

function updateTooltip(selected) {
    let grammarArr = [];
    let entitiesArr = [];
    if(!JSON.parse(JSON.stringify(props.dataObj))){
      console.log("no data obj")
      return;
    }
    try {
      JSON.parse(JSON.stringify(props.dataObj)).sentenceObj[selected]['sentenceGrammarArray'].forEach((g)=>{
        grammarArr.push([g.tokenTag,g.tokenPos,g.tokenText])
      });
      JSON.parse(JSON.stringify(props.dataObj)).sentenceObj[selected]['sentenceSpacyEntities'].forEach((h)=>{
        entitiesArr.push([h.text,h.type])
      })
      
      tooltipMsg.value = {
        grammarArrays : grammarArr,
        sentimentCompound : JSON.parse(JSON.stringify(props.dataObj)).sentenceObj[selected]['sentenceSentimentCompound']['compound'],
        sentimentNegative : JSON.parse(JSON.stringify(props.dataObj)).sentenceObj[selected]['sentenceSentimentNegative']['neg'],
        sentimentNeutral : JSON.parse(JSON.stringify(props.dataObj)).sentenceObj[selected]['sentenceSentimentNeutral']['neu'],
        sentimentPositive : JSON.parse(JSON.stringify(props.dataObj)).sentenceObj[selected]['sentenceSentimentPositive']['pos'],
        entityArrays : entitiesArr
      }
    } catch(e){
      console.log("err: ",e)
    }

  console.log("SOME READING MATERIAL: ", JSON.parse(JSON.stringify(props.dataObj)).sentenceObj[selected])

}
function tryToggleComparative(){
  props.graphstate = props.graphstate + 1;
}

function emitterClose(command){
  console.log("emitting");
  emit(command);
}
</script>

<template >
  <div id="graphDiv">
    <h1 id="graphTitle">TODO: Add Graph Title Here</h1>

      <!-- AREA CHART WORKS! IT IS OUR MODEL!
      <AreaChart :data="data" :tooltipmsg="tooltipMsg" :mode="mode" @selected="updateTooltip"></AreaChart> -->
      <TestChart 
        :data="data"
        :selectedXAxisRef="props.selectedXAxisRef"
        :selectedYAxisRef="props.selectedYAxisRef"
        :secondTextRef="props.secondTextRef" 
        :tooltipmsg="tooltipMsg" 
        :selectedRow="props.selectedRow"
        :mode="mode"
        @selected="updateTooltip"
        :currentLinesCount="props.currentLinesCount"
        :color0="props.color0"
        :color1="props.color1"
        :color2="props.color2"
        :color3="props.color3"  
        :colorX="props.colorX"
        :colorY="props.colorY"
        :valueX="valueX"
        :valueY="valueY"
        :numberXMax="this.numberXMax"
        :numberXMin="this.numberXMin"
        :numberYMax="this.numberYMax"
        :numberYMin="this.numberYMin"
        :axisColorMatchBool="axisColorMatchBool"
        :graphstate="props.graphstate" 
        @toggleComparative="tryToggleComparative" 
        @resetX="resetX"
        @resetY="resetY"
       >
      </TestChart>

    
      <div class="buttons" >
      <!-- BRING BACK SOON! -->
        <!-- <button class="green-btn bottom-btn" @click="addData">Add data</button>
        <button class="green-btn bottom-btn" @click="filterData">Filter data</button> -->
        <div id="d3UpdateButtonsWrapper">
          <h1 id="buttonsWrapperTitle">Let's Begin...</h1>
          <h3 id="buttonsWrapperSubtitle">
            Reopen this window any time you'd like to update the data displayed in the graph. Select a value to track with your first line.
          </h3>
          <div id="buttonsInnerWrapper">
            <span>Sentiment Scores</span>
            <br/>
            <button class="green-btn" @click="updateVizDataSentiment(false,false,false,true); emitterClose('closeUpdatePopup')">Pos</button>
            <button class="green-btn" @click="updateVizDataSentiment(true,false,false,false); emitterClose('closeUpdatePopup')">Comp</button>
            <button class="green-btn" @click="updateVizDataSentiment(false,true,false,false); emitterClose('closeUpdatePopup')">Neg</button>
            <button class="green-btn" @click="updateVizDataSentiment(false,false,true,false); emitterClose('closeUpdatePopup')">Neu</button>
            <br/>
            <span>Text-Level Statistics</span>
            <br/>
            <button class="green-btn" @click="updateVizDataCommonWords(); emitterClose('closeUpdatePopup')">Common Words</button>
            <br/>
            <span>Line-Level Analysis</span>
            <br/>
            <button class="green-btn" @click="updateVizDataLineObj(); emitterClose('closeUpdatePopup')">Syllables Per Line</button>
            <br/>
          </div>
        </div>
      </div>
  </div>
</template>



<style>
#graphTitle {
  position:absolute;
  position:relative;
  text-align:center;
  color:white;
  visibility:hidden;
}
.picker-popup > .slider:before {
  height:0px !important;
  width:0px !important;
}
#graphDiv {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    max-width: 100%;
    padding: 0 0px;
    width: 100%;
    position: fixed;
    z-index: 99;
    top: 80px;
    height: calc(72% - 52px);
    
}

svg {
  /* important for responsiveness */
  display: block;
  fill: none;
  stroke: none;
  width: 100%;
  height: 100%;
  overflow: visible;
  background: #eee;
}

.buttons {
  margin-top: 2rem;
}
</style>

<style>
#graphModal {
    width: 100%;
    height: auto;
    display: flex;
    text-align: center;
    top: 72px;
    bottom: 0px;
    left: 0px;
    right:0px;
    position: absolute;
}
#button {
  background-color: green;
}


.color-input .picker-popup {
  background-color:var(--color-background) !important;
  color:#ffffff;
  background:var(--color-background) !important;
}

.color-input .text-inputs-wrapper .text-input  {
  color: #000000;
} 

.text-format-arrows {
  --arrow-color: #000000;
}

#newTextPopup {
    display: none;
width: calc(100%);
    display: none;
    flex-direction: row;
    position: fixed;
    background: var(--color-background);
    background-color: var(--color-background);
    border-radius: 8px;
    display: flex;
    z-index: 99;
    /* margin-left: -96px; */
    text-align: center;
    /* justify-content: right; */
    /* left: 33%; */
    padding: 8%;
    top: -12%;
}

#d3UpdateButtonsWrapper {
    position: fixed;
    justify-content: center;
    width: 100%;
    top: 0%;
    z-index: 100;
    background-color: rgba(0, 0, 0, 0.88);
    left: 0%;
    padding-top: 20px;
    color: white;
    padding: 12%;
    /* border: 1px solid white; */
    border-radius: 8px;
    bottom: 0%;
    pointer-events:none;
}
#buttonsInnerWrapper {
  padding-top: 24px;
  padding-bottom: 24px;
  width: 100%;
  padding-right: 24px;
  padding-left: 24px;
  border-radius: 0px 0px 8px 8px;
  pointer-events:all;
}
#buttonsWrapperTitle,#buttonsWrapperSubtitle,#buttonsInnerWrapper {
  background-color:var(--color-background);
}
#buttonsWrapperTitle {
  border-radius: 8px 8px 0px 0px;
  padding: 12px;
}
#buttonsWrapperSubtitle {
  padding-right:24px;
  padding-left:24px;
}
button.green-btn {
  width:25%;
  font-size:14px
}
button.green-btn.bottom-btn {
   width: 25%;
  max-height: 40px;
  top: 16px;
}
.animate-close {
  opacity: 0;
  transition: opacity 2s;
}
</style>