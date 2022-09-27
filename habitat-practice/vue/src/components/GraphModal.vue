<script setup>
  import BarChart from './BarChart.vue';
  import TestChart from './TestChart.vue';
  import {watch, ref,onMounted} from 'vue';

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
    preservedDataLine1: Object,
    
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
  
  const emit = defineEmits(['numberXMin','numberXMax','numberYMin','numberYMax','dataname_y', 'dataname_x','closeUpdatePopup','dataHolder1Grandparent']); 
  
  const inGraphsParent = ref(false)
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
  // const dataHolder1Parent = [];
 
  const grammarArr = ref([]);
  const entitiesArr = ref([]);
  const savedLineOneDataObj = ref({})


  // onMounted(()=>{
  const dataHolder1Parent = ref({});
  //dataHolder1Parent.value = JSON.parse(JSON.stringify(props)).preservedDataLine1;
      //   return dataHolder1Parent;
      // })

//RITA! --> THIS WORKS!!!
  let words = window.RiTa.stresses("The elephant took a bite!")
    // for (let i=0; i < words.length; i++) {
    //     text(words[i], 50, 50 + i*20);
    // }
    // console.log(words);

    async function locateClientX(x){
      let popupTextWindow = await document.getElementById("grammarDisplayWrapper")
        // console.log("what is X? ", x);
        // console.log("what is inner width? ", window.innerWidth);
        if (popupTextWindow && (window.innerWidth - x) > 200){
          popupTextWindow.style.left = `${x}px` 
        } else {
          // clientX.value=x-200;
          popupTextWindow.style.left = `${x-150}px` 
        }
      }
      async function locateClientY(y){
        let popupTextWindow = await document.getElementById("grammarDisplayWrapper")
        // console.log("Y IS ", y)
        if(popupTextWindow && y < 80){
          popupTextWindow.style.top= `${y + 40}px`;
        } else if(y > window.innerHeight - 200) {
          popupTextWindow.style.top= `${y - 150}px`;
        } else {
          popupTextWindow.style.top= `${y}px`;
          popupTextWindow.style.backgroundColor = "transparent";
        }


      }





      function dataholderemit1(newData1Holder){ 
 
      }



  function hideUpdateButtons(){
    let graph = document.getElementById("svgId");
    if(graph){
      graph.style.bottom = "16%";
    }
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
      hideUpdateButtons();
      data.value = JSON.parse(JSON.stringify(props)).dataObj.textObj.mostCommonWords.map(i=>i['occurances']);
        let tempData = data.value.map(i=>i);
        valueY.value = "Occurances";
        valueX.value = "Items";
        // console.log("is thissss the problem? check temp data", tempData)
        if(tempData.length > 0){

        } else {
          return
        }
        numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length - 1; 
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
          numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length - 1; 
        }
        numberXMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = 0;
        if(Math.max(...tempData) > numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount]){
          numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max.apply(Math,tempData);
        }
        numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length - 1; 
        numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min.apply(Math,tempData);
        //console.log("common words in GM: ", numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount - 1]);
        //console.log("common words in GM: ", this.numberXMax[this.props.currentLinesCount - 1]);
    }
    function updateVizDataLineObj(){
      hideUpdateButtons();
      Object.keys(JSON.parse(JSON.stringify(props.dataObj))['lineObj']).slice(-1)
      data.value = Object.values(JSON.parse(JSON.stringify(props.dataObj))['lineObj']).map(i=>i['syllablesInLine']);
    
      // this is only necessary if it is stopping point errors
      let tempData = data.map(i=>i);
      valueY.value = "Syllable Count";
      valueX.value = "Sentence Count";
      //console.log("THIS CURR LINES COUNT: ", this.numberXMax[this.props.currentLinesCount]);

      numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length - 1; 
      numberXMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = 0;
      if( Math.max(...tempData) > Math.max(numberYMax.value)){
        numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max(...tempData)
      }
      if( Math.min(...tempData) < Math.min(numberYMin.value)){
        numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min(...tempData);
      }
      numberXMax.value = numberXMax.value.filter(q=>typeof q === "number");
      numberXMin.value = numberXMin.value.filter(r=>typeof r === "number");
      numberYMax.value = numberYMax.value.filter(s=>typeof s === "number");
      numberYMin.value = numberYMin.value.filter(t=>typeof t === "number");

      if(tempData.length > numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount]){
        numberXMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = tempData.length - 1; 
      }
      // make more reusable for later graphs...
      numberXMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = 0;

      if(Math.max(...tempData) > numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount]){
        numberYMax[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max.apply(Math,tempData) - 1;
      }
      numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min.apply(Math,tempData);

      let lineObjVizPlaceholder1 = [];
      Object.values(JSON.parse(JSON.stringify(props.dataObj))['lineObj']).map(i=>lineObjVizPlaceholder1.push(i));
      //console.log("LINE OBJECT !! ", lineObjVizPlaceholder1);
      let syllablesPerLinePlaceholder = [];
      Object.values(lineObjVizPlaceholder1).map(j=>{if(j['syllablesInLine']){syllablesPerLinePlaceholder.push(j['syllablesInLine'])}});
      data.value = syllablesPerLinePlaceholder;
    }
    
    function updateVizDataSentiment(compound,negative,neutral,positive){

      if(JSON.parse(JSON.stringify(props)).graphstate === 0){
        let preservedValsText1 = Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj)
       // console.log("PRESERVED VALS TEXT 1: ", preservedValsText1);
        emit('dataHolder1Grandparent', JSON.stringify(preservedValsText1))
      }

      let graph = document.getElementById("svgId");
      
      let moveableGrammarWrapper = document.getElementById("grammarDisplayWrapper");
      if(moveableGrammarWrapper){
        moveableGrammarWrapper.style.display = 'inline-block';
      }
      let modalHead = document.getElementById("modalHead");
      if(modalHead){
        modalHead.style.display = 'flex';
      }
      hideUpdateButtons();


   
      let sentenceVizSentimentPlaceholder1 = [];
      let sentenceVizSentimentPlaceholder1_Saved = []; 

      //console.log("AHHHHHH! ", JSON.parse(JSON.stringify(numberXMax.value)))
      try{
        //console.log("HEY IN BUSINESS!!!! ", JSON.parse(JSON.stringify(this)));
       
        // numberXMax.value = Math.max(...data.value.length);
        numberXMin.value = numberXMin.value.filter(i=>typeof i === "number");
        numberYMax.value = numberYMax.value.filter(i=>typeof i === "number");
        numberYMin.value = numberYMin.value.filter(i=>typeof i === "number");

      } catch(e){
        console.log("not in business: ", e);
      }  
      try {
        Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj).map((i)=>{
          if(sentenceVizSentimentPlaceholder1.indexOf(Object.values(i)) === -1){
            sentenceVizSentimentPlaceholder1.push(Object.values(i));
          } 
        });
      } catch(e){
      try {
        Object.values(JSON.parse(JSON.stringify(props)).preservedDataLine1.sentenceObj).map((i)=>{
          if(sentenceVizSentimentPlaceholder1_Saved.indexOf(Object.values(i)) === -1){
            sentenceVizSentimentPlaceholder1_Saved.push(Object.values(i));
          } 
        });
      } catch {

      }
      }
      
      //console.log("!!!!!! ", Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5])
      // sessionStorage.setItem("line1Data", Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5]);
      
      //console.log("WORKS@@ ", testSessionStorage);


      if(!sentenceVizSentimentPlaceholder1){
        return;
      }

      sentenceVizSentimentPlaceholder1.pop()
      if(sentenceVizSentimentPlaceholder1_Saved){
        sentenceVizSentimentPlaceholder1_Saved.pop();
      }
      // console.log("SENTIMENT MATRIX: ", sentenceVizSentimentPlaceholder1);
      let sentenceVizSentimentPlaceholder2 = [];
      let sentenceVizSentimentPlaceholder2_Saved = [];

      sentenceVizSentimentPlaceholder1.map((i)=>sentenceVizSentimentPlaceholder2.push(i.map(j=>Object.values(j)[0])))
      // if(sentenceVizSentimentPlaceholder1_Saved){
  
      // }

      // sentenceVizSentimentPlaceholder1_Saved.map((i)=>sentenceVizSentimentPlaceholder2_Saved.push(i.map(j=>Object.values(j)[0])))
      // if(sentenceVizSentimentPlaceholder1_Saved.length){
      sentenceVizSentimentPlaceholder1_Saved.map((i)=>sentenceVizSentimentPlaceholder2_Saved.push(i.map(j=>Object.values(j)[0])))
      // }
        // console.log("NEW Matrix: ", sentenceVizSentimentPlaceholder2);
      let tempData = [];
      let tempDataSaved = [];
      Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj).filter(i=>i.sentenceSentiment)
      // if(props.preservedDataLine1){
        Object.values(JSON.parse(JSON.stringify(props)).preservedDataLine1).filter(i=>i.sentenceSentiment);

      // }

