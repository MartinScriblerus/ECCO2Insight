<script>
import { onMounted, ref, watchEffect } from "vue";
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
  props: ["data","newData","mode","tooltipmsg","graphstate", "color0", "color1", "color2", "color3","colorX","colorY","valueX","numberXMax","numberXMin","numberYMax","numberYMin","valueY","numberY", "currentLinesCount","secondTextRef","axisColorMatchBool","selectedXAxisRef","selectedYAxisRef","selectedRow","axesFramingLast","dataHolder1Parent"],
  emits:["selected","clientX","clientY", "dataholderemit1"],

  data(){
    return {
      clientX: 0,
      clientY: 0,
      closestPoint: null,
      dataH1: ['']
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


  
    const entityArr = ref([])
    console.log("PROPS CHECK KILL ME ", props);
    const show = ref(false);
    points.value = [];
    const scaled = ref();
    const graphMode = ref();
    graphMode.value = 0;
    const DH1_Done = ref(false);
    const dataHolder1 = ref([]);
    dataHolder1.value = [];
    // const dataHolder2 = ref([]);
    // const dataHolder3 = ref([]);
    
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

      console.log("this show: ", show.value);
      console.log("this client x: ", event.clientX);
      console.log("this client y: ", event.clientY);
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
      console.log("fuck shit testchart 21");
      let tempSVGs=[]
      console.log
      const created_svgs = ref([]);

      const tooltipInner = ref(null)

      const xMax = ref(0);
      const xMin = ref(0);
      const yMax = ref(0);
      const yMin = ref(0);
      
      const dataRef1 = ref();
      const dataRef2 = ref();
      const dataRef3 = ref();
      const dataRef4 = ref(); 
      const createdLine1 = ref(false);
      const xMaxLabel = ref('');
      const yMaxLabel = ref('');


      function updateDataHolder1(newData){
      dataHolder1.value = newData;
   
      console.log("so done w this: ", dataHolder1.value )
    }

      
      // whenever any dependencies (like data, resizeState) change, call this!
      watchEffect(() => {
        // console.log("Props ZData in testvhart? ", JSON.parse(JSON.stringify(props.data)));
        // console.log("THIS FUCKING SUCKS: ", JSON.parse(JSON.stringify(props)).dataHolder1Parent);
        // console.log("DATA HOLDER 1 VAL: ", dataHolder1.value)
        // if(!JSON.parse(JSON.stringify(dataHolder1.value))){
        //   dataHolder1.value=JSON.parse(JSON.stringify(props.data))
        // }
        if(JSON.parse(JSON.stringify(props.data)).length < 1){
          console.log("fuck shit testchart 22");
          return;
        }

        const { width, height } = JSON.parse(JSON.stringify(resizeState)).dimensions;
          console.log("WIDTH: ", width);
          console.log("HEIGHT: ", height);
          console.log("D3=> ", d3);
        
          // CURRENTLY TESTING THIS...
          //if(Math.min.apply(Math,JSON.parse(JSON.stringify(props.data))) < yMin.value){
          yMin.value = Math.min.apply(Math,JSON.parse(JSON.stringify(props.data)));
          // }
          if(Math.max.apply(Math,JSON.parse(JSON.stringify(props.data))) > yMax.value){
            yMax.value = Math.max.apply(Math,JSON.parse(JSON.stringify(props.data)));

            for(let i = 0; i < props.currentLinesCount; i++){
              let tryGetKeyYMax = document.getElementById(`yRangeDisplayYMax_${i}`);
              let tryGetKeyYMin = document.getElementById(`yRangeDisplayYMin_${i}`);
              if(tryGetKeyYMax){
                tryGetKeyYMax.innerText = yMax.value;
              } else {
                console.log("CAN'T GET KEY Y MAX!!!!!!!")
              }
              if(tryGetKeyYMin){
                tryGetKeyYMin.innerText = yMin.value;
              } else {
                console.log("CAN'T GET KEY Y MIN!!!!!!!")
              }
            }      
            if(Object.keys(svg).length < 1){
              return;
            } else {
              console.log("SVG IS: ", svg.select(".y-axis"));
            }
            let yMaxRescale = svg
              .select(".y-axis")['_groups'][0][svg
              // .selectAll(`text`)['_groups'][0][svg
              // .select(".y-axis")
              // .selectAll(`text`)['_groups'][0].length - 1]
              .select(`.y-axis`)['_groups'][0].length - 1]

            if(yMaxRescale ){
              // yMaxLabel.value = yMaxRescale.childNodes[0].data;
              let textDivY = document.getElementById(`newVariable_${JSON.parse(JSON.stringify(props.currentLinesCount))-1}_yvar`);
              if(textDivY){
                yMaxLabel.value = textDivY;
              } 
            }
          }

          if(!props.selectedXAxisRef || !props.selectedYAxisRef){
            console.log("incoming! ", JSON.parse(JSON.stringify(props.data)).length - 1);
            if((JSON.parse(JSON.stringify(props.data)).length - 1) > xMax.value){
              xMax.value = JSON.parse(JSON.stringify(props.data)).length - 1;
              console.log("what is XMAX VAL??? ", xMax.value);
              let xMaxRescale = svg.select(".x-axis")
                .selectAll(`text`)['_groups'][0][svg
                .select(".x-axis")
                .selectAll(`text`)['_groups'][0].length - 1]

              if(xMaxRescale && xMaxRescale.childNodes.length > 0){
                xMaxLabel.value = xMaxRescale.childNodes[0].data;
              }
            }
            // SETTING XMIN-MAX AND YMIN-MAX
            xMin.value = 0;
            yMin.value = 0;
            // yMax.value = max(props.data);
            console.log("CHECK PROPS: ", JSON.parse(JSON.stringify(props)))

            let yMinTemp = JSON.parse(JSON.stringify(props)).numberYMin.filter(i=>i);
            let yMaxTemp = JSON.parse(JSON.stringify(props)).numberYMax.filter(i=>i);
            let xMinTemp = JSON.parse(JSON.stringify(props)).numberXMin.filter(i=>i);
            let xMaxTemp = JSON.parse(JSON.stringify(props)).numberXMax.filter(i=>i);

            //if((Math.min(...yMinTemp) && JSON.parse(JSON.stringify(props.currentLinesCount)) === yMinTemp.length) || yMinTemp && Math.min(...yMinTemp) <= yMin.value){
                //yMin.value = Math.min(...yMinTemp) 
                yMin.value = [yMinTemp[yMinTemp.length - 1]]; 
            // }
            if(JSON.parse(JSON.stringify(props)).currentLinesCount === 1 && yMinTemp.length >= 1){
              console.log("INNER CHECK MATH MIN FOR ERROR: ", Math.min(...xMinTemp));
              yMin.value = yMinTemp[yMinTemp.length -1];
            }
            if(JSON.parse(JSON.stringify(props)).currentLinesCount === 2 && yMinTemp.length >= 2){
              console.log("INNER CHECK MATH MAX FOR ERROR: ", Math.max(...yMaxTemp));
              // yMax.value = Math.max(...yMaxTemp)
              yMin.value = yMinTemp[yMinTemp.length -1];
            }
            // if(xMinTemp && Math.min(...xMinTemp) <= xMin.value){
            //   console.log("INNER CHECK MATH MIN FOR ERROR: ", Math.min(...xMinTemp));
            //   xMin.value = Math.min(...xMinTemp)
            // }
            if(xMaxTemp && Math.max(...xMaxTemp) >= xMax.value){
              console.log("INNER CHECK MATH MAX X FOR ERROR: ", Math.max(...xMaxTemp));
              xMax.value = Math.max(...xMaxTemp)
            }

          } else {
            xMin.value = Math.min(JSON.parse(...JSON.stringify(props.numberXMin)));;
              // console.log("last2");
            if(resetXNeeded.value === true || Math.max(...JSON.parse(JSON.stringify(props.numberXMax))) > xMax.value){
              resetXNeeded.value = false;
              // console.log("last marker here... ");
              xMax.value = Math.max(...JSON.parse(JSON.stringify(props.numberXMax)));
              // console.log("last1");
            }
            // xMin.value = Math.min(JSON.parse(...JSON.stringify(props.numberXMin)));
            if(resetYNeeded.value === true || Math.max(...JSON.parse(JSON.stringify(props.numberYMax))) > yMax.value){
              resetYNeeded.value = false;
              // console.log("last marker here... 2");
              yMax.value = Math.max(...JSON.parse(JSON.stringify(props.numberYMax)));
              // console.log("YMAX VAL in hot update: ", yMax.value)
              //xMin.value = Math.min.apply(...JSON.parse(JSON.stringify(props.numberXMin)));
            }
            // xMin.value = Math.min(JSON.parse(...JSON.stringify(props.numberXMin)));
            // console.log("last markerrr... ");
            //   console.log("GET VALUE BEFORE ARRAYS ", JSON.parse(JSON.stringify(props.selectedXAxisRef))['value']);

              if(resetXNeeded.value === true || xMax.value < JSON.parse(JSON.stringify(props.selectedXAxisRef))['value'][1][0]){
                resetXNeeded.value = false;
                xMax.value = JSON.parse(JSON.stringify(props.selectedXAxisRef))['value'][1][0];
              }

              if(resetXNeeded.value === true || xMin.value > JSON.parse(JSON.stringify(props.selectedXAxisRef))['value'][0][0]){
                xMin.value = JSON.parse(JSON.stringify(props.selectedXAxisRef))['value'][0][0];
              }
              if(resetYNeeded.value === true || yMax.value < JSON.parse(JSON.stringify(props.selectedYAxisRef))['value'][1][0]){
                resetYNeeded.value = false;
                yMax.value = JSON.parse(JSON.stringify(props.selectedYAxisRef))['value'][1][0];
              }
              if(resetYNeeded.value === true || yMin.value > JSON.parse(JSON.stringify(props.selectedYAxisRef))['value'][0][0]){
                yMin.value = JSON.parse(JSON.stringify(props.selectedYAxisRef))['value'][0][0];
              }
              console.log(`xmin: ${xMin.value} / xmax: ${xMax.value} / ymin ${yMax.value} / ymax ${yMin.value}`)
            }

            // *** ________________________________________________________
            let finalAxes = {
              xMax:xMax.value,
              xMin:xMin.value,
              yMax:yMin.value,
              yMin:yMin.value
            }
            console.log("WTF ARE CURRENT LINES? ", JSON.parse(JSON.stringify(props)).currentLinesCount);

            if(JSON.parse(JSON.stringify(props)).currentLinesCount < 2){
              xMin.value = Math.min(...JSON.parse(JSON.stringify(props)).data);
              yMax.value = Math.max(...JSON.parse(JSON.stringify(props)).data);

              // dataHolder1.value = JSON.parse(JSON.stringify(props)).data;
              // if(dataHolder1.value.length < 1){
              //   dataHolder1.value.push(props.data);
              // }

              console.log("DATAHOLDERE 1 is.... ", JSON.parse(JSON.stringify(dataHolder1.value)));
              console.log("Current Lines Check0", JSON.parse(JSON.stringify(props)).currentLinesCount)
              console.log("Graphstate Check0", JSON.parse(JSON.stringify(props)).graphstate)
              //dataHolder1.value = JSON.parse(JSON.stringify(props.data));
            } else if(props.currentLinesCount === 2){
              console.log("WILL THIS BE ANY USE: ", dataHolder1.value);
              // try{
              //   console.log("DATAH1: ", dataH1);
              // } catch (e){console.log("err")}
              console.log("Current Lines Check1", JSON.parse(JSON.stringify(props)).currentLinesCount)
              console.log("Graphstate Check1", JSON.parse(JSON.stringify(props)).graphstate)
              if(Math.min(...JSON.parse(JSON.stringify(dataHolder1.value))) < finalAxes.yMin){
                yMin.value = Math.min(...JSON.parse(JSON.stringify(dataHolder1.value)))
              }
              if(Math.max(...JSON.parse(JSON.stringify(dataHolder1.value))) > finalAxes.yMax){
                yMax.value = Math.max(...JSON.parse(JSON.stringify(dataHolder1.value)));
              }
            
            } else if(JSON.parse(JSON.stringify(props)).currentLinesCount === 3){
              console.log("Current Lines Check2", JSON.parse(JSON.stringify(props)).currentLinesCount)
              console.log("Graphstate Check2", JSON.parse(JSON.stringify(props)).graphstate)
              if(Math.min(...JSON.parse(JSON.stringify(dataHolder1.value))) < finalAxes.yMin){
                yMin.value = Math.min(...JSON.parse(JSON.stringify(dataHolder1.value)))
              }
              if(Math.max(...JSON.parse(JSON.stringify(dataHolder1.value))) > finalAxes.yMax){
                yMax.value = Math.max(...JSON.parse(JSON.stringify(dataHolder1.value)));
              }
              // if(Math.min(...JSON.parse(JSON.stringify(dataHolder2.value))) < finalAxes.yMin){
              //   yMin.value = Math.min(...JSON.parse(JSON.stringify(dataHolder2.value)))
              // }
              // if(Math.max(...JSON.parse(JSON.stringify(dataHolder2.value))) > finalAxes.yMax){
              //   yMax.value = Math.max(...JSON.parse(JSON.stringify(dataHolder2.value)));
              // }
            } else if(JSON.parse(JSON.stringify(props)).currentLines === 4){
              if(Math.min(...JSON.parse(JSON.stringify(dataHolder1.value))) < finalAxes.yMin){
                yMin.value = Math.min(...JSON.parse(JSON.stringify(dataHolder1.value)))
              }
              if(Math.max(...JSON.parse(JSON.stringify(dataHolder1.value))) > finalAxes.yMax){
                yMax.value = Math.max(...JSON.parse(JSON.stringify(dataHolder1.value)));
              }
              // if(Math.min(...JSON.parse(JSON.stringify(dataHolder2.value))) < finalAxes.yMin){
              //   yMin.value = Math.min(...JSON.parse(JSON.stringify(dataHolder2.value)))
              // }
              // if(Math.max(...JSON.parse(JSON.stringify(dataHolder2.value))) > finalAxes.yMax){
              //   yMax.value = Math.max(...JSON.parse(JSON.stringify(dataHolder2.value)));
              // }
              // if(Math.min(...JSON.parse(JSON.stringify(dataHolder3.value))) < finalAxes.yMin){
              //   yMin.value = Math.min(...JSON.parse(JSON.stringify(dataHolder3.value)))
              // }
              // if(Math.max(...JSON.parse(JSON.stringify(dataHolder3.value))) > finalAxes.yMax){
              //   yMax.value = Math.max(...JSON.parse(JSON.stringify(dataHolder3.value)));
              // }
            } else {
              // finalAxes.yMax = yMin.value;
              // finalAxes.xMax = yMax.value; 
            }  

            // THIS IS A PLACE TO IMPROVE... 
            // scales: map index / data values to pixel values on x-axis / y-axis
            const xScale = scaleLinear()
              .domain([xMin.value,xMax.value])
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
                console.log("removing t: ", t);
                props.data=JSON.parse(JSON.stringify(props)).data.slice(ind)
              }
            })
            //////////////////////////////////////////////
           
            if(props.length < 1){
              return;
            } else {
              console.log("D3 NAMESPACES=> ", d3.namespaces);
              console.log("WTF IS GRAPHSTATE ", JSON.parse(JSON.stringify(props)).graphstate);
              
              
              if(JSON.parse(JSON.stringify(props)).graphstate === 0){
                if(!dataRef1.value && JSON.parse(JSON.stringify(props)).data.length > 0){
                  dataRef1.value = props.data; 
           
                  let data1Ready = JSON.parse(JSON.stringify(props)).data;
                  if(data1Ready !== []){
                    emit("dataholderemit1", data1Ready)
                  }

                }
                let vals = Object.values(JSON.parse(JSON.stringify(dataRef1.value)));
                for(let v = 0;v<vals.length-1;v++){
                
                  if(typeof Object.values(JSON.parse(JSON.stringify(dataRef1.value)))[v] === "number"){

                  } else {
                    console.log("what type is this? ", typeof Object.values(JSON.parse(JSON.stringify(dataRef1.value)))[v]);
                  }
                }
                //console.log("JUST CHERCKING: ", JSON.parse(JSON.stringify(dataRef1.value)));
                console.log("WHAT IS DATAREF1 VALUE? ", dataRef1.value);
                // dataHolder1.value = dataRef1.value;
                
                console.log("dataholder1: ", dataHolder1.value )
                if(DH1_Done.value !== true && JSON.parse(JSON.stringify(dataRef1.value)).length){

                  DH1_Done.value = true;
                  //dataH1.push(dataRef1.value);
     
                  console.log("dataholder I am going insane: ", dataHolder1.value);
                }
                createLine([dataRef1.value],props.color0,1.5,"line_0");
                
              }
           
              if(JSON.parse(JSON.stringify(props)).graphstate === 1){
                // This will be line #2

                dataRef2.value = props.data; 

                // let data2Ready = JSON.parse(JSON.stringify(props)).data;
                // if(data2Ready !== []){
                //   emit("dataholderemit2", data2Ready)
                // }

                // console.log("DATAREEF2: ", JSON.parse(JSON.stringify(dataRef2.value)));
                // console.log("WHAT IS DATAREF2? WHAT IS DATAHOLDER?? // PICK UP EDITS HERE!")
                let toDel = svg.selectAll(`.line#line_1`);
                if(toDel.length > 0){
                  for(let i = 0;i<toDel.length - 1;i++){
                    console.log(toDel[i]);
                    toDel[i].remove();
                  }
                }
                if(JSON.parse(JSON.stringify(dataRef2.value)).length > 0){
                  if(Math.max(JSON.parse(JSON.stringify(dataRef2.value))) > yMax.value){
                    yMax.value = Math.max(...JSON.parse(JSON.stringify(dataRef2.value)))
                  } else {
                    console.log("hit else for max in line 2 ", JSON.parse(JSON.stringify(dataRef2.value)));
                  }
                  if(Math.min(JSON.parse(JSON.stringify(dataRef2.value))) > yMin.value ){
                    yMin.value = Math.min(...JSON.parse(JSON.stringify(dataRef2.value)))
                  } else {
                    console.log("hit else for min in line 2");
                  }
                  // console.log("WHAT THE FUCK: ", JSON.parse(JSON.stringify(props)).dataHolder1Parent);

                  
                  createNewLine1([Object.values(dataRef2.value)],props.color1,1.75,"line_1");
                }
              }

              // SAVE GROUPS 3 AND 4 UNTIL POST-MVP
              // if(JSON.parse(JSON.stringify(props)).graphstate === 2){
              //   // this will be for line #3
              //   dataRef3.value = props.data; 

              //   let data3Ready = JSON.parse(JSON.stringify(props)).data;
              //   if(data3Ready !== []){
              //     emit("dataholderemit3", data3Ready)
              //   }

              //   let toDel = svg.selectAll(".line#line_2")
              //   if(toDel.length > 0){
              //     for(let i = 0;i<toDel.length - 1;i++){
              //       toDel[i].remove();
              //     }
              //   }
              //   if(JSON.parse(JSON.stringify(dataRef3.value)).length > 0){
              //     if(Math.max(JSON.parse(JSON.stringify(dataRef3.value)))> yMax.value){
              //       yMax.value = Math.max(...JSON.parse(JSON.stringify(dataRef3.value)))
              //     }
              //     createNewLine2([Object.values(dataRef3.value)],props.color2,2,"line_2");
              //   }
              // }
              // if(JSON.parse(JSON.stringify(props)).graphstate === 3){
              //   dataRef4.value = JSON.parse(JSON.stringify(props.data));
              //   let toDel = svg.selectAll(".line#line_3")
              //   if(toDel.length > 0){
              //     for(let i = 0;i<toDel.length - 1;i++){
              //       toDel[i].remove();
              //     }
              //   }
              //   if(dataRef4.value.length > 0){
              //     if(Math.max(JSON.parse(JSON.stringify(dataRef4.value)))> yMax.value){
              //       yMax.value = Math.max(...JSON.parse(JSON.stringify(dataRef4.value)))
              //     }
              //     createNewLine3([JSON.parse(JSON.stringify(dataRef4.value))],props.color3,2.25,"line_3");
              //   }
              // }
              
              let textDivX = document.getElementById(`newVariable_${JSON.parse(JSON.stringify(props.currentLinesCount))-1}_xvar`);
            
              if(textDivX){
                textDivX.innerText = JSON.parse(JSON.stringify(props)).valueX;
                xAxisLabel.value = JSON.parse(JSON.stringify(props)).valueX;
                console.log("inner text div x ", textDivX.innerText);
                if(lineLabelsArr.value.indexOf(textDivX.innerText) === -1){
                  lineLabelsArr.value.push(textDivX.innerText);
                }
              }
              let textDivY = document.getElementById(`newVariable_${JSON.parse(JSON.stringify(props.currentLinesCount))-1}_yvar`);
          
              if(textDivY){
                textDivY.innerText = JSON.parse(JSON.stringify(props)).valueY;
                yAxisLabel.value = JSON.parse(JSON.stringify(props)).valueY;
                console.log("text div Y: ", textDivY);
                if(lineLabelsArr.value.indexOf(textDivY.innerText) === -1){
                  lineLabelsArr.value.push(textDivY.innerText);
                }
              }
            }

        
            // function to render path element with D3's General Update Pattern
            function createLine(dataIn,strokeColor,strokeWidth,chosenClassName){ 
              try{
                svg.selectAll(`#line_0`).remove();
              } catch(e){
                console.log("err in createline: ",e)
              }
              // dataIn = dataIn.filter(i=>i)
              console.log("WHAT IS DATA IN???? ", dataIn);

              let dataInTemp = JSON.parse(JSON.stringify(dataIn))[0].filter(i=>typeof i === "number");
              if(dataInTemp.length < 1){
                return;
              }
              // let dataInTypeCheck = dataIn.filter(i => typeof i === "number").length;
              console.log("WHAT IS DATA IN FOR FUCK's SAKE: ", dataInTemp);
              dataIn = dataInTemp;       
              
              dataIn.filter(i=>typeof i === "number");
              console.log("JESUS CHRIST: ", dataHolder1.value);
              // if(dataHolder1.value.length > 1 && dataIn !== []){
              //   console.log("do we hit this???");
              //   dataHolder1.value.push(dataIn)
              // }
              // console.log("DATA IN in in create line: ", dataIn)
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
              document.getElementById("modalFull").classList.remove("receivedSingleTextData");
              try{
                svg.selectAll(`#line_1`).remove();
              } catch(e){
                console.log("err in createline: ",e)
              }
              dataIn1.filter(i=>i)
              let dataInTemp = JSON.parse(JSON.stringify(dataIn1))[0].filter(i=>typeof i === "number");
              
              dataIn1 = dataInTemp;   
              //recreate original line
              svg.selectAll(`#line_0`).remove();
             
              console.log("WHAT IS DATAHOLDER1 VALUE? ", dataHolder1.value);
              createLine([props.dataHolder1Parent],props.color0,1.5,"line_0");
              // createLine([dataHolder1.value],props.color0,1.5,"line_0");
              dataIn1.filter(i=>typeof i === "number");
              console.log("DATA IN in create new line 1: ", dataIn1)
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


            // SAVE GROUP 3 AND 4 UNTIL POST-MVP
            // // function to render new path element with D3's General Update Pattern
            // function createNewLine2(dataIn,strokeColor,strokeWidth,chosenClassName){ 
            //   document.getElementById("modalFull").classList.remove("receivedSingleTextData");
            //   console.log("WTF IS DATA IN IN CREATE LINE 2? ", dataIn);
            //   JSON.parse(JSON.stringify(dataIn))[0].forEach((t,ind)=>{
            //     if(typeof t === "undefined" || typeof t === "null"){
            //       console.log("removed undefined point ", dataIn[ind]);
            //       dataIn=dataIn.slice(ind)
            //     }
            //   })
            //   //recreate original line
            //   svg.selectAll(`#line_0`).remove();
            //   svg.selectAll(`#line_1`).remove();
            //   try{
            //     svg.selectAll(`#line_2`).remove();
            //   } catch(e){
            //     console.log("err in createline: ",e)
            //   }
            //   createLine([props.dataHolder1Parent],props.color0,1.5,"line_0");
            //   // createNewLine1([JSON.parse(JSON.stringify(dataRef2.value))],props.color1,1.75,"line_1");
            //   createNewLine1([props.dataHolder2Parent],props.color1,1.75,"line_1");
            //   svg
            //       .selectAll(`#line_2`)
            //       .data(dataIn) // sync them with our data
            //       .join(`path`) // create a new "path" for new pieces of data (if needed)
            //       .attr("stroke", strokeColor)
            //       .attr("id", "line_2")
            //       .attr("stroke-width", strokeWidth)
            //       .attr("d", lineGen); // shape and form of our line!          
            //   const xAxis = axisBottom(xScale);
                      
            //   return svg; 
            // }
            
            // // function to render new path element with D3's General Update Pattern
            // function createNewLine3(dataIn,strokeColor,strokeWidth,chosenClassName){  
            //   JSON.parse(JSON.stringify(dataIn)).forEach((t,ind)=>{
            //       if(typeof t === "undefined" || typeof t === "null"){
            //         console.log("removed undefined point ", dataIn[ind]);
            //         dataIn=dataIn.slice(ind)
            //       }
            //     })
            //     //recreate original line
            //     svg.selectAll(`#line_0`).remove();
            //     svg.selectAll(`#line_1`).remove();
            //     svg.selectAll(`#line_2`).remove();
                
            //     // createLine([dataRef1.value],props.color0,1.5,"line_0");
            //     // createNewLine1([JSON.parse(JSON.stringify(dataRef2.value))],props.color1,1.75,"line_1");
            //     // createNewLine2([JSON.parse(JSON.stringify(dataRef3.value))],props.color2,2.00,"line_2");
            //     createLine([props.dataHolder1Parent],props.color0,1.5,"line_0");
            //     createNewLine1([props.dataHolder2Parent],props.color1,1.75,"line_1");
            //     createNewLine2([props.dataHolder3Parent],props.color2,2.00,"line_2");
                
            //     svg
            //         .selectAll(`#line_3`)
            //         .data(JSON.parse(JSON.stringify(dataIn))) // sync them with our data
            //         .join(`path`) // create a new "path" for new pieces of data (if needed)
            //         .attr("stroke", strokeColor)
            //         .attr("id", "line_3")
            //         .attr("stroke-width", strokeWidth)
            //         .attr("d", lineGen); // shape and form of our line!          
            //     const xAxis = axisBottom(xScale);        
            //     return svg; 
            // }
            
            

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
              console.log("height check in: ", height);
              console.log("WHAT IS CURRENT GRAPHSTATE: ", JSON.parse(JSON.stringify(props)).graphstate);
              console.log("check resizeState in d3-heavy chunk for axes: ", JSON.parse(JSON.stringify(JSON.parse(JSON.stringify(resizeState)))));

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
                //xMax.value = JSON.parse(JSON.stringify(props)).numberXMax[1];
                console.log("xMax value: ", xMax.value);
                let tryGetKeyAxisXMax = document.getElementById("xAxisRangeDisplayMax");
                let tryGetKeyAxisXMin = document.getElementById("xAxisRangeDisplayMin");
                let tryGetKeyAxisYMax = document.getElementById("yAxisRangeDisplayMax");
                let tryGetKeyAxisYMin = document.getElementById("yAxisRangeDisplayMin");

                let tryGetKeyXMax = document.getElementById("xRangeDisplayXMax_0");
                let tryGetKeyXMin = document.getElementById("xRangeDisplayXMin_0");
                let tryGetKeyYMax = document.getElementById("xRangeDisplayYMax_0");
                let tryGetKeyYMin = document.getElementById("xRangeDisplayYMin_0");
                if(tryGetKeyXMax){
                  tryGetKeyXMax.innerText = xMax.value
                } else {
                  console.log("CAN'T GET KEY XMIN!!!!!!!")
                }
                if(tryGetKeyXMin){
                  tryGetKeyXMin.innerText = xMin.value
                } else {
                  console.log("CAN'T GET KEY XMAX!!!!!!!")
                }
                if(tryGetKeyYMax){
                  tryGetKeyYMax.innerText = yMax.value
                } else {
                  console.log("CAN'T GET KEY YMAX!!!!!!!")
                }
                if(tryGetKeyYMin){
                  tryGetKeyYMin.innerText = yMin.value
                } else {
                  console.log("CAN'T GET KEY YMIN!!!!!!!")
                }
                if(tryGetKeyAxisXMax){
                  tryGetKeyAxisXMax.innerText = xMax.value
                } else {
                  console.log("CAN'T GET KEY AXIS XMIN!!!!!!!")
                }
                if(tryGetKeyAxisXMin){
                  tryGetKeyAxisXMin.innerText = xMin.value
                } else {
                  console.log("CAN'T GET KEY AXIS XMAX!!!!!!!")
                }
                if(tryGetKeyAxisYMax){
                  tryGetKeyAxisYMax.innerText = yMax.value
                } else {
                  console.log("CAN'T GET KEY AXIS YMAX!!!!!!!")
                }
                if(tryGetKeyAxisYMin){
                  tryGetKeyAxisYMin.innerText = yMin.value
                } else {
                  console.log("CAN'T GET KEY AXIS YMIN!!!!!!!")
                }
              
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
              console.log("WE ARE CHANGING Y AXIS NOW!!! ");
           
              const yAxis = axisLeft(yScale);
              let oldYLabel = svg
                .select(".y-axis")
                .selectAll(`text`)['_groups'][0][svg
                .select(".y-axis")
                .selectAll(`text`)['_groups'][0].length -1]
              if(oldYLabel){
                oldYLabel.remove();
              }
              console.log("are we getting color? ", color);
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
                console.log("RESETTING Y ", JSON.parse(JSON.stringify(props)).numberYMax);
                yMax.value = JSON.parse(JSON.stringify(props)).numberYMax[JSON.parse(JSON.stringify(props)).numberYMax.length - 1];
                yMin.value = JSON.parse(JSON.stringify(props)).numberYMin[JSON.parse(JSON.stringify(props)).numberYMax.length - 1];
                console.log("Y MIN VAL IS NOW... ", yMin.value);
                console.log("Y MAX VAL IS NOW... ", yMin.value);

                // emit("resetY")
                resetYNeeded.value = true;
              }
              console.log("*** SVG y axis *** ", svg);
              return svg
            }


            svg.on('mouseover', function(d) {
              console.log("what is D??? ", d);
              console.log("what is props data length> ", JSON.parse(JSON.stringify(props)).data.length);
              console.log("what is width? ", width);
              let selectedIndexX = Math.floor((d.offsetX/width) * JSON.parse(JSON.stringify(props)).data.length);
            
              if(!selectedIndexX ){
                return;
              } else {
                if(!selectedIndexX){
                  return;
                }
                console.log("what is D? ", d);
                console.log("what is selected X? ", selectedIndexX);
                this.selectedIndexX = selectedIndexX;
            
                if(selectedIndexX > 0){
                  console.log("emitting the selected x index ", selectedIndexX)
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
        console.log("RESIZEREF ", resizeRef);

    // return refs to make them available in template
    return { svgRef, resizeRef, mouseMove,tooltipmsg, show,resetShow,dataHolder1};
  },
  methods: {
    tryAppendTopics(newVal){
      console.log("CAN WEE APPEND TOPICS>???")
      let topicListWrapper = document.getElementById("topicListWrapper");
      let tooltipInner = document.getElementById("tooltipInner")
      if(topicListWrapper && tooltipInner){
        JSON.parse(JSON.stringify(JSON.parse(JSON.stringify(newVal)).entityArrays)).forEach((entArr)=>{
          try{
            if(entityArr.indexOf(entArr[0]) === -1){
              entityArr.push(entArr[0]);
            }
          } catch {
            console.log("ERROR!!!! ------------ ",entArr)
          }
          console.log("ENTITY ARR: ", entityArr);
        })
      }
    },

    // mouseMove(event) {
    //   const { clientX, clientY } = event;
    //   show.value = true;
    //   console.log("this show: ", show.value);
    //   console.log("this client x: ", event.clientX);
    //   console.log("this client y: ", event.clientY);
    //   this.clientX = event.clientX;
    //   this.clientY = event.clientY;
    // }
  },
  watch: { 
    dataHolder1:{
        // deep: true,
        handler: function(newVal, oldVal){
  
          console.log("fuck shit testchart 1 old ", oldVal);
          console.log("fuck shit testchart 1 new ", newVal);
          
          if(oldVal !== newVal){
            console.log("MISMATCH! old: ", oldVal);
            console.log("MISMATCH! new: ", newVal);
            // dataH1 = newVal;
            
            // dataHolder1.value = 
          }
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    // dataHolder2:{
    //     deep: true,
    //     handler: function(newVal, oldVal){
    //       console.log("fuck shit testchart 1");
    //       // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
    //     }
    // },
    // dataHolder3:{
    //     deep: true,
    //     handler: function(newVal, oldVal){
    //       console.log("fuck shit testchart 1");
    //       // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
    //     }
    // },
    xMax:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("fuck shit testchart 1");
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    yMax:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("fuck shit testchart 2");
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    xMin:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("fuck shit testchart 3");
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    yMin:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("fuck shit testchart 4");
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    xMaxLabel:{
        deep: true,
        handler: function(newVal, oldVal){
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    yMaxLabel:{
        deep: true,
        handler: function(newVal, oldVal){
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    selectedRow:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("fuck shit testchart 5");
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    currentLinesCount:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("fuck shit testchart 6");
          console.log("GREAT CHECK!! ",newVal)
          if(dataRef1.value && dataHolder1.value === []){
            console.log("this sucks");
            dataHolder1.value.push(dataRef1.value);
          }
          if(newVal === 1){
            if(oldVal.length > 0){
                    dataHolder1.value = oldVal;
                  }
          }
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    }, 
    resetXNeeded:{
      handler: function(newVal, oldVal){
        console.log("fuck shit testchart 7");
        console.log("RESET NEEDED ", newVal);

      }
    },
    resetYNeeded:{
      handler: function(newVal, oldVal){
        console.log("fuck shit testchart 8");
        console.log("RESET NEEDED ", newVal);

      }
    },
    axisColorMatchBool:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("newCOLORMATCH BOOL: ",newVal);
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },     
    color0:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("fuck shit testchart 9");
          console.log("newCOL: ",newVal);
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    color1: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log(newVal);
          // alert('color1 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    color2: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log(newVal);
        //  alert('color2 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    color3: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log(newVal);
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    colorX: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log(newVal);
          console.log("here's keybuilder div");
              let keyBuilder = document.getElementById("d3UpdateButtonsWrapper");
              
              if(keyBuilder){
                console.log("NEW COLOR>>X AXIS? ", newVal);
                keyBuilder.style.borderColor = newVal.value;
              }
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    colorY: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log(newVal);
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    valueX: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("fuck shit testchart 10");
          console.log("new x value", newVal);
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
          //WE'LL NEED TO SET THIS FOR OTHER BLOCKS THAN JUST 1!!
          // xAxisLabel.value = JSON.parse(JSON.stringify(newVal));
          
        }
    },
    valueY: {
        deep: true,
        handler: function(newVal, oldVal){

          console.log("new yyy value", newVal);
          
          // yAxisLabel.value = JSON.parse(JSON.stringify(newVal));
    
        }
    },
    numberXMin: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("in new xmin!")
        }
    },
    numberXMax: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("in new xmax!")
          console.log("fuck shit testchart 12");
          // console.log("new x MAX number", Math.max(...Object.values(JSON.parse(JSON.stringify(newVal)))));
          // if(JSON.parse(JSON.stringify(props)).numberXMax.value.filter(i=>typeof i === "number").length > 0){
          //   numberXMax.value = Math.min(...JSON.parse(JSON.stringify(props)).numberXMax.value.filter(i=>typeof i === "number"))
          // } else {
          //   numberXMax.value = 0;
          // }
            // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    numberYMin: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("in new ymin!")
          console.log("new y number", newVal);
          console.log("fuck shit testchart 13");
            // if(JSON.parse(JSON.stringify(newVal.value)).filter(i=>typeof i === "number").length > 0){
            //   this.numberYMin = Math.min(...JSON.parse(JSON.stringify(newVal.value)).filter(i=>typeof i === "number"))
            //this.numberYMin = JSON.parse(JSON.stringify(newVal));
            // } 
            // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    numberYMax: {
        deep: true,
        handler: function(newVal, oldVal){
          // console.log("in new ymax!")
          console.log("in new y max: ", newVal);
   
            // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    selectedXAxisRef: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("********* new x number", newVal);
          console.log("new x axis ref in test", Math.max(...newVal));
          console.log("fuck shit testchart 15");
          // this.selectedXAxisRef = newVal;
        }
    },
    selectedYAxisRef: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("********* new y number", JSON.parse(JSON.stringify(newVal)));
          // this.selectedYAxisRef = newVal;
        }
    },
    yAxisFramingLast: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("fuck shit testchart 6");
            if(newVal){
              console.log("AXES FRAMING CHANGHED IN TEST FILE! ",newVal);
            } 
        }
    },
    show: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("SHOW VALUE! ", newVal);
        }
    },
    graphstate: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("fuck shit testchart 17");
            console.log("graphstate changed in area! ", newVal)
            // if(newVal){
                
                // console.log("parse method: ", JSON.parse(JSON.stringify(this.graphstate)));

                // console.log("THIS WAY??? ", JSON.parse(JSON.stringify(this)).graphstate)
              
                // console.log("what about number XMAX? ", this.data.numberXMax)
                // JSON.parse(JSON.stringify(props)).graphstate = newVal
                // // alert("we are now comparing");
                // return this.data.graphstate;
            // }
        }
    },
    tooltipmsg: {
      deep: true,
      handler: async function(newVal, oldVal){
        console.log("fuck shit testchart 18");
        console.log('Prop changed: ', newVal, ' | was: ', oldVal)
        

////////////////
//**************

function updateTooltip(newVal){
      console.log("fuck shit testchart 20 ", JSON.parse(JSON.stringify(newVal)));
      // newVal = tooltipmsg.value;
      console.log("the fuck is newval?", JSON.parse(JSON.stringify(newVal)));
      show.value = true;
       let tooltip = document.getElementById("tooltipInner");
          console.log("tooltip inner: ", tooltip);

          console.log("NEW TOOLTIP-READY VALS!!! UI GOLDMINE!!!! ", JSON.parse(JSON.stringify(newVal)))
          // console.log("YOYOYOYO ENTITY ARR", JSON.parse(JSON.stringify(newVal)).sentenceGrammarArray);
          // console.log("YOYOYOYO GRAMMAR ARR ", JSON.parse(JSON.stringify(newVal)).sentenceEntityArray);
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
        
          console.log("what the heck is this?: ", JSON.parse(JSON.stringify(newVal)).entityArrays);
          if(newVal){
            console.log('what in the world is this? ', JSON.parse(JSON.stringify(newVal)).entityArrays);
            JSON.parse(JSON.stringify(JSON.parse(JSON.stringify(newVal)).entityArrays)).forEach(i=>topicWrapper.append(`${i[0]}\n`))
          }
    }
    updateTooltip(newVal)
//**************
////////////////


          // let tooltip = await document.getElementById("tooltipInner");
          // console.log("tooltip inner: ", tooltip);

          // console.log("NEW TOOLTIP-READY VALS!!! UI GOLDMINE!!!! ", JSON.parse(JSON.stringify(newVal)))
          // console.log("YOYOYOYO ENTITY ARR", JSON.parse(JSON.stringify(newVal)).sentenceGrammarArray);
          //   console.log("YOYOYOYO GRAMMAR ARR ", JSON.parse(JSON.stringify(newVal)).sentenceEntityArray);
          //   console.log("WHAT IS TOOLTOIP?? ", tooltip);
          // if(tooltip){
          //   tooltip.innerHTML = `
          //   <div id="sentimentDisplay">
          
          //     <h4 class="HUD-Test-half-div">Comp: ${JSON.parse(JSON.stringify(newVal)).sentimentCompound}</h1>
          //     <h4 class="HUD-Test-half-div">Neg: ${JSON.parse(JSON.stringify(newVal)).sentimentNegative}</h1>
          //     <h4 class="HUD-Test-half-div">Neu: ${JSON.parse(JSON.stringify(newVal)).sentimentNeutral}</h1>
          //     <h4 class="HUD-Test-half-div">Pos: ${JSON.parse(JSON.stringify(newVal)).sentimentPositive}</h1>
          //   </div>
        
          //   <div id="topicListWrapper">
          //     ${entityArr.value.toString()}
          //   </div> 
          //   `
          // }
          // let topicWrapper = document.getElementById("topicListWrapper");
        
          // console.log("what the heck is this?: ", JSON.parse(JSON.stringify(newVal)).entityArrays);
          // if(newVal){
          //   console.log('what in the world is this? ', JSON.parse(JSON.stringify(newVal)).entityArrays);
          //   JSON.parse(JSON.stringify(JSON.parse(JSON.stringify(newVal)).entityArrays)).forEach(i=>topicWrapper.append(`${i[0]}\n`))
          // }
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
  top: 4px;
}
#svgId {
    background: rgba(0,0,0,0.98);
    bottom: 16%;
}
#tooltip {
  border: 1px solid black;
  padding: 5px;
  position: absolute;
  background-color: transparent;
  color:#ffffff;
  font-size: 16px;
  font-weight: 400;
  z-index:9999;
    margin-left: 36px;
 
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