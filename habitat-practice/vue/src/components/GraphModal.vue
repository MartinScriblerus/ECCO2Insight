<script setup>
  import BarChart from './BarChart.vue';
  import TestChart from './TestChart.vue';
  import {watch, ref} from 'vue';
  // import AreaChart from './AreaChart.vue';
  // import LineChart from './LineChart.vue';
  // import StackedAreaChart from './StackedAreaChart.vue';

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
    yAxisFramingLast: Boolean,
  
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
  
  // const valueX = ref('');
  // const valueY = ref('');
  const numberXMax = ref([]);
  const numberXMin = ref([]);
  const numberYMax = ref([]);
  const numberYMin = ref([]);
  const popupOpen = ref(false)
  numberXMax.value = []; 
  numberXMin.value = []; 
  numberYMax.value = []; 
  numberYMin.value = []; 
  const tooltipMsg = ref();
  tooltipMsg.value = ''
  const resetXRef = ref(false);
  const resetYRef = ref(false);
  const mode = ref([1]);
  const data = ref([]);
  const valueX = ref('init_X');
  const valueY = ref('init_Y');
  function hideUpdateButtons(){
    console.log("fuck shit graph 1");
    let wrapperTitle = document.getElementById("buttonsWrapperTitle");
    let wrapperSubtitle = document.getElementById("buttonsWrapperSubtitle");
    let wrapperBtns = document.getElementById("buttonsInnerWrapper");
    if(wrapperTitle){
      wrapperTitle.style.display = "none";
    } 
    if(wrapperSubtitle){
      wrapperSubtitle.style.display = "none";
    } 
    if(wrapperBtns){
      wrapperBtns.style.display = "none";
    } 
  }
  popupOpen.value = false;
  console.log("fuck shit graph 2");
    function setWidth(width){
      // this.width = width;
      console.log("SET WIDTH TO ", width);
    }
    function setHeight(height){
      // this.height = height;
      console.log("SET HEIGHT TO ", height);
    }
    function addData() {
      // add random value from 0 to 50 to array
      data.value = [...data.value, Math.round(Math.random() * 50)];
    }
    function filterData() {
      data.value = data.value.filter((v) => v <= 35);
    }
    function updateVizDataCommonWords(){
      console.log("fuck shit graph 3");
      hideUpdateButtons();
      console.log("fuck shit graph 4");
      data.value = JSON.parse(JSON.stringify(props)).dataObj.textObj.mostCommonWords.map(i=>i['occurances']);
        let tempData = data.value.map(i=>i)
        console.log("fuck shit graph 5");
        valueY.value = "Occurances";
        valueX.value = "Items";
        console.log("is thissss the problem? check temp data", tempData)
        
        numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length; 
        numberXMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = 0;
        
        if(numberYMax.value && numberYMax.value < Math.max(...tempData)){
          numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max(...tempData) || 0;
        }
        if(numberYMin.value && numberYMin.value > Math.min(...tempData)){
          numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min(...tempData) || 0;
        }

        numberXMax.value = numberXMax.value.filter(m=>typeof m === "number");
        numberXMin.value = numberXMin.value.filter(n=>typeof n === "number");
        numberYMax.value = numberYMax.value.filter(o=>typeof o === "number");
        numberYMin.value = numberYMin.value.filter(p=>typeof p === "number");
        
        if(tempData.length > numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount]){
          numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length; 
        }
        numberXMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = 0;
        if(Math.max(...tempData) > numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount]){
          numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max.apply(Math,tempData);
        }
        numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length - 1; 
        numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min.apply(Math,tempData);
        console.log("common words in GM: ", numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount - 1]);
        console.log("fuck shit graph 6");
        //console.log("common words in GM: ", this.numberXMax[this.props.currentLinesCount - 1]);
    }
    function updateVizDataLineObj(){
      console.log("fuck shit graph 7");
      hideUpdateButtons();
      console.log("fuck shit graph 8");
      Object.keys(JSON.parse(JSON.stringify(props.dataObj))['lineObj']).slice(-1)
      data = Object.values(JSON.parse(JSON.stringify(props.dataObj))['lineObj']).map(i=>i['syllablesInLine']);
    
      // this is only necessary if it is stopping point errors
      let tempData = data.map(i=>i)
      console.log("fuck shit graph 9");
      valueY.value = "Syllable Count";
      valueX.value = "Sentence Count";
      //console.log("THIS CURR LINES COUNT: ", this.numberXMax[this.props.currentLinesCount]);
      console.log("TEMPDATA: ", tempData);
      numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length; 
      numberXMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = 0;
      if( Math.max(...tempData) > Math.max(numberYMax.value)){
        numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max(...tempData)
      }
      if( Math.min(...tempData) > Math.min(numberYMin.value)){
        numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min(...tempData);
      }
      numberXMax.value = numberXMax.value.filter(q=>typeof q === "number");
      numberXMin.value = numberXMin.value.filter(r=>typeof r === "number");
      numberYMax.value = numberYMax.value.filter(s=>typeof s === "number");
      numberYMin.value = numberYMin.value.filter(t=>typeof t === "number");

      if(tempData.length > numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount]){
        numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length; 
      }
      // make more reusable for later graphs...
      numberXMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = 0;

      if(Math.max(...tempData) > numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount]){
        numberYMax[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max.apply(Math,tempData) - 1;
      }
      numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min.apply(Math,tempData);

      let lineObjVizPlaceholder1 = [];
      Object.values(JSON.parse(JSON.stringify(props.dataObj))['lineObj']).map(i=>lineObjVizPlaceholder1.push(i));
      console.log("fuck shit graph 10");
      console.log("LINE OBJECT !! ", lineObjVizPlaceholder1);
      let syllablesPerLinePlaceholder = [];
      Object.values(lineObjVizPlaceholder1).map(j=>{if(j['syllablesInLine']){syllablesPerLinePlaceholder.push(j['syllablesInLine'])}});
      console.log("fuck shit graph 11");
      data.value = syllablesPerLinePlaceholder;
    }
    function updateVizDataSentiment(compound,negative,neutral,positive){
      console.log("fuck shit graph 12");
      hideUpdateButtons();
      console.log("fuck shit graph 13");
      let sentenceVizSentimentPlaceholder1 = [];

      try{
        console.log("HEY IN BUSINESS!!!! ", JSON.parse(JSON.stringify(this)));
        numberXMax.value = numberXMax.value.filter(i=>i);
        numberXMin.value = numberXMin.value.filter(i=>i);
        numberYMax.value = numberYMax.value.filter(i=>i);
        numberYMin.value = numberYMin.value.filter(i=>i);
        console.log("fuck shit graph 14");
      } catch(e){
        console.log("e1: ", e);
        console.log("fuck shit graph 15");
      }  
      try {
        console.log("fuck shit graph 16");
        Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj).map((i)=>{
          if(sentenceVizSentimentPlaceholder1.indexOf(Object.values(i)) === -1){
            sentenceVizSentimentPlaceholder1.push(Object.values(i));
          }
        });
      } catch(e){
        console.log("fuck shit graph 17");
        console.log("that object is not happy")
      }

      sentenceVizSentimentPlaceholder1.pop()
      // console.log("SENTIMENT MATRIX: ", sentenceVizSentimentPlaceholder1);
      let sentenceVizSentimentPlaceholder2 = [];
      sentenceVizSentimentPlaceholder1.map((i)=>sentenceVizSentimentPlaceholder2.push(i.map(j=>Object.values(j)[0])))
      // console.log("NEW Matrix: ", sentenceVizSentimentPlaceholder2);
      let tempData = [];
      Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj).filter(i=>i.sentenceSentiment)
      console.log("fuck shit graph 19");
      if(compound){
        tempData = sentenceVizSentimentPlaceholder2.map((i)=>i[0])
        valueY.value = "Sentiment (Compound)";
        valueX.value = "Sentence Count";
      
        numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length; 
        numberXMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = 0;
        if( Math.max(...tempData) > Math.max(numberYMax.value)){
          numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max(...tempData);
        }
        if( Math.min(...tempData) > Math.min(numberYMin.value)){
          numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min(...tempData);
        }
        Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj).map((i)=>{
          if(i.sentenceSentimentCompound){
            if(tempData.indexOf(Object.values(i.sentenceSentimentCompound)[0]) === -1){
              tempData.push(Object.values(i.sentenceSentimentCompound)[0])
            }
          }
        })
      }
      if(negative){
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[1])
        valueY.value = "Sentiment (Negative)";
        valueX.value = "Sentence Count";
        numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length;
        numberXMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = 0;
        if( Math.max(...tempData) > Math.max(numberYMax.value)){
          numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max.apply(Math,tempData);
        }
        if( Math.min(...tempData) > Math.min(numberYMax.value)){
          numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min.apply(Math,tempData); 
        }
        Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj).map((i)=>{
          if(i.sentenceSentimentNegative){
            if(tempData.indexOf(Object.values(i.sentenceSentimentNegative)[0]) === -1){
              tempData.push(Object.values(i.sentenceSentimentNegative)[0])
            }
          }
        })
      }
      if(neutral){
        valueY.value = "Sentiment (Neutral)";
        valueX.value = "Sentence Count";
        numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length;
        numberXMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = 0;
        if( Math.max(...tempData) > Math.max(numberYMax.value)){
          numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max(...tempData);
        } 
        if( Math.min(...tempData) > Math.min(numberYMin.value)){
          numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min(...tempData); 
        }
        Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj).map((i)=>{
          if(i.sentenceSentimentNeutral){
            tempData.push(Object.values(i.sentenceSentimentNeutral)[0])
          }
        })
      }
      if(positive){
        Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj).map((i)=>{   
          if(i.sentenceSentimentPositive){
            tempData.push(Object.values(i.sentenceSentimentPositive)[0]);
          }
        });

        valueY.value = "Sentiment (Positive)";
        valueX.value = "Sentence Count";

        numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length;
        numberXMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = 0;
        if( Math.max(...tempData) > Math.max(numberYMax.value)){
          numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max(...tempData);
        }
        if( Math.min(...tempData) < Math.min(numberYMin.value)){
          numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min(...tempData); 
        }

        numberXMax.value.filter(a=>typeof a === "number");
        numberXMin.value.filter(b=>typeof b === "number");
        numberYMax.value.filter(c=>typeof c === "number");
        numberYMin.value.filter(d=>typeof d === "number");

        mode.value[0] = 1;
        mode.value = [4];
      }
      console.log("fuck shit graph 20");
      data.value = tempData;
      if(!data.value){
        console.log("fuck shit graph 21");
        return;
      }
      console.log("fuck shit graph 22");
      numberXMax.value = numberXMax.value.filter(a=>typeof a === "number");
      numberXMin.value = numberXMin.value.filter(b=>typeof b === "number");
      numberYMax.value = numberYMax.value.filter(c=>typeof c === "number");
      numberYMin.value = numberYMin.value.filter(d=>typeof d === "number");
      
      console.log(`check on ... ${numberXMax.value} / ${numberXMin.value} / ${numberYMax.value} / ${numberYMin.value}`);
      console.log("fuck shit graph 23");
    }
      
    watch([props,
    props.dataObj, 
    tooltipMsg, 
    props.secondTextRef, 
    valueX,
    valueY,
    props.currentLinesCount,
    props.colorX,
    props.axisColorMatchBool,
    numberXMax,
    numberXMin,
    numberYMax,
    numberYMin,
    props.selectedXAxisRef,
    props.selectedYAxisRef,
    props.selectedRow,
    resetXRef, 
    resetYRef], ([currentXLabel,currentYLabel], [oldXLabel,oldYLabel]) => {
      console.log("fuck shit 100");
      console.log("fuck shit graph 24");
      if(Object.values(JSON.parse(JSON.stringify(props.dataObj))).length < 1){
        console.log("fuck shit graph 25");
        return;
      }
      if(numberXMax.value && resetXRef.value === true){
        console.log("fuck shit 101");
        console.log("fuck shit graph 26");
        let index = numberXMax.value.indexOf(Math.max(...numberXMax.value));
        numberXMax.value.slice(index);
        resetXRef.value = false;
        console.log("fuck shit graph 27");
        emit('numberYMax', numberYMax.value.filter(z=>typeof z === "number"));
      }
      if(numberXMin.value && resetXRef === true){
        console.log("fuck shit 102");
        let index = numberXMin.value.indexOf(Math.min(...numberXMin.value));
        numberXMin.value.slice(index);
        resetXRef.value = false;
        console.log("fuck shit graph 28");
        emit('numberXMin', numberXMin.value.filter(g=>typeof g === "number"));
      }
      if(numberYMax.value && resetYRef === true){
        console.log("fuck shit 103");
        let index = numberYMax.value.indexOf(Math.max(...numberYMax.value));
        numberYMax.value.slice(index);
        resetYRef.value = false;
        console.log("fuck shit graph 29");
        emit('numberYMax', numberYMax.value.filter(g=>typeof g === "number"));
      }
      if(numberYMin.value && resetYRef === true){
        console.log("fuck shit 104");
        let index = numberYMin.value.indexOf(Math.max(...numberYMin.value));
        numberYMin.value.slice(index);
        resetYRef.value = false;
        console.log("fuck shit graph 30");
        emit('numberYMin', numberYMin.value.filter(g=>typeof g === "number"));
      }
      if(resetYRef.value === true){
        console.log("fuck shit 105");
        let index = JSON.parse(JSON.stringify(numberYMax.value)).indexOf(Math.max(...numberYMax.value));
        JSON.parse(JSON.stringify(numberYMax.value)).slice(index);
        resetYRef.value = false;
        console.log("fuck shit graph 31");
      }
      if(currentXLabel !== oldXLabel){
        console.log("fuck shit 106");
        console.log('curr x label val: ', JSON.parse(JSON.stringify(valueX.value)));
        console.log("fuck shit graph 32");
        emit('dataname_x', valueX.value);
       
      }
      if(currentYLabel !== oldYLabel){
        console.log("fuck shit 107");
        console.log('curr y label val: ', JSON.parse(JSON.stringify(valueY.value)));
        emit('dataname_y',valueY.value);
      }
      console.log("fuck shit 108");
      console.log("fuck shit graph 33");
      let keyBuilder = document.getElementById("d3UpdateButtonsWrapper");
      if(keyBuilder){
        console.log("fuck shit 109");
        keyBuilder.style.borderColor = props.colorX;
      }
      if(valueX.value){
        console.log("fuck shit 110");
        emit('dataname_x',valueX.value)
      } 
      if(valueY.value){
        console.log("fuck shit 111");
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
    console.log("fuck shit graph 36");
      console.log("IN UPDATE TOOLTIP!!! ", selected);
      let grammarArr = [];
      let entitiesArr = [];

        console.log("selected ", selected)
      if(Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5][selected]){
        Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5][selected]['sentenceGrammarArray'].forEach((g)=>{
          console.log("STILL PUSHING GRAMMAR FINE!")
          grammarArr.push({'tokenTag':g.tokenTag,'tokenPos':g.tokenPos,'tokenText':g.tokenText})
        });
        Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5][selected]['sentenceSpacyEntities'].forEach((h)=>{
          console.log("STILL PUSHING ENTITIES FINE!", h)
          if(entitiesArr.indexOf(h.id) === -1 || entitiesArr.indexOf(h.text) === -1){
            entitiesArr.push([h.text,h.type,h.id])
          }
        });
        console.log("fuck shit graph 37");
        tooltipMsg.value = {
          grammarArrays : Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5][selected]['sentenceGrammarArray'],
          sentimentCompound : Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5][selected]['sentenceSentimentCompound']['compound'],
          sentimentNegative : Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5][selected]['sentenceSentimentNegative']['neg'],
          sentimentNeutral : Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5][selected]['sentenceSentimentNeutral']['neu'],
          sentimentPositive : Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5][selected]['sentenceSentimentPositive']['pos'],
          entityArrays : Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5][selected]['sentenceSpacyEntities']
        }
        console.log("$$$ ", JSON.parse(JSON.stringify(tooltipMsg.value)));
      } else {
        console.log("fuck shit graph 38");
        console.log("tooltip failure: ", Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5]);
      }
  }
  function tryToggleComparative(){
    props.graphstate = props.graphstate + 1;
  }
  
  function emitterClose(command){
    console.log("fuck shit graph 39");
    console.log("emitting");
    emit(command);
  }
  </script>
 
  