////
if(JSON.parse(JSON.stringify(tempData)).length > JSON.parse(JSON.stringify(tempDataSaved)).length || !tempDataSaved){
          numberXMax.value[JSON.parse(JSON.stringify(props.currentLinesCount))] = JSON.parse(JSON.stringify(tempData)).length - 1; 
        } else {
          numberXMax.value[JSON.parse(JSON.stringify(props.currentLinesCount))] = JSON.parse(JSON.stringify(tempDataSaved)).length - 1; 
        }
        numberXMin.value[JSON.parse(JSON.stringify(props.currentLinesCount))] = 0;
        if(Math.max(...tempData) > Math.max(...tempDataSaved) || !tempDataSaved){
          if( Math.max(...tempData) > Math.max(numberYMax.value)){
            numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max(...tempData);
          }
        } else {
          if( Math.max(...tempDataSaved) > Math.max(numberYMax.value)){
            numberYMax.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.max(...tempDataSaved);
          }
        }
        if(Math.min(...tempData) < Math.min(...tempDataSaved) || !tempDataSaved){
          if( Math.min(...tempData) < Math.min(numberYMin.value)){
            numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min(...tempData);
          }
        } else {
          if( Math.min(...tempData) < Math.min(numberYMin.value)){
            numberYMin.value[JSON.parse(JSON.stringify(props)).currentLinesCount] = Math.min(...tempDataSaved);
          }
        }
        numberXMax.value.filter(a=>typeof a === "number");
        numberXMin.value.filter(b=>typeof b === "number");
        numberYMax.value.filter(c=>typeof c === "number");
        numberYMin.value.filter(d=>typeof d === "number");
