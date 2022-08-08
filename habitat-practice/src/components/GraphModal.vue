<script>

import * as d3 from 'd3';

export default {
  name: "GraphModal",
  components: {
    AreaChart,
    TestChart
  },
  emits : ['dataname_y','dataname_x','dataCountX', 'dataCountY'],
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
    // Can these be removed/updated?
    //createArea: d3.area().x(d => d.x).y0(d => d.max).y1(d => d.y),
    //createLine: d3.line().x(d => d.x).y(d => d.y),
    //createValueSelector: d3.area().x(d => d.x).y0(d => d.max).y1(0),


    // getClosestPoint(x) {
    //   console.log("what are point options?? ", this.points);
    //   return this.data
    //     .map((point, index) => ({ x:
    //       point.x,
    //       diff: Math.abs(point.x - x),
    //       index,
    //     }))
    //     .reduce((memo, val) => (memo.diff < val.diff ? memo : val));
    // },

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

  currentLinesCount: Number,
  numberX: Number,
  numberY: Number
});

const emit = defineEmits(['number_x','number_y','dataname_y', 'dataname_x','dataCountX']); 

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

watch([props,props.dataObj, tooltipMsg, valueX.value,valueY.value,numberX.value,numberY.value,props.currentLinesCount], ([currentValueA,currentValueB,currentValueC,currXLabel,currYLabel], [oldValueA,oldValueB,oldValueC,oldXLabel,oldYLabel]) => {
  if(currXLabel !== oldXLabel){
    emit('dataname_x', currXLabel);
  }
  if(currYLabel !== oldYLabel){
    emit('dataname_y', currYLabel);
  }
  console.log("props ", props.graphstate);
  console.log(`PROPS COLORS -> ${props.color0} ${props.color1} ${props.color2} ${props.color3}`)
  console.log(currentValueA);
  console.log(currentValueB);
  console.log(currentValueC);
  console.log("!!!!! ", props.currentLinesCount);
 
  emit('dataname_y','NAME_HERE')
  emit('dataCountX',props.dataObj.length)
  emit('number_x',props.dataObj.length)
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

</script>

<template >
  <div id="graphDiv">
    <h1 id="graphTitle">TODO: Add Graph Title Here</h1>

      <!-- AREA CHART WORKS! IT IS OUR MODEL!
      <AreaChart :data="data" :tooltipmsg="tooltipMsg" :mode="mode" @selected="updateTooltip"></AreaChart> -->
      <TestChart 
        :data="data" 
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
        :graphstate="this.props.graphstate" 
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
      <div>
        <button class="green-btn" @click="updateVizDataCommonWords">Common</button>
        <button class="green-btn" @click="updateVizDataSentiment(true,false,false,false)">Comp</button>
        <button class="green-btn" @click="updateVizDataSentiment(false,true,false,false)">Neg</button>
        <button class="green-btn" @click="updateVizDataSentiment(false,false,true,false)">Neu</button>
        <button class="green-btn" @click="updateVizDataSentiment(false,false,false,true)">Pos</button>
        <button class="green-btn" @click="updateVizDataLineObj()">Syll/Line</button>
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
    height: calc(64% - 52px);
    
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
    top: 10%;
}



</style>