<script>

  // import * as d3 from 'd3';
  
  export default {
    name: "GraphModal",
    components: {
      // AreaChart,
      TestChart
    },
    emits : ['dataname_y','dataname_x','dataCountX', 'dataCountY','closeUpdatePopup','numberXMax','numberXMin','numberYMax','numberYMin'],
    watch: 
    {
      dataname_x:{
        deep: true,
        handler: function(newVal, oldVal){
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
      },
      dataname_y:{
        deep: true,
        handler: function(newVal, oldVal){
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
      },
      numberXMax:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("num x changes")
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
      },
      numberYMax:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("num x changes")
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
      },
      numberXMin:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("num y changes")
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
      },
      numberYMin:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("num y changes")
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
      },
    },
    // [
    //   'dataname_x',
    //   'dataname_y',
    //   'numberXMin',
    //   'numberXMax',
    //   'numberYMin',
    //   'numberYMax'],
    props : {
      open: {
        type: Boolean,
        // is this right???
        default: () => (false),
      },
      dataObj: {
        type: Object,
        default: () => ({}),
      },
      graphstate: {
        type: Number,
        default: () => (0),
      },
      color0: {
        type: String,
        default: () => (''),
      },
      color1: {
        type: String,
        default: () => (''),
      },
      color2: {
        type: String,
        default: () => (''),
      },
      color3: {
        type: String,
        default: () => (''),
      },
      colorX: {
        type: String,
        default: () => (''),
      },
      colorY: {
        type: String,
        default: () => (''),
      },
      secondTextRef: {
        type: Boolean,
        default: () => (false),
      },
      currentLinesCount: {
        type: Number,
        default: () => (0),
      },
      axisColorMatchBool: {
        type: Boolean,
        default: () => (true),
      },
      selectedXAxisRef: {
        type: Object,
        default: () => ({}),
      },
      selectedYAxisRef: {
        type: Object,
        default: () => ({}),
      },
      label: {
        type: String,
        default: () => (''),
      },
      value: {
        type: Array,
        default: () => ([]),
      },
      isIndex: {
        type: Boolean,
        default: () => (false),
      },
      selectedRow: {
        type: Number,
        default: () => (0),
      },
    },
  
    data() {
      return {
        data:[],
        currentXName: "X_",
        currentYName: "Y_",
        // mode:[1],
        points: [],
        // popupOpen: false,
        paths: {
          area: '',
          line: '',
          selector: '',
        },
        width:null,
        height:null,
        color:null,
        // numberXMaxData: [],
        // numberXMinData: [],
        // numberYMaxData: [],
        // numberYMinData: [],
        valueX: 'initX',
        valueY: 'initY',

      };
    },
    // mounted() {
    //   console.log("CHECK MOUNTED PROPS IN GRAPHMODAL: ", JSON.parse(JSON.stringify(this.props)));
    // },
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
     
    }
    }
  };
  
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
        :yAxisFramingLast="yAxisFramingLast"
        @selected="updateTooltip"
        :currentLinesCount="props.currentLinesCount"
        :color0="props.color0"
        :color1="props.color1"
        :color2="props.color2"
        :color3="props.color3"  
        :numberXMax="numberXMax"
        :numberXMin="numberXMin"
        :numberYMax="numberYMax"
        :numberYMin="numberYMin"
        :colorX="props.colorX"
        :colorY="props.colorY"
        :valueX="valueX"
        :valueY="valueY"

        :axisColorMatchBool="axisColorMatchBool"
        :graphstate="props.graphstate" 
        @toggleComparative="tryToggleComparative" 
   
       >
      </TestChart>

    
      <div class="buttons" >
      <!-- BRING BACK SOON! -->
        <!-- <button class="green-btn bottom-btn" @click="addData">Add data</button>
        <button class="green-btn bottom-btn" @click="filterData">Filter data</button> -->
        <div id="d3UpdateButtonsWrapper">
          <h1 id="buttonsWrapperTitle">Update Graph</h1>
          <h3 id="buttonsWrapperSubtitle">
            Reopen this window any time you'd like to update the data displayed in the graph. Select a value to track with your first line.
          </h3>
          <div id="buttonsInnerWrapper">
            <div id="sentimentBtns">
              <span class="label-wrapper">
                <span class="buttons-row">
                  <button class="green-btn" @click="updateVizDataSentiment(false,false,false,true); emitterClose('closeUpdatePopup')">Pos</button>
                  <button class="green-btn" @click="updateVizDataSentiment(true,false,false,false); emitterClose('closeUpdatePopup')">Comp</button>
                  <button class="green-btn" @click="updateVizDataSentiment(false,true,false,false); emitterClose('closeUpdatePopup')">Neg</button>
                  <button class="green-btn" @click="updateVizDataSentiment(false,false,true,false); emitterClose('closeUpdatePopup')">Neu</button>
                </span>
                <span>Sentiment Scores</span>
                <br/>
              </span>
            </div>
            <br/>
            
            <div class="inner-wrap">

              <span class="buttons-row">
                <div id="textStatsBtns">
                  <span class="label-wrapper">
                    <button class="green-btn" @click="updateVizDataCommonWords(); emitterClose('closeUpdatePopup')">Common Words</button>
                    <span>Text-Level Statistics</span>
                  </span>
                </div>
                <div id="lineStatsBtns">                      
                  <span class="label-wrapper">
                    <button class="green-btn" @click="updateVizDataLineObj(); emitterClose('closeUpdatePopup')">Syllables Per Line</button>
                    <span>Line-Level Analysis</span>
                  </span>
                </div>
              </span>

            </div>
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
  top: 16%;
  height: calc(76%);
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

    bottom: 0px;
    left: 0px;
    right:0px;
    position: absolute;
}
#button {
  background-color: green;
}
#sentimentBtns,#textStatsBtns,#lineStatsBtns{
  display: flex;
  width: 100%;
  justify-content: center;
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
    width: calc(100%);

    flex-direction: row;
    position: fixed;
    background: var(--color-background);
    background-color: var(--color-background);
    border-radius: 8px;

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
  display: flex;
  flex-direction: column;
  align-items: center;
}
.label-wrapper {
  display:flex;
  flex-direction: column;
}
.buttons-row {
  display: flex;
  flex-direction: row;
  width: 100%;
  padding: 2%;
}
.inner-wrap {
  width:100%;
  flex-direction: row;
  display:flex;
  justify-content: center;
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