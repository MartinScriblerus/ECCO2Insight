<script>

import * as d3 from 'd3';

export default {
  name: "GraphModal",
  components: {
    AreaChart,
    TestChart
  },
  emits : ['dataname_y','dataname_x','dataCountX', 'dataCountY','closeUpdatePopup'],
  data() {
    return {
      data:[7,1,1,7],
      currentXName: "X_",
      currentYName: "Y_",
      mode:[1],
      points: [],
      // scaled: {
      //   x: null,
      //   y: null,
      // },
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
      numberX: 0,
      numberY: 0
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
      console.log("WHAT ARE PROPS: ", props);
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

    //////////////////////////////////////////////

    /////////////////////////////////////////////
    addData() {
      // add random value from 0 to 50 to array
      this.data = [...this.data, Math.round(Math.random() * 50)];
    },
    filterData() {
      this.data = this.data.filter((v) => v <= 35);
    },
    updateVizDataCommonWords(){
      this.data = JSON.parse(JSON.stringify(this.props.dataObj))['textObj']['mostCommonWords'].map(i=>i['occurances']);
    },
    updateVizDataLineObj(){
      let lineObjVizPlaceholder1 = [];
      Object.values(JSON.parse(JSON.stringify(this.props.dataObj))['lineObj']).map(i=>lineObjVizPlaceholder1.push(i));
      console.log("LINE OBJECT !! ", lineObjVizPlaceholder1);
      let syllablesPerLinePlaceholder = [];
      Object.values(lineObjVizPlaceholder1).map(j=>syllablesPerLinePlaceholder.push(j['syllablesInLine']));
      this.data = syllablesPerLinePlaceholder;
    },
    // closeUpdatePopup(){

    //   let updateDataBtn = document.getElementById("updateeDataBtn");
    //   if(updateDataBtn){
    //     updatePopup.classList.remove("animateClose");
    //   }
    //   setTimeout(()=>{
        
    //   },2000);
    //   clearTimeout();
    // },
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
        this.valueY = "Sentiment (Compound)";
        this.valueX = "Sentence Count";
        this.numberX = tempData.length; 
        console.log("are we getting this? ", this.numberX);
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[0])
      }
      if(negative){
        this.valueY = "Sentiment (Negative)";
        this.valueX = "Sentence Count";
        this.numberX = tempData.length; 
        //emit('dataname_y', 'sentiment (negative)')
        console.log("are we getting this? ", this.numberX);
      
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[1])
      }
      if(neutral){
        //emit('dataname_y', 'sentiment (neutral)')
        this.valueY = "Sentiment (Neutral)";
        this.valueX = "Sentence Count";
        this.numberX = tempData.length; 
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[2])
      }
      if(positive){
        this.valueY = "Sentiment (Positiive)";
        this.valueX = "Sentence Count";
        this.numberX = tempData.length; 
        //emit('dataname_y', 'sentiment (positive)')
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[3])
        this.mode[0] = 1;
        this.mode = [4];
      }
     // emit('dataCountXLength', tempData.length)
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
  graphstate: String,
  color0: String,
  color1: String,
  color2: String,
  color3: String,
  colorX: String,
  colorY: String,
  secondTextRef: Boolean,
  currentLinesCount: Number,
  numberX: Number,
  numberY: Number
});

const emit = defineEmits(['number_x','number_y','dataname_y', 'dataname_x','dataCountX','closeUpdatePopup']); 

const valueX = ref('');
valueX.value = "count";

const valueY = ref('');
valueY.value = "count";

const tooltipMsg = ref();
tooltipMsg.value = ''

// DO WE WANT TO USE DATA VARIABLE OR REF HERE>>>>?
const numberX = ref(null);
const numberY = ref(null);
numberX.value = 0;
numberY.value = 0;

watch([props,props.dataObj, tooltipMsg, props.secondTextRef.value, valueX.value,valueY.value,numberX.value,numberY.value,props.currentLinesCount,props.colorX], ([currentValueA,currentData,currentTooltip,currentXLabel,currentYLabel,currentXMax,currentYMax,currentLineCount,currentColorX], [oldValueA,oldData,oldTooltip,oldXLabel,oldYLabel,oldXMax,oldYMax,oldLineCount,oldColorX]) => {
  if(currentXLabel !== oldXLabel){
    emit('dataname_x', currentXLabel);
  }
  if(currentYLabel !== oldYLabel){
    emit('dataname_y', currentYLabel);
  }
  if(currentData !== oldData){
    console.log("HEY CHECK OUT CURRENT DATA: ", currentData);
  }
  // if(currentColorX !== oldColorX){
    let keyBuilder = document.getElementById("d3UpdateButtonsWrapper");
    console.log("here's keybuilder div");
    if(keyBuilder){
      keyBuilder.style.borderColor = props.colorX;
    }
  // }
  console.log("props ", props.graphstate);
  console.log(`PROPS COLORS -> ${props.color0} ${props.color1} ${props.color2} ${props.color3}`);
  console.log("!!!!! ", props.currentLinesCount);
  console.log("FUUUUUUUUUUUUUUUCK: ", props.dataObj)
  emit('dataname_y','NAME_HERE')
  emit('dataCountX',props.dataObj.length)

  return;
});

