<script>

import * as d3 from 'd3';

export default {
  name: "GraphModal",
  components: {
    AreaChart,
    TestChart
  },
  data() {
    return {
      data:[7,1,1,7],
      mode:[1],
      // show: false,
      // clientX: 0,
      // clientY: 0,
      lastHoverPoint: {},
      points: [],
      scaled: {
        x: null,
        y: null,
      },
      paths: {
        area: '',
        line: '',
        selector: '',
      },
      width:null,
      height:null,
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
    setup(props){
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

    // mouseMove(event) {
    //   const { clientX, clientY } = event;
    //   this.show = true;
    //   this.clientX = event.clientX;
    //   this.clientY = event.clientY;
    // },
    
    createArea: d3.area().x(d => d.x).y0(d => d.max).y1(d => d.y),
    createLine: d3.line().x(d => d.x).y(d => d.y),
    createValueSelector: d3.area().x(d => d.x).y0(d => d.max).y1(0),
    // update(){
    // //  this.scaled.x.domain(d3.extent(this.data, (d, i) => i));
    // //   this.scaled.y.domain([0, this.height]);
    //   for (const [i, d] of this.data.entries()) {
    //     console.log("THIS IS D: ", d);
  
    //       this.points.push({
    //           x: i,
    //           y: d,
    //           max: this.height,
    //       });
 
    //     console.log(">?>?>? ", this.createLine(this.points));
    //     // this.paths.area = this.createArea(this.points);
    //     // this.paths.line = this.createLine(this.points);
    //     // console.log("PATHS: ", this.paths);
    //   }
    // },

    getClosestPoint(x) {
      // console.log("what are point options?? ", this.points);
      return this.data
        .map((point, index) => ({ x:
          point.x,
          diff: Math.abs(point.x - x),
          index,
        }))
        .reduce((memo, val) => (memo.diff < val.diff ? memo : val));
    },
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
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[0])
      }
      if(negative){
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[1])
      }
      if(neutral){
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[2])
      }
      if(positive){
        tempData = sentenceVizSentimentPlaceholder2.map(i=>[i])
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
  graphstate: String
});

const tooltipMsg = ref();
tooltipMsg.value = ''

watch([props,props.dataObj, tooltipMsg], ([currentValueA,currentValueB,currentValueC], [oldValueA,oldValueB,oldValueC]) => {
  console.log("?????? ", props.graphstate);
  console.log(currentValueA);
  console.log(currentValueB);
  console.log(currentValueC);
  return;
});

function updateTooltip(selected) {
    let grammarArr = [];
    let entitiesArr = [];
    if(!JSON.parse(JSON.stringify(props.dataObj))){
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
      console.log("eerrr: ",e)
    }
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

</script>

<template >
  <div id="graphDiv">
    <h1 id="graphTitle">TODO: Add Graph Title Here</h1>

      <!-- AREA CHART WORKS! IT IS OUR MODEL!
      <AreaChart :data="data" :tooltipmsg="tooltipMsg" :mode="mode" @selected="updateTooltip"></AreaChart> -->
      <TestChart :data="data" :tooltipmsg="tooltipMsg" :mode="mode"  :graphstate="this.props.graphstate" @selected="updateTooltip"></TestChart>

    <div class="buttons" >
      <button class="green-btn" @click="addData">Add data</button>
      <button class="green-btn" @click="filterData">Filter data</button>
      <div>
        <button class="green-btn" @click="updateVizDataCommonWords">Common Words</button>
        <button class="green-btn" @click="updateVizDataSentiment(true,false,false,false)">Sentiment</button>
        <button class="green-btn" @click="updateVizDataSentiment(false,true,false,false)">Sentiment</button>
        <button class="green-btn" @click="updateVizDataSentiment(false,false,true,false)">Sentiment</button>
        <button class="green-btn" @click="updateVizDataSentiment(false,false,false,true)">Sentiment</button>
        <button class="green-btn" @click="updateVizDataLineObj()">Syllables per Line</button>
      </div>
    </div>
  </div>
</template>



<style>
#graphTitle {
  position:absolute;
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
    top: 92px;
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

</style>