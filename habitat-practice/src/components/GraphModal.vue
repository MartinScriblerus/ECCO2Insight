<script>

export default {
  name: "GraphModal",
  components: {
    AreaChart,
  },
  data() {
    return {
      data:[7,1,1,7],
    };
  },
  methods: {
    setup(props){
      console.log("WHAT ARE PROPS: ", props);
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
      console.log("SENTIMENT MATRIX: ", sentenceVizSentimentPlaceholder1);
      let sentenceVizSentimentPlaceholder2 = [];
      sentenceVizSentimentPlaceholder1.map(i=>sentenceVizSentimentPlaceholder2.push(i.map(j=>Object.values(j)[0])))
      console.log("NEW Matrix: ", sentenceVizSentimentPlaceholder2);
      if(compound){
        this.data = sentenceVizSentimentPlaceholder2.map(i=>i[0])
      }
      if(negative){
        this.data = sentenceVizSentimentPlaceholder2.map(i=>i[1])
      }
      if(neutral){
        this.data = sentenceVizSentimentPlaceholder2.map(i=>i[2])
      }
      if(positive){
        this.data = sentenceVizSentimentPlaceholder2.map(i=>i[3])
      }

    },

  },
};


</script>

<script setup>
import BarChart from './BarChart.vue';
import {watch} from 'vue';
import AreaChart from './AreaChart.vue';
import LineChart from './LineChart.vue';
import StackedAreaChart from './StackedAreaChart.vue';

const props = defineProps({
  open: Boolean,
  dataObj: Object
});

watch(props.dataObj, (currentValue, oldValue) => {
  console.log(currentValue);
  console.log(oldValue);
  return;
});

</script>

<template>
  <div id="graphDiv">
    <h1>TODO: Add Graph Title Here</h1>
  
      <!-- <StackedAreaChart></StackedAreaChart> -->
      <AreaChart :data="data"></AreaChart>
        <!-- <BarChart :data="data" ></BarChart> -->

    <div class="buttons">
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
#graphDiv {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    max-width: 100%;
    padding: 0 20px;
    width: 100%;
    position: fixed;
    z-index: 99;
    top: 0px;
    height: 64%;
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