function updateTooltip(selected) {
  console.log("in update tooltip ", selected);
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
      console.log("wat the fuq eerrr: ",e)
    }
    console.log("WHERE IS TOOLTIP MSG>> ", tooltipMsg.value)
  console.log("SOME READING MATERIAL: ", JSON.parse(JSON.stringify(props.dataObj)).sentenceObj[selected])
    // tooltipMsg.value = {
    //   grammarArrays : grammarArr,
    //   sentimentCompound : JSON.parse(JSON.stringify(props.dataObj)).sentenceObj[selected]['sentenceSentimentCompound']['compound'],
    //   sentimentNegative : JSON.parse(JSON.stringify(props.dataObj)).sentenceObj[selected]['sentenceSentimentNegative']['neg'],
    //   sentimentNeutral : JSON.parse(JSON.stringify(props.dataObj)).sentenceObj[selected]['sentenceSentimentNeutral']['neu'],
    //   sentimentPositive : JSON.parse(JSON.stringify(props.dataObj)).sentenceObj[selected]['sentenceSentimentPositive']['pos'],
    //   entityArrays : entitiesArr
    // }


}
function tryToggleComparative(){
  props.graphstate = "singleText";
}


// console.log("SET UP COLOR... HERE IS THIS: ", props.color0);
// const colorInput = this.refs.colorInput // root instance
// const picker = colorInput.refs.picker // popup color picker instance
// console.log("COLORPICKER: ", colorInput.color) // tinycolor instance);

// function colorInputMountedHandler(){
//   console.log("input mounted: ");
//     console.log("LOOK: ", document.getElementById("text-input-hex"));
// } 

// function colorPickerShowHandler(){
//   console.log("showpicker mounted: ", );
//   console.log("LOOK 2: ", document.getElementById("text-input-hex"));
  
// }
function emitterClose(command){
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
        :secondTextRef="props.secondTextRef" 
        :tooltipmsg="tooltipMsg" 
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
        :numberX="numberX"
        :numberY="numberY"
        :graphstate="props.graphstate" 
        @toggleComparative="tryToggleComparative" 
       >
      </TestChart>
<!--     
    <div id="newTextPopup">
    TEST TEST TEST
      <color-input v-model="color" position="right top" ref="colorInput" @mounted="colorInputMountedHandler" @pickStart="colorPickerShowHandler"/>
    </div> -->
    
    <div class="buttons" >
      <button class="green-btn" @click="addData">Add data</button>
      <button class="green-btn" @click="filterData">Filter data</button>
      <div id="d3UpdateButtonsWrapper">
        <h1>Let's Begin...</h1>
        <h3>
          Reopen this window any time you'd like to update the data displayed in the graph. Select a value to track with your first line.
        </h3>
        <div id="buttonsInnerWrapper">
          <span>Sentiment Scores</span>
          <br/>
          <button class="green-btn" @click="updateVizDataSentiment(false,false,false,true); emitterClose('closeUpdatePopup')">Positive</button>
          <button class="green-btn" @click="updateVizDataSentiment(true,false,false,false); emitterClose('closeUpdatePopup')">Compound</button>
          <button class="green-btn" @click="updateVizDataSentiment(false,true,false,false); emitterClose('closeUpdatePopup')">Negative</button>
          <button class="green-btn" @click="updateVizDataSentiment(false,false,true,false); emitterClose('closeUpdatePopup')">Neutral</button>
          <br/>
          <span>Text-Level Statistics</span>
          <br/>
          <button class="green-btn" @click="updateVizDataCommonWords">Common Words</button>
          <br/>
          <span>Line-Level Analysis</span>
          <br/>
          <button class="green-btn" @click="updateVizDataLineObj()">Syllables Per Line</button>
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
  color:pink;
  background:var(--color-background) !important;
}

.color-input .text-inputs-wrapper .text-input  {
  color: #000000;
} 

.text-format-arrows {
  --arrow-color: pink;
}

#newTextPopup {
    width: 60%;

    display: none;
    flex-direction: row;
    position: fixed;
    background: var(--color-background);
    background-color: var(--color-background);
    border: solid 1px #eee;
    border-radius: 8px; 
    display: flex;
    z-index: 9999;
    left: 0px;
    text-align: center;
    justify-content: right;
    left: 5%;
    right: 5%;
    top: 24%;
}

#d3UpdateButtonsWrapper {
    position: fixed;
    justify-content: center;
    width: 50%;
    top: 16%;
    z-index: 9999;
    background: rgba(255, 255, 255, 0.078);
    background-color: rgba(0, 0, 0, 0.88);
    left: 25%;
    padding-top: 20px;
    color: white;
    padding: 20px;
    border: 1px solid white;
    border-radius: 8px;
}
#buttonsInnerWrapper {
  padding-top: 20px;
  padding-bottom: 20px;
  width: 100%;

}
button.green-btn {
  width:25%;
}
.animate-close {
  opacity: 0;
  transition: opacity 2s;
}
</style>