////


      if(compound){

        let updatePopup = document.getElementById("d3UpdateButtonsWrapper");
        if(updatePopup){
          // console.log("ADD A CHECK HERE FOR IN GRAPHS");
          updatePopup.classList.add("animate-close");
        }

        inGraphsParent.value = true;
        //console.log("in compound ** ", sentenceVizSentimentPlaceholder2);
        //console.log("in compound **saved ", sentenceVizSentimentPlaceholder2_Saved);
        tempData = sentenceVizSentimentPlaceholder2.map((i)=>i[0])
        tempDataSaved = sentenceVizSentimentPlaceholder2_Saved.map((i)=>i[1])
        //console.log("in compound ", tempData);
        valueY.value = "Sentiment (Compound)";
        valueX.value = "Sentence Count";
        //console.log("currrrrr lines count: ", JSON.parse(JSON.stringify(props.currentLinesCount)));



        Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj).map((i)=>{
          if(i.sentenceSentimentCompound){
            // call self-building spinner here
            // console.log("CURR LINES - 1 ", JSON.parse(JSON.stringify(props)).currentLinesCount -1);
            if(tempData.indexOf(Object.values(i.sentenceSentimentCompound)[0]) === -1){
              //console.log("pushing into compound tempdata: ", Object.values(i.sentenceSentimentCompound)[JSON.parse(JSON.stringify(props)).currentLinesCount -1])
              tempData.push(Object.values(i.sentenceSentimentCompound)[0])
            }
          }
        })
        // if(props.preservedDataLine1){
          Object.values(JSON.parse(JSON.stringify(props)).preservedDataLine1).map((i)=>{
            if(i.sentenceSentimentCompound){
              // call self-building spinner here
              // console.log("CURR LINES - 1 ", JSON.parse(JSON.stringify(props)).currentLinesCount -1);
              if(tempDataSaved.indexOf(Object.values(i.sentenceSentimentCompound)[0]) === -1){
                tempDataSaved.push(Object.values(i.sentenceSentimentCompound)[0])

              }
            }
          })
         //console.log("TEMP DATA SAVED IS... ", tempDataSaved);
        // }
      }
      if(negative){
        let updatePopup = document.getElementById("d3UpdateButtonsWrapper");
        if(updatePopup){
          // console.log("ADD A CHECK HERE FOR IN GRAPHS");
          updatePopup.classList.add("animate-close");
        }
        inGraphsParent.value = true;
   
        console.log("nonsense: ",sentenceVizSentimentPlaceholder2_Saved);
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[1])
        tempDataSaved = sentenceVizSentimentPlaceholder2_Saved.map((i)=>i[1])

        valueY.value = "Sentiment (Negative)";
        valueX.value = "Sentence Count";
        
        Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj).map((i)=>{
          if(i.sentenceSentimentNegative){
            if(tempData.indexOf(Object.values(i.sentenceSentimentNegative)[0]) === -1){
              tempData.push(Object.values(i.sentenceSentimentNegative)[0])
            }
          }
        })

        if(JSON.parse(JSON.stringify(props)).preservedDataLine1){
          tempDataSaved = sentenceVizSentimentPlaceholder2_Saved.map((i)=>i[1])
          let negat = Object.values(JSON.parse(JSON.stringify(props)).preservedDataLine1);
      
          negat.map((i)=>{
            if(Object.values(i)[1]){
              if(tempDataSaved.indexOf(Object.values(i)[1]) && tempDataSaved.indexOf(Object.values(Object.values(i)[1])) === -1){
                tempDataSaved.push(Object.values(Object.values(i)[1])[0]);
              }
            }
          })
        }
      }
      if(neutral){
        let updatePopup = document.getElementById("d3UpdateButtonsWrapper");
        if(updatePopup){
          updatePopup.classList.add("animate-close");
        }
        inGraphsParent.value = true;
        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[2])
        tempDataSaved = sentenceVizSentimentPlaceholder2_Saved.map(i=>i[2])        
        valueY.value = "Sentiment (Neutral)";
        valueX.value = "Sentence Count";
        
        Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj).map((i)=>{
          if(i.sentenceSentimentNeutral){
            if(tempData.indexOf(Object.values(i.sentenceSentimentNeutral)[0]) === -1){
              tempData.push(Object.values(i.sentenceSentimentNeutral)[0]);
            }
          }
        })
        if(JSON.parse(JSON.stringify(props)).preservedDataLine1){
          tempDataSaved = sentenceVizSentimentPlaceholder2_Saved.map((i)=>i[2])
          let neut = Object.values(JSON.parse(JSON.stringify(props)).preservedDataLine1);
      
          neut.map((i)=>{
            if(Object.values(i)[2]){
              if(tempDataSaved.indexOf(Object.values(i)[2]) && tempDataSaved.indexOf(Object.values(Object.values(i)[2])) === -1){
                tempDataSaved.push(Object.values(Object.values(i)[2])[0]);
              }
            }
          })
        }
      }
      if(positive){
        inGraphsParent.value = true;
        Object.values(JSON.parse(JSON.stringify(props)).dataObj.sentenceObj).map((i)=>{   
          if(i.sentenceSentimentPositive && Object.values(i.sentenceSentimentPositive)[0].length > 0){
            tempData.push(Object.values(i.sentenceSentimentPositive)[0]);
          }
        });
        valueY.value = "Sentiment (Positive)";
        valueX.value = "Sentence Count";

        tempData = sentenceVizSentimentPlaceholder2.map(i=>i[3])
        tempDataSaved = sentenceVizSentimentPlaceholder2_Saved.map((i)=>i[3])
       
        mode.value[0] = 1;
        mode.value = [4];


        if(JSON.parse(JSON.stringify(props)).preservedDataLine1){
          tempDataSaved = sentenceVizSentimentPlaceholder2_Saved.map((i)=>i[1])
          let posArr = Object.values(JSON.parse(JSON.stringify(props)).preservedDataLine1);
      
          posArr.map((i)=>{
            if(Object.values(i)[3]){
              if(tempDataSaved.indexOf(Object.values(i)[3]) && tempDataSaved.indexOf(Object.values(Object.values(i)[3])) === -1){
                tempDataSaved.push(Object.values(Object.values(i)[3])[0]);
              }
            }
          })
        }

      }

      //console.log("WHAT IS TEMPDATA??? ", tempData);
      //console.log("WHAT IS TEMPDATA_SAVED??? ", tempDataSaved);
      dataHolder1Parent.value = tempDataSaved;
      if(props.graphstate === 0 && tempData.length > 0 && tempData !== undefined && tempData !== null && tempData !== {}){
        if(!tempData){
          return;
        }
        dataHolder1Parent.value = tempDataSaved;
      } else {
        
      }
      data.value = tempData;
      if(!data.value){
        return;
      }
      numberXMax.value = numberXMax.value.filter(a=>typeof a === "number");
      numberXMin.value = numberXMin.value.filter(b=>typeof b === "number");
      numberYMax.value = numberYMax.value.filter(c=>typeof c === "number");
      numberYMin.value = numberYMin.value.filter(d=>typeof d === "number");
      
      //why is ymin not coming through?
      //console.log(`check on ... ${numberXMax.value} / ${numberXMin.value} / ${numberYMax.value} / ${numberYMin.value}`);
    }
      
    watch([
      props,
    // dataObj, 

    tooltipMsg, 
    // dataHolder1Parent,
    // secondTextRef, 
    valueX,
    valueY,
    // currentLinesCount,
    // colorX,
    // axisColorMatchBool,
    numberXMax,
    numberXMin,
    numberYMax,
    numberYMin,
    // selectedXAxisRef,
    // selectedYAxisRef,
    // selectedRow,
    resetXRef, 
    resetYRef], ([currentXLabel,currentYLabel], [oldXLabel,oldYLabel]) => {
      if(Object.values(JSON.parse(JSON.stringify(props.dataObj))).length < 1){
        return;
      } else {

      }

      // if(inGraphsParent.value !== true){
      //   return
      // }
      //console.log("RESET REF: ", resetXRef.value)

      if(JSON.parse(JSON.stringify(numberXMax.value)) && resetXRef.value === true){
        let index = numberXMax.value.indexOf(Math.max(...numberXMax.value));
        numberXMax.value.slice(index);
        resetXRef.value = false;
        // console.log("WHAT AM I EMITTING??? YMAX", numberYMax.value.filter(z=>typeof z === "number"));
        emit('numberYMax', numberYMax.value.filter(z=>typeof z === "number"));
      }
      if(JSON.parse(JSON.stringify(numberXMin.value)) && resetXRef.value === true){
        let index = numberXMin.value.indexOf(Math.min(...numberXMin.value));
        numberXMin.value.slice(index);
        resetXRef.value = false;
        //console.log("WHAT AM I EMITTING??? XMAX", numberXMax.value.filter(z=>typeof z === "number"));
        emit('numberXMin', numberXMin.value.filter(g=>typeof g === "number"));
      }
      if(JSON.parse(JSON.stringify(numberYMax.value)) && resetYRef.value === true){
        let index = numberYMax.value.indexOf(Math.max(...numberYMax.value));
        numberYMax.value.slice(index);
        resetYRef.value = false;
        //console.log("WHAT AM I EMITTING??? YMAX", numberYMax.value.filter(z=>typeof z === "number"));
        emit('numberYMax', numberYMax.value.filter(g=>typeof g === "number"));
      }
      if(JSON.parse(JSON.stringify(numberYMin.value)) && resetYRef.value === true){
        let index = numberYMin.value.indexOf(Math.min(...numberYMin.value));
        numberYMin.value.slice(index);
        resetYRef.value = false;
        //console.log("WHAT AM I EMITTING??? YMIN", numberYMin.value.filter(z=>typeof z === "number"));
        emit('numberYMin', numberYMin.value.filter(g=>typeof g === "number"));
      }
      if(resetYRef.value === true){
        let index = JSON.parse(JSON.stringify(numberYMax.value)).indexOf(Math.max(...numberYMax.value));
        JSON.parse(JSON.stringify(numberYMax.value)).slice(index);
        resetYRef.value = false;
      }
      if(currentXLabel !== oldXLabel){
        //console.log('curr x label val: ', JSON.parse(JSON.stringify(valueX.value)));
        emit('dataname_x', valueX.value);
       
      }
      if(currentYLabel !== oldYLabel){
        //console.log('curr y label val: ', JSON.parse(JSON.stringify(valueY.value)));
        emit('dataname_y',valueY.value);
      }

      if(valueX.value){
        emit('dataname_x',valueX.value)
      } 
      if(valueY.value){
        emit('dataname_y',valueY.value)

      }

      let keyBuilder = document.getElementById("d3UpdateButtonsWrapper");
      if(keyBuilder){
        keyBuilder.style.borderColor = props.colorX;
      }

      return;
    });
    
    function resetX(){
      resetXRef.value = true;
    }
    
    function resetY(){
      resetYRef.value = true;
    }
  
  function updateTooltipGrammarText(g){
    var innerGrammarDisplayEntities = document.getElementById("grammarDisplayWrapper");
    let t = document.getElementsByClassName("displayed-grammar");
    let s = document.querySelector(".createdGrammarWrapper");
    if(t && t.length > 0){
      for(let i=0;i<t.length;i++){
        if(i !== t.length-1){
         t[i].remove();
        }
      }
      
    }

 
    var c = document.createDocumentFragment();
    c.className = "createdGrammarWrapper"; 
    
    let stopDupe = document.getElementById(g['tokenText'] + "_" + g['sentenceIndex']  + "_" + g['idx_in_sents'])
    if(stopDupe){
      // console.log("FOUND MATCH!!!!!!")
      return;
    }
    let removedShown = document.getElementsByClassName("createdGrammarWrapper");
    if(removedShown){
      for(let s = 0; s < removedShown.length; s++){
        c.remove(removedShown[s]);
      }
    } 

    let e = document.createElement("span");
    e.id = g['tokenText'] + "_" + g['sentenceIndex']  + "_" + g['idx_in_sents']; 
    e.className = "displayed-grammar";
    let text = g['tokenText'];
    e.append(text);
    e.style.fontSize = "18px";
    e.style.paddingRight = "4px";
    e.style.paddingLeft = "4px";
    e.style.paddingTop = "1px";
    e.style.paddingBottom = "1px";
    // console.log("tag: ", g['tokenTag'])
    switch(g['tokenTag']){
      case "CC":
        // coordinating conjunction
        e.style.backgroundColor = "#c1dbd7"
        e.style.color = "rgba(0,0,0,1)";
        break;
      case "CD":
        // numeral cardinal
        e.style.backgroundColor = "#949FB3";
        break;
      case "DT":
        // determiner
        e.style.backgroundColor = "#c1dbd7"
        e.style.color = "rgba(0,0,0,1)";
        break;
      case "EX":
        // existential there
        e.style.backgroundColor = "#94B3A5";
        break;
      case "JJ":
        // adjective or ordinal numeral
        e.style.backgroundColor = "#E6CECA";
        e.style.color = "#000000";
        break;
      case "JJR":
        // comparative adjective
        e.style.backgroundColor = "#E6CECA";
        e.style.color = "#000000";
        break;
      case "JJS":
        // superlative adjective
        e.style.backgroundColor = "#E6CECA";
        e.style.color = "#000000";
        break;
      case "LS":
        // list item marker
        e.style.backgroundColor = "#c1dbd7"
        e.style.color = "rgba(0,0,0,1)";
        break;
      case "MD":
        // modal auxiliary
        e.style.backgroundColor = "#c1dbd7"
        e.style.color = "rgba(0,0,0,1)";
        break;
      case "NN":
        // noun, common, singular or mass
        e.style.backgroundColor = "#e6e4d6";
        e.style.color = "rgba(0,0,0,1)";
 
        break;
      case "NNP":
        // noun, proper, singular
        e.style.backgroundColor = "#e6e4d6";
        e.style.color = "rgba(0,0,0,1)";
    
        break;
      case "NNPS":
        // noun, proper, plural
        e.style.backgroundColor = "#e6e4d6";
        e.style.color = "rgba(0,0,0,1)";
        break;
      case "NNS":
        // noun, common, plural
        e.style.backgroundColor = "#e6e4d6";
        e.style.color = "rgba(0,0,0,1)";
        break;
      case "PRP$":
        // possessive pronoun
        e.style.backgroundColor = "#c1dbd7";
        e.style.color = "rgba(0,0,0,1)";
        break;
      case "RB":
        // adverb
        e.style.backgroundColor = "#EAE093";
        e.style.color = "#000000";
        break;
      case "RBR":
        // comparative adverb
        e.style.backgroundColor = "#EAE093";
        e.style.color = "#000000";
        break;
      case "RBS":
        // superlative adverb
        e.style.backgroundColor = "#EAE093";
        e.style.color = "#000000";
        break;
      case "PRP":
        // personal pronoun
        e.style.backgroundColor = "#c1dbd7";
        e.style.color = "#000000";
        // e.style.border = "solid 0.5px rgba(0,0,0,1)";
        break;
      case "RP":
        // particle
        e.style.backgroundColor = "var(--color-background)";
        e.style.color = "#e6e4d6";
        break;
      case "TO":
        //  "to" as preposition or infinitive marker
        e.style.backgroundColor = "#c1dbd7";
        e.style.color = "#000000";
        break;
      case "UH":
        // interjection
        e.style.backgroundColor = "#E6CECA";
        e.style.color = "#000000";
        break;
      case "VB":
        // verb base form
        // e.style.color = "#e6e4d6";
        // e.style.backgroundColor = "rgba(0,0,0,1)";
        e.style.backgroundColor = "#9ea5e9";
        e.style.color = "#000000";
        // e.style.border = "solid 0.5px rgba(0,0,0,1)";
        break;
      case "VBD":
        // past tense
        e.style.backgroundColor = "#9ea5e9";
        e.style.color = "#000000";
        break;
      case "VBG":
        // present participle / gerund
        // e.style.color = "#e6e4d6";
        // e.style.backgroundColor = "rgba(0,0,0,1)";
        e.style.backgroundColor = "#9ea5e9";
        e.style.color = "#000000";
        break;
      case "VBN":
        // past participle
        e.style.backgroundColor = "#9ea5e9";
        e.style.color = "#000000";
        break;
      case "VBP":
        // present tense verb (not 3rd person singular)
        e.style.backgroundColor = "#9ea5e9";
        e.style.color = "#000000";
        break;
      case "VBZ":
        // present tense verb 3rd person singular
        // e.style.color = "#e6e4d6";
        // e.style.backgroundColor = "rgba(0,0,0,1)";
        e.style.backgroundColor = "#9ea5e9";
        e.style.color = "#000000";
        break;
      case "WDT":
        // WH determiner (that what whatever which)
        e.style.backgroundColor = "#c1dbd7";
        e.style.color = "rgba(0,0,0,1)";
        break;
      case "WP":
        // WH pronoun (that what whatever whatsoever which who whom whosoever)
        e.style.backgroundColor = "#c1dbd7"
        e.style.color = "rgba(0,0,0,1)";
        // e.style.border = "solid 0.5px rgba(0,0,0,1)";
        break;
      case "WRB":
        // WH Adverb (how however whence whenever where whereby whereever wherein whereof why)
        e.style.backgroundColor = "#EAE093";
        e.style.color = "rgba(0,0,0,1)";
        // e.style.border = "solid 0.5px rgba(0,0,0,1)";
        break;
      case "POS":
        // genitive marker
        e.style.backgroundColor = "#c1dbd7"
        e.style.color = "rgba(0,0,0,1)";
        break;
      case "PUNCT":
        e.style.color = "#000000";
        break;
      case "PDT":
        // p#9ea5e9eterminer
        e.style.backgroundColor = "#c1dbd7"
        e.style.color = "rgba(0,0,0,1)";
        break;
      case "IN":
        // preposition / subordinating conjunction 
        e.style.backgroundColor = "#c1dbd7"
        e.style.color = "rgba(0,0,0,1)";
        break;
      case "VBN":
        // past participle verb
        e.style.backgroundColor = "#9ea5e9";
        e.style.color = "#000000";
        break;
      default:
        e.style.color = "#e6e4d6";
        break;

    }

    c.append(e);
    setTimeout(()=>{
    if(innerGrammarDisplayEntities){
      innerGrammarDisplayEntities.append(c);
    }
  },1000);
  }  

  async function updateTooltipText(h){
    var innerTooltipEntities = await document.getElementById("tooltipEntityDisplay");
            
      let t = document.getElementsByClassName("displayed-entity");
      let s = document.querySelector(".createdEntityWrapper");
      if(t && t.length > 0){
        for(let i=0;i<t.length;i++){
          t[i].remove();
        }
      }
      // if(s && s.length < 1){
        var c = document.createDocumentFragment();
        c.className = "createdEntityWrapper";  
      // }    
      let e = document.createElement("div");
      e.className = "displayed-entity";
      e.innerText=h.text;

      c.append(e);
      innerTooltipEntities.append(c);

    }

  const currSelected = ref(null);

  async function updateTooltip(selected) {
    if(selected === currSelected.value){
      return;
    } else {
      const elements = document.getElementsByClassName("displayed-grammar");
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
      let s = document.querySelector(".createdGrammarWrapper");
    }

    currSelected.value = selected;


      if(Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5][selected]){
        // grammarArr.value = [];
        Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5][selected]['sentenceGrammarArray'].forEach((g)=>{
          // console.log("STILL PUSHING GRAMMAR FINE! ", g);
          if(grammarArr.value.indexOf(g['tokenText']) === -1){
            grammarArr.value.push(g['tokenText'],g['sentenceIndex'],g['idx_in_sents'])
          } else {
            return
          }
       
          updateTooltipGrammarText(g);
 
          grammarArr.value.push({'tokenTag':g.tokenTag,'tokenPos':g.tokenPos,'tokenText':g.tokenText})
        });
        
        let existingEntities = document.getElementsByClassName("displayed-entity");
        if(existingEntities && existingEntities.children && existingEntities.children.length){
          for(let j=0;j<existingEntities.children.length;j++){
            existingEntities[j] = null;
          }
        }
        entitiesArr.value = [];
        Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5][selected]['sentenceSpacyEntities'].forEach((h)=>{
          // console.log("STILL PUSHING ENTITIES FINE!", h)
          if(entitiesArr.value.indexOf(h.id) === -1){
            entitiesArr.value.push(h.id)
          } else {
            return
          }
          updateTooltipText(h);
        });

        updateTooltipData();
      } else {
        //console.log("tooltip failure: ", Object.values(JSON.parse(JSON.stringify(props.dataObj)))[5]);
      }
  }

  function updateTooltipData(){
    //console.log("CHECK CHECK! ", tooltipMsg.value);

  }

  function tryToggleComparative(){
    console.log("GRAPHSTATE CHANGED!");
    props.graphstate = props.graphstate + 1;
  }
  
  function emitterClose(command){
    //console.log("emitting ", command);
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
          // console.log("num x changes")
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
      },
      numberYMax:{
        deep: true,
        handler: function(newVal, oldVal){
          // console.log("num x changes")
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
      },
      numberXMin:{
        deep: true,
        handler: function(newVal, oldVal){
          // console.log("num y changes")
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
      },
      numberYMin:{
        deep: true,
        handler: function(newVal, oldVal){
          // console.log("num y changes")
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
        // dataHolder1Parent: [],
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
        // clientX:null,
        // clientY:null
      };
    },
    margin: {
      type: Object,
      default: () => ({
        left: "0px",
        right: "0px",
        top: "0px",
        bottom: "0px",
      }),
    },

    methods: {
      setup(props,{emit}){
      
      },

 
        
      }
    };
  // const dataHolder1Parent = ref([]);

  // TODO: refactor=>this dataholder is a workaround for vue quirks


  </script>




<template >
  <div  id="tooltipEntityDisplay">

  </div>
  <div id="grammarDisplayWrapper" ></div>
  <div id="graphDiv">

    <h1 id="graphTitle">TODO: Add Graph Title Here</h1>

      <!-- AREA CHART WORKS! IT IS OUR MODEL!
      <AreaChart :data="data" :tooltipmsg="tooltipMsg" :mode="mode" @selected="updateTooltip"></AreaChart> -->
      <TestChart 
        :data="data"
        :dataHolder1="dataHolder1Parent"
        :savedLineOneDataObj="savedLineOneDataObj" 
        :selectedXAxisRef="props.selectedXAxisRef"
        :selectedYAxisRef="props.selectedYAxisRef"
        :secondTextRef="props.secondTextRef" 
        :tooltipmsg="tooltipMsg" 
        :selectedRow="props.selectedRow"
        :mode="mode"
        :inGraphsParent="inGraphsParent"
        :yAxisFramingLast="yAxisFramingLast"
        @selected="updateTooltip"
        @dataholderemit1="dataholderemit1"
   
 
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
        @clientX="locateClientX"
        @clientY="locateClientY"
        @resetX="resetX"
        @resetY="resetY"
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
                  <span>
                  <button class="green-btn" @click="updateVizDataSentiment(false,false,false,true); emitterClose('closeUpdatePopup')">Pos</button>
                  <button class="green-btn" @click="updateVizDataSentiment(false,true,false,false); emitterClose('closeUpdatePopup')">Neg</button>
                </span>
                <span>
                  <button class="green-btn" @click="updateVizDataSentiment(true,false,false,false); emitterClose('closeUpdatePopup')">Comp</button>
                  <button class="green-btn" @click="updateVizDataSentiment(false,false,true,false); emitterClose('closeUpdatePopup')">Neu</button>
                </span>
                </span>
                <span id="sentimentTitle">Sentiment Scores</span>
                <br/>
              </span>
            </div>
            <br/>
            
            <!-- <div class="inner-wrap"> -->

              <!-- <span class="buttons-row">
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
              </span> -->

            <!-- </div> -->
          </div>
        </div>
      </div>
  </div>
</template>



<style>
#graphTitle {
  position:absolute;
  text-align:center;
  color:white;
  display:none;
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
  height:72%;
  margin-top:12%;
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

    border-radius: 8px;

    z-index: 99;
    /* margin-left: -96px; */
    text-align: center;
    /* justify-content: right; */
    /* left: 33%; */
    padding: 2%;
    top: -12%;
}

