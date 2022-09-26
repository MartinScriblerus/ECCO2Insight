<script>
import { onMounted, ref, watch, watchEffect } from "vue";
import * as d3 from 'd3';
// import { ColorPicker } from 'vue-accessible-color-picker';
import {
  select,
  line,
  area,
  cluster,
  arc,
  scaleLinear,
  min,
  max,
  curveBasis,
  axisBottom,
  axisLeft,
} from "d3";
import useResizeObserver from "@/libs/ResizeObserver.js";

export default {
  name: "ResponsiveLineChart",
  props: ["data","newData","mode","tooltipmsg","graphstate", "color0", "color1", "color2", "color3","colorX","colorY","valueX","numberXMax","numberXMin","numberYMax","numberYMin","valueY","numberY", "currentLinesCount","secondTextRef","axisColorMatchBool","selectedXAxisRef","selectedYAxisRef","selectedRow","inGraphsParent","savedLineOneDataObj","dataHolder1"],
  emits:["selected","clientX","clientY", "dataholderemit1","resetX","resetY"],

  data(){
    return {
      clientX: 0,
      clientY: 0,
      closestPoint: null,
      dataH1: [],
      
      // entityArr:[],
      // graphstate: 0,
      // xAxisLabel: '',
      // numberXMax: [],
      // numberYMax: [],
      // numberXMin: [],
      // numberXMin: [],
    };
  },
  setup(props,{emit}) {
    const points = ref();
    const yAxisLabel = ref('');
    const xAxisLabel = ref('');
    const setDH_1 = ref()
    const dataHolder1 = ref([]);
    dataHolder1.value= [];
     // emit("dataholderemit1", dataRef1.value)
    const vueIsGarbageSavedLineOne = ref({})
    const entityArr = ref([])
    const noDupes = ref()
    noDupes.value = false;
    const show = ref(false);
    points.value = [];
    const scaled = ref();
    const graphMode = ref();
    graphMode.value = 0;
    // const DH1_Done = ref(false);
   
    // const dataHolder2 = ref([]);
    // const dataHolder3 = ref([]);
    const passedDataRef1 = ref();
    scaled.value = {
      x: null,
      y: null
    };      
    let regVarData1 = [];
    const tooltipmsg = ref({
      grammarArrays: [],
      sentenceSentimentCompound: 0,
      sentenceSentimentNegative: 0,
      sentenceSentimentNeutral: 0,
      sentenceSentimentPositive: 0,
      entityArrays: [],
    });
   
    // create ref to pass to D3 for DOM manipulation
    const svgRef = ref(null);
    const resetXNeeded = ref(false);
    const resetYNeeded = ref(false);
    
    const lineLabelsArr = ref([]);

    function resetShow(){
      try{
        let t = document.document.querySelector(".createdEntityWrapper");
        if(t){
          t.parentNode.removeChild(t);
        }
      } catch {

      }
      show.value = false;
    }

    function mouseMove(event) {

      const { clientX, clientY } = event;
      show.value = true;

      // console.log("this show: ", show.value);
      // console.log("this client x: ", event.clientX);
      // console.log("this client y: ", event.clientY);
      this.clientX = event.clientX;
      this.clientY = event.clientY;
      emit("clientX",event.clientX);
      emit("clientY",event.clientY);

    }

    let tooltip = document.getElementById("tooltipInner");





    //this.data = newData;
    // this creates another ref to observe resizing, 
    // which we will attach to a DIV,
    // since observing SVGs with the ResizeObserver API doesn't work properly
    const { resizeRef, resizeState } = useResizeObserver();

    onMounted((event) => {
      
      // pass ref with DOM element to D3, when mounted (DOM available)      
      const svg = select(svgRef.value);
      let tempSVGs=[]
      // console.log
      const created_svgs = ref([]);

      const tooltipInner = ref(null)

      const xMaxRef = ref(0);
      const xMinRef = ref(0);
      const yMaxRef = ref(0);
      const yMinRef = ref(0);
      
      const dataRef1 = ref([]);
      const dataRef2 = ref([]);
      // const dataRef3 = ref();
      // const dataRef4 = ref(); 
      const createdLine1 = ref(false);
      const xMaxLabel = ref('');
      const yMaxLabel = ref('');


    //   function updateDataHolder1(newData){
    //   dataHolder1.value = newData;
   
    // }
      
      const storedRef = ref(false);
   


   
     
      function updateOldData(oldData){

    }
      // whenever any dependencies (like data, resizeState) change, call this!
      watchEffect(() => {

        if(JSON.parse(JSON.stringify(props.data)).length < 1){
          return;
        }
        
        const { width, height } = JSON.parse(JSON.stringify(resizeState)).dimensions;
          // console.log("WIDTH: ", width);
          // console.log("HEIGHT: ", height);
          // console.log("D3=> ", d3);

          // CURRENTLY TESTING THIS...
          // if(!JSON.parse(JSON.stringify(props.numberYMax))[JSON.parse(JSON.stringify(props)).currentLinesCount - 1] || !JSON.parse(JSON.stringify(props.numberYMin))[JSON.parse(JSON.stringify(props)).currentLinesCount - 1]){
          //   console.log("RETURNING HERE!!!");
          //   return;
          // }

          yMinRef.value = JSON.parse(JSON.stringify(props.numberYMin))[JSON.parse(JSON.stringify(props)).currentLinesCount - 1];
          yMaxRef.value = JSON.parse(JSON.stringify(props.numberYMax))[JSON.parse(JSON.stringify(props)).currentLinesCount - 1]
          // if(!Math.min.apply(Math,JSON.parse(JSON.stringify(props.data))) || !Math.max.apply(Math,JSON.parse(JSON.stringify(props.data)))){
          //   return;
          // }
          if(JSON.parse(JSON.stringify(Math.min.apply(Math,JSON.parse(JSON.stringify(props.data))))) < yMinRef.value){
            resetYNeeded.value = true;
            // console.log("Y RESET NEEDED");
            yMinRef.value = JSON.parse(JSON.stringify(Math.min.apply(Math,JSON.parse(JSON.stringify(props.data)))));
          } else {
            //yMinRef.value = JSON.parse(JSON.stringify(yMinRef.value))[JSON.parse(JSON.stringify(props)).currentLinesCount - 1];
          }
          // console.log("is this already a proxy? ", JSON.parse(JSON.stringify(yMinRef.value))[JSON.parse(JSON.stringify(props)).currentLinesCount - 1])
          // console.log("check curr lines count: ", JSON.parse(JSON.stringify(props)).currentLinesCount -1)

          if(JSON.parse(JSON.stringify(Math.max.apply(Math,JSON.parse(JSON.stringify(props.data))))) > yMaxRef.value){
            //console.log("RESETTING Y MAX");
            yMaxRef.value = JSON.parse(JSON.stringify(Math.max.apply(Math,JSON.parse(JSON.stringify(props.data)))));

            for(let i = 0; i < props.currentLinesCount; i++){
              let tryGetKeyYMax = document.getElementById(`yRangeDisplayYMax_${i}`);
              let tryGetKeyYMin = document.getElementById(`yRangeDisplayYMin_${i}`);
              if(tryGetKeyYMax){
                tryGetKeyYMax.innerText = yMaxRef.value;
              } else {
                // console.log("CAN'T GET KEY Y MAX!!!!!!!")
              }
              if(tryGetKeyYMin){
                tryGetKeyYMin.innerText = yMinRef.value;
              } else {
                // console.log("CAN'T GET KEY Y MIN!!!!!!!")
              }
            }     
            if(Object.keys(svg).length < 1){
              return;
            } else {
              //console.log("SVG IS: ", svg.select(".y-axis"));
            }
            let yMaxRescale = svg
              .select(".y-axis")['_groups'][0][svg
              // .selectAll(`text`)['_groups'][0][svg
              // .select(".y-axis")
              // .selectAll(`text`)['_groups'][0].length - 1]
              .select(`.y-axis`)['_groups'][0].length - 1]

            if(yMaxRescale ){
              // yMaxLabel.value = yMaxRescale.childNodes[0].data;
              let textDivY = document.getElementById(`newVariable_${JSON.parse(JSON.stringify(props.currentLinesCount))-1}`);
              if(textDivY){
                yMaxLabel.value = textDivY;
              } 
            }
          }
          // if(props.data.length){
          if(!props.selectedXAxisRef || !props.selectedYAxisRef){
            console.log("incoming! ", JSON.parse(JSON.stringify(props.data)).length - 1);
            

            // if(JSON.parse(JSON.stringify(props)).currentLinesCount === 1){
              
              dataRef1.value = JSON.parse(JSON.stringify(props.data));
            // } else {
            //   console.log("looooook: ", JSON.parse(JSON.stringify(dataRef1.value)))
            //   console.log("not reassigning dataRef1 -> curr lines is not 1");
            // }
            if((JSON.parse(JSON.stringify(props.data)).length - 1) > xMaxRef.value){
              xMaxRef.value = JSON.parse(JSON.stringify(props.data)).length - 1;
              //console.log("what is XMAX VAL??? ", xMaxRef.value);
              let xMaxRescale = svg.select(".x-axis")
                .selectAll(`text`)['_groups'][0][svg
                .select(".x-axis")
                .selectAll(`text`)['_groups'][0].length - 1]

                if(xMaxRescale && xMaxRescale.childNodes.length > 0){
                  xMaxLabel.value = xMaxRescale.childNodes[0].data;
                }
              }
              // SETTING XMIN-MAX AND YMIN-MAX
              xMinRef.value = 0;
              yMinRef.value = 0;

              let yMinTemp = JSON.parse(JSON.stringify(props)).numberYMin.filter(i=>i);
              let yMaxTemp = JSON.parse(JSON.stringify(props)).numberYMax.filter(i=>i);
              let xMinTemp = JSON.parse(JSON.stringify(props)).numberXMin.filter(i=>i);
              let xMaxTemp = JSON.parse(JSON.stringify(props)).numberXMax.filter(i=>i);


              //if((Math.min(...yMinTemp) && JSON.parse(JSON.stringify(props.currentLinesCount)) === yMinTemp.length) || yMinTemp && Math.min(...yMinTemp) <= yMinRef.value){
                  //yMinRef.value = Math.min(...yMinTemp) 
                  yMinRef.value = [yMinTemp[yMinTemp.length - 1]]; 
              // }
              if(JSON.parse(JSON.stringify(props)).currentLinesCount === 1 && yMinTemp.length >= 1){
                //console.log("INNER CHECK MATH MIN FOR ERROR: ", yMinTemp[yMinTemp.length -1]);
                yMinRef.value = yMinTemp[yMinTemp.length -1];
              }
              if(JSON.parse(JSON.stringify(props)).currentLinesCount === 2 && yMinTemp.length >= 2){
                yMinRef.value = yMinTemp[yMinTemp.length -1];
              }
              if(xMaxTemp && Math.max(...xMaxTemp) >= xMaxRef.value){
                xMaxRef.value = Math.max(...xMaxTemp)
              }

            } else {
              xMinRef.value = Math.min(JSON.parse(...JSON.stringify(props.numberXMin)));;
                // console.log("last2");
              if(resetXNeeded.value === true || Math.max(...JSON.parse(JSON.stringify(props.numberXMax))) > xMaxRef.value){
                resetXNeeded.value = false;
                // console.log("last marker here... ");
                xMaxRef.value = Math.max(...JSON.parse(JSON.stringify(props.numberXMax)));
                // console.log("last1");
              }
              // xMinRef.value = Math.min(JSON.parse(...JSON.stringify(props.numberXMin)));
              if(resetYNeeded.value === true || Math.max(...JSON.parse(JSON.stringify(props.numberYMax))) > yMaxRef.value){
                resetYNeeded.value = false;
                // console.log("last marker here... 2");
                yMaxRef.value = Math.max(...JSON.parse(JSON.stringify(props.numberYMax)));
                //console.log("YMAX VAL in hot update: ", yMaxRef.value)

              }

              if(resetXNeeded.value === true || xMaxRef.value < JSON.parse(JSON.stringify(props.selectedXAxisRef))['value'][1][0]){
                resetXNeeded.value = false;
                xMaxRef.value = JSON.parse(JSON.stringify(props.selectedXAxisRef))['value'][1][0];
              }

              if(resetXNeeded.value === true || xMinRef.value > JSON.parse(JSON.stringify(props.selectedXAxisRef))['value'][0][0]){
                xMinRef.value = JSON.parse(JSON.stringify(props.selectedXAxisRef))['value'][0][0];
              }
              if(resetYNeeded.value === true || yMaxRef.value < JSON.parse(JSON.stringify(props.selectedYAxisRef))['value'][1][0]){
                resetYNeeded.value = false;
                yMaxRef.value = JSON.parse(JSON.stringify(props.selectedYAxisRef))['value'][1][0];
              }
              if(resetYNeeded.value === true || yMinRef.value > JSON.parse(JSON.stringify(props.selectedYAxisRef))['value'][0][0]){
                yMinRef.value = JSON.parse(JSON.stringify(props.selectedYAxisRef))['value'][0][0];
              }
              //console.log(`xmin: ${xMinRef.value} / xmax: ${xMaxRef.value} / ymin ${yMaxRef.value} / ymax ${yMinRef.value}`)
            }

            // *** ________________________________________________________
            let finalAxes = {
              xMax:xMaxRef.value,
              xMin:xMinRef.value,
              yMax:yMinRef.value,
              yMin:yMinRef.value
            }
          
            if(JSON.parse(JSON.stringify(props)).currentLinesCount < 2){
              yMinRef.value = Math.min(...JSON.parse(JSON.stringify(props)).data);
              yMaxRef.value = Math.max(...JSON.parse(JSON.stringify(props)).data);
            } else if(props.currentLinesCount === 2){

              // console.log("Current Lines Check1", JSON.parse(JSON.stringify(props)).currentLinesCount)
              // console.log("Graphstate Check1", JSON.parse(JSON.stringify(props)).graphstate)
              if(Math.min(...JSON.parse(JSON.stringify(dataHolder1.value))) < finalAxes.yMin){
                yMinRef.value = Math.min(...JSON.parse(JSON.stringify(dataHolder1.value)))
              }
              if(Math.max(...JSON.parse(JSON.stringify(dataHolder1.value))) > finalAxes.yMax){
                yMaxRef.value = Math.max(...JSON.parse(JSON.stringify(dataHolder1.value)));
              }
            
            } else if(JSON.parse(JSON.stringify(props)).currentLinesCount === 3){
              //console.log("Current Lines Check2", JSON.parse(JSON.stringify(props)).currentLinesCount)
              //console.log("Graphstate Check2", JSON.parse(JSON.stringify(props)).graphstate)
              if(Math.min(...JSON.parse(JSON.stringify(dataHolder1.value))) < finalAxes.yMin){
                yMinRef.value = Math.min(...JSON.parse(JSON.stringify(dataHolder1.value)))
              }
              if(Math.max(...JSON.parse(JSON.stringify(dataHolder1.value))) > finalAxes.yMax){
                yMaxRef.value = Math.max(...JSON.parse(JSON.stringify(dataHolder1.value)));
              }
  
            } else if(JSON.parse(JSON.stringify(props)).currentLines === 4){
              if(Math.min(...JSON.parse(JSON.stringify(dataHolder1.value))) < finalAxes.yMin){
                yMinRef.value = Math.min(...JSON.parse(JSON.stringify(dataHolder1.value)))
              }
              if(Math.max(...JSON.parse(JSON.stringify(dataHolder1.value))) > finalAxes.yMax){
                yMaxRef.value = Math.max(...JSON.parse(JSON.stringify(dataHolder1.value)));
              }

            } else {
              // finalAxes.yMax = yMinRef.value;
              // finalAxes.xMax = yMaxRef.value; 
            }  
            console.log()
            // THIS IS A PLACE TO IMPROVE... 
            // scales: map index / data values to pixel values on x-axis / y-axis
            const xScale = scaleLinear()
              .domain([xMinRef.value,xMaxRef.value])
              //.domain([0, props.data.length - 1]) // input values...
              .range([0, width]); // ... output values

            // && min/min refs show the absolute biggest & smallest -- 
            // even if a val is no longer in play!!!!!  
      
            const yScale = scaleLinear()
              .domain([Math.min(...JSON.parse(JSON.stringify(props)).data),Math.max(...JSON.parse(JSON.stringify(props)).data)])
              //.domain([min(props.data), max(props.data)]) // input values...
              .range([height, 0]); // ... output values

            // line generator: D3 method to transform an array of values to data points ("d") for a path element
            const lineGen = area()
              .curve(curveBasis)
              // if axes are inverted from usual, flip these... 
              .x((value, index) => xScale(index))
              .y((value) => yScale(value));
          
            /////////////////////// error catching (TODOs)
            // removed undefined values that throw errors
            Object.values(JSON.parse(JSON.stringify(props)).data).forEach((t,ind)=>{
              if(typeof t=== undefined){
                // console.log("removing t: ", t);
                props.data=JSON.parse(JSON.stringify(props)).data.slice(ind)
              }
            })
            //////////////////////////////////////////////
           
            if(JSON.parse(JSON.stringify(props)).length < 1){
              return;
            } else {
              //console.log("D3 NAMESPACES=> ", d3.namespaces);

    
              if(JSON.parse(JSON.stringify(props)).graphstate === 0){
              
              
                  console.log("props in test: ", JSON.parse(JSON.stringify(props)));
                  dataRef1.value = JSON.parse(JSON.stringify(props)).data;
                  dataHolder1.value = dataRef1.value;

                  if(JSON.parse(JSON.stringify(props)).graphstate === 0 && JSON.parse(JSON.stringify(dataRef1.value)) !== {} && dataRef1.value !== {}){
                    vueIsGarbageSavedLineOne.value = dataRef1.value; 
                  }

                  createLine([dataRef1.value],props.color0,1.5,"line_0");
           
                
 
                
                // if(storedRef.value !== true){
                //     storedRef.value = true;
                   // emit("dataholderemit1", dataRef1.value)
                    // dataHolder1.value = dataRef1.value
                    // createLine([dataRef1.value],props.color0,1.5,"line_0");
                // }
              }
           
              if(JSON.parse(JSON.stringify(props)).graphstate === 1){
                // This will be line #2
          
                // let data2Ready = JSON.parse(JSON.stringify(props)).data;
                // if(data2Ready !== []){
                //   emit("dataholderemit2", data2Ready)
                // }

                // console.log("DATAREEF2: ", JSON.parse(JSON.stringify(dataRef2.value)));
 
                let toDel = svg.selectAll(`.line#line_1`);
                if(toDel.length > 0){
                  for(let i = 0;i<toDel.length - 1;i++){
                    // console.log(toDel[i]);
                    toDel[i].remove();
                  }
                }

                if(JSON.parse(JSON.stringify(props.data)).length > 0){
                  if(Math.max(JSON.parse(JSON.stringify(props.data))) > yMaxRef.value){
                    yMaxRef.value = Math.max(...JSON.parse(JSON.stringify(props.data)))
                  } else {
                    //console.log("hit else for max in line 2 ", JSON.parse(JSON.stringify(dataRef2.value)));
                  }
                  if(Math.min(JSON.parse(JSON.stringify(props.data))) > yMinRef.value ){
                    yMinRef.value = Math.min(...JSON.parse(JSON.stringify(props.data)))
                  } else {
                    // console.log("hit else for min in line 2");
                  }
 

                  // createLine([Object.values(dataHolder1.value)],props.color0,1.5,"line_0");
                  console.log("initial line just prior to creating: ", Object.values(props.data))
                  createNewLine1([Object.values(props.data)],props.color1,1.75,"line_1");
                }
              }
              
              let textDivX = document.getElementById(`newVariable_${JSON.parse(JSON.stringify(props.currentLinesCount))-1}`);
            
              if(textDivX){
                textDivX.innerText = JSON.parse(JSON.stringify(props)).valueX;
                xAxisLabel.value = JSON.parse(JSON.stringify(props)).valueX;
                // console.log("inner text div x ", textDivX.innerText);
                if(lineLabelsArr.value.indexOf(textDivX.innerText) === -1){
                  lineLabelsArr.value.push(textDivX.innerText);
                }
              }
              let textDivY = document.getElementById(`newVariable_${JSON.parse(JSON.stringify(props.currentLinesCount))-1}`);
              //console.log("geetting textdiv y: ", textDivY);
              if(textDivY){
                textDivY.innerText = JSON.parse(JSON.stringify(props)).valueY;
                yAxisLabel.value = JSON.parse(JSON.stringify(props)).valueY;
                //console.log("look here: ", yAxisLabel.value)
                if(lineLabelsArr.value.indexOf(textDivY.innerText) === -1){
                  //console.log("pushing this val into Y: ", textDivY.innerText);
                  lineLabelsArr.value.push(textDivY.innerText);
                }
              }
            }


            // function to render path element with D3's General Update Pattern
            function createLine(dataIn,strokeColor,strokeWidth,chosenClassName){ 
              // emit("dataholderemit1", dataIn);
              try{
                svg.selectAll(`#line_0`).remove();
              } catch(e){
              
              }
              
              let dataInTemp;
              
              if(JSON.parse(JSON.stringify(props)).currentLinesCount< 2){
                dataInTemp = JSON.parse(JSON.stringify(dataIn))[0].filter(i=>typeof i === "number");
                if(dataInTemp.length < 1){
                  return;
                }
                dataIn = dataInTemp;       
                console.log("WHAT IS DATA IN???? ", dataIn);
                if(JSON.parse(JSON.stringify(props)).graphstate === 0){
                  dataHolder1.value = dataIn;
                }
              
                dataIn.filter(i=>typeof i === "number");
                // if(JSON.parse(JSON.stringify(props)).graphstate === 0){
                if(JSON.parse(JSON.stringify(props)).currentLinesCount < 2 && JSON.parse(JSON.stringify(dataIn)).length > 0){
                  dataHolder1.value = JSON.parse(JSON.stringify(dataIn));
                  dataHolder1.value = JSON.parse(JSON.stringify(dataIn));
                }
              } else {

              }
              

              strokeWidth = 1;
              svg
                .selectAll(".line") // get all "existing" lines in svg
                .data([dataIn]) // sync them with our data
                .join("path") // create a new "path" for new pieces of data (if needed)
                // everything after .join() is applied to every "new" and "existing" element
                .attr("id", `line_0`)
                .attr("class", "line") // attach class (important for updating)
                .attr("stroke", strokeColor)
                .attr("stroke-width", strokeWidth)
                .attr("d", lineGen) // shape and form of our line!
                
                .append("defs").append("clipPath")
                  .attr("id", "line_0")
                  .append("rect")
              return svg; 
            }
          

            // // function to render new path element with D3's General Update Pattern
            // // --------------------------------------------------------------------
            function createNewLine1(dataIn1,strokeColor,strokeWidth,chosenClassName){ 
              
              if(JSON.parse(JSON.stringify(props)).currentLinesCount === 1){
                return;
              }
              try{
                svg.selectAll(`#line_1`).remove();
              } catch(e){
                console.log("err in createline: ",e)
              }
             
              if(!dataRef2.value){
                dataRef2.value = JSON.parse(JSON.stringify(dataIn1))[0];
              }
              let dataInTemp = JSON.parse(JSON.stringify(dataIn1))[0].filter(i=>typeof i === "number");
              
              //console.log("WHAT IS TEMP &******** ", JSON.parse(JSON.stringify(props.dataHolder1Parent)));
              dataIn1 = dataInTemp;   
              //recreate original line
              svg.selectAll(`#line_0`).remove();
                let savedVals = Object.values(JSON.parse(JSON.stringify(props.dataHolder1)))
                savedVals.map(i=>typeof i === "number");

              createLine(savedVals,props.color0,1.5,"line_0");
              
              // createLine([dataHolder1.value],props.color0,1.5,"line_0");
              dataIn1.filter(i=>typeof i === "number");
              //console.log("DATA IN in create new line 1: ", dataIn1);
              strokeWidth = 1;
              svg
                  .selectAll(`#line_1`)
                  .data([dataIn1]) // sync them with our data
                  .join(`path`) // create a new "path" for new pieces of data (if needed)
                  .attr("stroke", strokeColor)
                  .attr("id", "line_1")
                  .attr("stroke-width", strokeWidth)
                  .attr("d", lineGen); // shape and form of our line!   
                  
              const xAxis = axisBottom(xScale);
                      
              return svg; 
            }
  

            // create axes
            // -----------------------------------------------------------------------
            function createXAxis(color){
              // render axes with help of scales
              // (we let Vue render our axis-containers and let D3 populate the elements inside it)
              const xAxis = axisBottom(xScale);
        
              let oldXLabel = svg
                .select(".x-axis")
                .selectAll(`text`)['_groups'][0][svg
                .select(".x-axis")
                .selectAll(`text`)['_groups'][0].length -1]
              if(oldXLabel){
                oldXLabel.remove();
              }

              svg
                .select(".x-axis")
              
                .style("transform", `translateY(${height}px)`) // position on the bottom
                .style("color", color)
                // Add X axis label:
                .call(xAxis)
                    .call(g => g.append("text")
                    .attr("x", JSON.parse(JSON.stringify(resizeState)).dimensions.width)
                    .attr("y", 30)
                    .attr("fill", "currentColor")
                    .attr("text-anchor", "end")
                    .text(JSON.parse(JSON.stringify(props)).valueX));
         
              if(JSON.parse(JSON.stringify(props)).graphstate < 1 && oldXLabel !== xMaxLabel.value){

                let tryGetKeyAxisXMax = document.getElementById("xAxisRangeDisplayMax");
                let tryGetKeyAxisXMin = document.getElementById("xAxisRangeDisplayMin");
                let tryGetKeyAxisYMax = document.getElementById("yAxisRangeDisplayMax");
                let tryGetKeyAxisYMin = document.getElementById("yAxisRangeDisplayMin");

                let tryGetKeyXMax = document.getElementById("xRangeDisplayXMax_0");
                let tryGetKeyXMin = document.getElementById("xRangeDisplayXMin_0");
                let tryGetKeyYMax = document.getElementById("xRangeDisplayYMax_0");
                let tryGetKeyYMin = document.getElementById("xRangeDisplayYMin_0");
              

                resetXNeeded.value = true;
              }
              return svg;
            }

            if(props.axisColorMatchBool){
              createYAxis(JSON.parse(JSON.stringify(props)).colorY)
            } else {
              createYAxis(JSON.parse(JSON.stringify(props)).colorX)
            }
              createXAxis(JSON.parse(JSON.stringify(props)).colorX);

            function createYAxis(color){
              //console.log("WE ARE CHANGING Y AXIS NOW!!! ");
           
              const yAxis = axisLeft(yScale);
              let oldYLabel = svg
                .select(".y-axis")
                .selectAll(`text`)['_groups'][0][svg
                .select(".y-axis")
                .selectAll(`text`)['_groups'][0].length -1]
              if(oldYLabel){
                oldYLabel.remove();
              }
              //console.log("are we getting color? ", color);
                svg.select(".y-axis")
                    .style("color", color)
                    .call(yAxis)
                    // add y axis label
                    .call(g => g.append("text")
                    .attr("y", -12)
                    .attr("x", -40)
                    .attr("fill", "currentColor")
                    .attr("text-anchor", "start")
          
                    .text(JSON.parse(JSON.stringify(props)).valueY));

              if(JSON.parse(JSON.stringify(props)).graphstate < 1){
               // console.log("RESETTING Y ", JSON.parse(JSON.stringify(props)).numberYMax);

                yMaxRef.value = JSON.parse(JSON.stringify(props)).numberYMax;
                yMinRef.value = JSON.parse(JSON.stringify(props)).numberYMin;
               // console.log("Y MIN VAL IS NOW... ", yMinRef.value);
                // console.log("Y MAX VAL IS NOW... ", yMaxRef.value);

                emit("resetY")
                resetYNeeded.value = true;
              }
              //console.log("*** SVG y axis *** ", svg);
              return svg
            }

            svg.on('mouseover', function(d) {
              let selectedIndexX = Math.floor((d.offsetX/width) * JSON.parse(JSON.stringify(props)).data.length);
            
              if(!selectedIndexX ){
                return;
              } else {
                if(!selectedIndexX){
                  return;
                }
                //console.log("what is D? ", d);
                //console.log("what is selected X? ", selectedIndexX);
                this.selectedIndexX = selectedIndexX;
            
                if(selectedIndexX > 0){
                  //console.log("emitting the selected x index ", selectedIndexX)
                  emit('selected', selectedIndexX);
                }
              }
            })
            points.value = [];
            for(let i = 0; i < JSON.parse(JSON.stringify(props)).data.length - 1; i++){
            
              points.value.push({
                x: i,
                y: props.data[i],
                max: height
              })
            }
            // console.log("!!##POINTS: ", JSON.parse(JSON.stringify(points.value)));
          });
        });
        //console.log("RESIZEREF ", resizeRef);

    // return refs to make them available in template
    return { svgRef, resizeRef, mouseMove,tooltipmsg, show,resetShow};
  },
  methods: {
    tryAppendTopics(newVal){
      let topicListWrapper = document.getElementById("topicListWrapper");
      let tooltipInner = document.getElementById("tooltipInner")
      if(topicListWrapper && tooltipInner){
        JSON.parse(JSON.stringify(JSON.parse(JSON.stringify(newVal)).entityArrays)).forEach((entArr)=>{
          try{
            if(entityArr.indexOf(entArr[0]) === -1){
              entityArr.push(entArr[0]);
            }
          } catch {
            // console.log("ERROR!!!! ------------ ",entArr)
          }

        })
      }
    }
  },

  watch: { 
    dataRef1:{
        // deep: true,
        handler: function(newVal, oldVal){
            
        }
    },
    dataHolder1:{
        deep: true,
        handler: function(newVal, oldVal){
          if(newVal !== oldVal){
            console.log("OLD VAL!!! ", oldVal);
          }
          console.log(newVal)
        }
    },
    xMaxRef:{
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    xMaxRef:{
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    yMaxRef:{
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    xMinRef:{
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    yMinRef:{
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    xMaxLabel:{
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    yMaxLabel:{
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    selectedRow:{
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    currentLinesCount:{
        deep: true,
        handler: function(newVal, oldVal){
          //console.log("GREAT CHECK!! ",newVal)
          if(dataRef1.value && dataHolder1.value.length && passedDataRef1.value === false){
            
            // dataHolder1.value.push(dataRef1.value);
            passedDataRef1.value = true;
          }
          if(newVal === 1){
            if(oldVal.length && oldVal.length > 0){
              // dataHolder1.value = oldVal;
            }
          }
        }
    }, 
    resetXNeeded:{
      handler: function(newVal, oldVal){
        //console.log("RESET NEEDED ", newVal);

      }
    },
    resetYNeeded:{
      handler: function(newVal, oldVal){
        //console.log("RESET NEEDED ", newVal);

      }
    },
    axisColorMatchBool:{
        deep: true,
        handler: function(newVal, oldVal){

        }
    },     
    color0:{
        deep: true,
        handler: function(newVal, oldVal){
          
        }
    },
    color1: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    color2: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    color3: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    colorX: {
        deep: true,
        handler: function(newVal, oldVal){
          // console.log(newVal);
          //console.log("here's keybuilder div");
              let keyBuilder = document.getElementById("d3UpdateButtonsWrapper");
              
              if(keyBuilder){
                //console.log("NEW COLOR>>X AXIS? ", newVal);
                keyBuilder.style.borderColor = newVal.value;
              }
        }
    },
    colorY: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    valueX: {
        deep: true,
        handler: function(newVal, oldVal){
          
        }
    },
    valueY: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    numberXMin: {
        deep: true,
        handler: function(newVal, oldVal){
          // console.log("in new xmin!")
        }
    },
    numberXMax: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    numberYMin: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    numberYMax: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    selectedXAxisRef: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    selectedYAxisRef: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    yAxisFramingLast: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    show: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    graphstate: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    dataHolder1: {
        deep: true,
        handler: function(newVal, oldVal){

        }
    },
    tooltipmsg: {
      deep: true,
      handler: async function(newVal, oldVal){

        
////////////////
//**************

function updateTooltip(newVal){
  show.value = true;
  let tooltip = document.getElementById("tooltipInner");
    if(tooltip){
                    tooltip.innerHTML = `
                    <div id="sentimentDisplay">
                      <h4 class="HUD-Test-half-div">Comp: ${JSON.parse(JSON.stringify(newVal)).sentimentCompound}</h4>
                      <h4 class="HUD-Test-half-div">Neg: ${JSON.parse(JSON.stringify(newVal)).sentimentNegative}</h4>
                      <h4 class="HUD-Test-half-div">Neu: ${JSON.parse(JSON.stringify(newVal)).sentimentNeutral}</h4>
                      <h4 class="HUD-Test-half-div">Pos: ${JSON.parse(JSON.stringify(newVal)).sentimentPositive}</h4>
                    </div>
                
                    <div id="topicListWrapper">
                      ${entityArr.value.toString()}
                    </div> 
                    `
                  }
                  let topicWrapper = document.getElementById("topicListWrapper");
                
                  if(newVal){
                    JSON.parse(JSON.stringify(JSON.parse(JSON.stringify(newVal)).entityArrays)).forEach(i=>topicWrapper.append(`${i[0]}\n`))
                  }
            }
        updateTooltip(newVal)
//**************
////////////////

      }
    }
  }
};
</script>

<template>
  <div id="barChartWrapper" ref="resizeRef">
    <!-- :style="{ top: `${clientY}px`, left: `${clientX}px` }" -->
    <!-- v-if="show" -->
    <div id="tooltip"
          :style="{ top: `${0}px`, left: `${0}px`, width: `${60}vw`,position:`absolute` }"
      
          @mouseout="resetShow"
      >
        <div id="tooltipInner" ref="tooltipInner">

        </div>
    </div>
    <!-- <span v-if="this.xAxisLabel" id="yAxisLabel">{{this.xAxisLabel}}</span> -->
    <svg @mouseover="mouseMove" id="svgId" ref="svgRef">
      <g class="x-axis" />
      <g class="y-axis" />
    </svg>
  </div>
</template>

<style>
#barChartWrapper {
  display: flex;
  height: 100%;
  z-index: 10;
  margin-left: 48px;
  margin-right: 48px;
  top: 8%;
}
#svgId {
    background: rgba(0,0,0,0.98);
 
}
#tooltip {
  padding: 5px;
  position: absolute;
  background-color: transparent;
  color:#ffffff;
  font-size: 16px;
  font-weight: 400;
  z-index:9999;
  margin-left: 36px;
  pointer-events:none;
}
#tooltipInner {
  width: 100%;
  height: 80px;
}
.HUD-Test-half-div {
  width:100%;
  min-width:50%;
  overflow:hidden;
  text-align:left;
  padding-left: 2%;
}
#sentimentDisplay {
  display:grid;
  flex-direction: row;
  overflow:hidden;
  width:100%;
  grid-template-columns: 1fr 1fr 1fr 1fr;
}
#topicListWrapper {
  text-align:left;
}

</style>