#d3UpdateButtonsWrapper {
  position: fixed;
  justify-content: center;
  width: 100%;
  top: 0%;
  z-index: 100;
  top: 0%;
  left: 0%;
  right: 0%;
  color: #fff;
  padding: 1%;
  /* border-radius: 8px; */
  pointer-events: none;
  /* max-height: 490px; */
  bottom: 0%;
  min-height: 400px;
  height: 100%;
  z-index: 99;
  background: var(--color-background);
  padding-top: 16%;



   
}
#grammarDisplayWrapper {
  align-items: center;
  justify-content: center;

  position: absolute;
  margin-right: 12px;
  max-height:240px;
  border: solid 1px #0097BF;
  border-radius: 8px;
  z-index: 100;
  width: 40%;
  max-width:300px;
  top: 64px;

  flex-direction: row;
  object-fit: contain;
  display: inline-block;
  overflow-y: scroll;
  /* pointer-events: none; */
  color: #000000;
  display:none;
}
#tooltipEntityDisplay {
  z-index: 9999;
  position: absolute;
  background: blue;
  max-width: 100%;
  left: 64px;
  bottom: 80px;
  pointer-events: none;
  top: 80px;
  width: 112px;
  display:none;
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
  font-family: monospace;
  background-color:var(--color-background);
}
#buttonsWrapperTitle {
  border-radius: 8px 8px 0px 0px;
  font-size: 20px;
  padding: 12px;
}
#buttonsWrapperSubtitle {
  padding-right:48px;
  padding-left:48px;
  font-size: 15px;
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
.displayed-entity {
  font-size:16px;
  width:25%;
  min-height: 32px;
}
.displayed-grammar {
  font-size:16px;
  min-height: 24px;
  font-weight:300;
  line-height:1.5;
  display:inline-block;
  pointer-events:none;

  overflow-y: scroll;

}
#sentimentTitle {
  font-size: 24px;
  padding-top: 12px;
}
</style>