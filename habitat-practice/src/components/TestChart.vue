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
import useResizeObserver from "@/use/resizeObserver";

export default {
  name: "ResponsiveLineChart",
  props: ["data","newData","mode","tooltipmsg","graphstate", "color0", "color1", "color2", "color3","colorX","colorY","valueX","numberXMax","numberXMin","numberYMax","numberYMin","valueY","numberY", "currentLinesCount","secondTextRef","axisColorMatchBool","selectedXAxisRef","selectedYAxisRef","selectedRow"],
  emits:["selected"],
  watch: { 
    selectedRow:{
        deep: true,
        handler: function(newVal, oldVal){
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    currentLinesCount:{
        deep: true,
        handler: function(newVal, oldVal){
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    }, 
    resetXNeeded:{
      handler: function(newVal, oldVal){
        console.log("RESET NEEDED ", resetXNeeded.value);

      }
    },
    resetYNeeded:{
      handler: function(newVal, oldVal){
        console.log("RESET NEEDED ", resetYNeeded.value);

      }
    },
    axisColorMatchBool:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("newCOLORMATCH BOOL: ",JSON.parse(JSON.stringify(newVal)));
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },     
    color0:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("newCOL: ",JSON.parse(JSON.stringify(newVal)));
          // alert('color0 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    color1: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log(JSON.parse(JSON.stringify(newVal)));
          // alert('color1 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    color2: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log(JSON.parse(JSON.stringify(newVal)));
        //  alert('color2 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    color3: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log(JSON.parse(JSON.stringify(newVal)));
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    colorX: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log(JSON.parse(JSON.stringify(newVal)));
              let keyBuilder = document.getElementById("d3UpdateButtonsWrapper");
              console.log("here's keybuilder div");
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
          console.log(JSON.parse(JSON.stringify(newVal)));
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    valueX: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("new x value", JSON.parse(JSON.stringify(newVal)));
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
          //WE'LL NEED TO SET THIS FOR OTHER BLOCKS THAN JUST 1!!
          
        }
    },
    valueY: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("new yyy value", JSON.parse(JSON.stringify(newVal)));
          this.xAxisLabel = JSON.parse(JSON.stringify(newVal));
    
        }
    },
    numberXMin: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("new x number", newVal);
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    numberXMax: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("new x MAX number", newVal);
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    numberYMin: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("new y number", Math.min(...JSON.parse(JSON.stringify(newVal))));
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
        numberYMax: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("new y MAX number", Math.max(...JSON.parse(JSON.stringify(newVal))));
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    selectedXAxisRef: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("********* new x number", JSON.parse(JSON.stringify(newVal)));
          
        }
    },
    selectedYAxisRef: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("********* new y number", JSON.parse(JSON.stringify(newVal)));
        }
    },
    graphstate: {
        deep: true,
        handler: function(newVal, oldVal){
    
            console.log("graphstate changed in area! ", newVal)
            if(newVal > 0){
                
                console.log("parse method: ", JSON.parse(JSON.stringify(this.graphstate)));

                console.log("THIS WAY??? ", JSON.parse(JSON.stringify(this)).graphstate)
              
                
                this.data.graphstate = newVal
                // alert("we are now comparing");
                return this.data.graphstate;
            }
        }
    },
    tooltipmsg: {
      deep: true,
      handler: function(newVal, oldVal){
      
        console.log('Prop changed: ', newVal, ' | was: ', oldVal)
        
          let tooltip = document.getElementById("tooltipInner");
          if(tooltip){
            tooltip.innerHTML = `
            <div id="sentimentDisplay">
          
              <h4 class="HUD-Test-half-div">Comp: ${JSON.parse(JSON.stringify(newVal)).sentimentCompound}</h1>
              <h4 class="HUD-Test-half-div">Neg: ${JSON.parse(JSON.stringify(newVal)).sentimentNegative}</h1>
              <h4 class="HUD-Test-half-div">Neu: ${JSON.parse(JSON.stringify(newVal)).sentimentNeutral}</h1>
              <h4 class="HUD-Test-half-div">Pos: ${JSON.parse(JSON.stringify(newVal)).sentimentPositive}</h1>
            </div>
        
            <div id="topicListWrapper">
              ${this.entityArr.toString()}
            </div> 
            `
          }
          let topicWrapper = document.getElementById("topicListWrapper");
          console.log(JSON.parse(JSON.stringify(JSON.parse(JSON.stringify(newVal)).entityArrays)));
          if(newVal){
            JSON.parse(JSON.stringify(JSON.parse(JSON.stringify(newVal)).entityArrays)).forEach(i=>topicWrapper.append(`${i[0]}\n`))
          }
      }
    }
  },
  data(){
    return {
      show: false,
      clientX: 0,
      clientY: 0,
      closestPoint: null,
      entityArr:[],
      graphstate: 0,
      xAxisLabel: ''
    };
  },
  setup(props,{emit}) {
      const points = ref();
      points.value = [];
      const scaled = ref();
    
      const graphMode = ref()
      graphMode.value = 0;
      console.log("Y REF: ", props.selectedYAxisRef);
      console.log("X REF: ", props.selectedXAxisRef);
      scaled.value = {
        x: null,
        y: null
      };      
      let tooltipMsg = {
        grammarArrays: [],
        sentenceSentimentCompound: 0,
        sentenceSentimentNegative: 0,
        sentenceSentimentNeutral: 0,
        sentenceSentimentPositive: 0,
        entityArrays: [],
      }
    // create ref to pass to D3 for DOM manipulation
    const svgRef = ref(null);
    const resetXNeeded = ref(false);
    const resetYNeeded = ref(false);

    const lineLabelsArr = ref([]);

    //this.data = newData;
    // this creates another ref to observe resizing, 
    // which we will attach to a DIV,
    // since observing SVGs with the ResizeObserver API doesn't work properly
    const { resizeRef, resizeState } = useResizeObserver();

    onMounted((event) => {
      // pass ref with DOM element to D3, when mounted (DOM available)
      const svg = select(svgRef.value);

      let tempSVGs=[]

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
      
      // whenever any dependencies (like data, resizeState) change, call this!
      watchEffect(() => {
        if(JSON.parse(JSON.stringify(props.data)).length < 1){
          return;
        }

        // console.log("RESIZEE STATE: ", resizeState);
        const { width, height } = resizeState.dimensions;
            console.log("WIDTH: ", width);
            console.log("HEIGHT: ", height);
            console.log("D3=> ", d3);
              
        console.log("What is props data in test chart?: ", JSON.parse(JSON.stringify(props.data)));

        if(Math.max(...JSON.parse(JSON.stringify(props.data))) > yMax.value){
          yMax.value = Math.max(...JSON.parse(JSON.stringify(props.data)));
        if(Object.keys(svg).length < 1){
          return;
        } else {
          console.log("SVG IS: ", Object.keys(svg));
        }
          let yMaxRescale = svg
            .select(".y-axis")
            .selectAll(`text`)['_groups'][0][svg
            .select(".y-axis")
            .selectAll(`text`)['_groups'][0].length -1]

          if(yMaxRescale && yMaxRescale.childNodes.length > 0){
            yMaxLabel.value = yMaxRescale.childNodes[0].data;
          }
        }

        if((!props.selectedXAxisRef || !props.selectedYAxisRef)){
          console.log("incoming! ", JSON.parse(JSON.stringify(props.data)).length - 1);
          if((JSON.parse(JSON.stringify(props.data)).length - 1) > xMax.value){
            
            xMax.value = JSON.parse(JSON.stringify(props.data)).length - 1;

            let xMaxRescale = svg
              .select(".x-axis")
              .selectAll(`text`)['_groups'][0][svg
              .select(".x-axis")
              .selectAll(`text`)['_groups'][0].length -1]

            if(xMaxRescale && xMaxRescale.childNodes.length > 0){
              xMaxLabel.value = xMaxRescale.childNodes[0].data;
            }
          }
          xMin.value = 0;
          // yMax.value = max(props.data);

          if(Math.max(...JSON.parse(JSON.stringify(props.numberYMax))) > yMax.value){
      
            yMax.value = Math.max(...JSON.parse(JSON.stringify(props.numberYMax)));
          }
          // yMin.value = min(props.data);
          yMin.value = Math.min(...JSON.parse(JSON.stringify(props.numberYMin)));

        } else {

          if(resetXNeeded.value === true || Math.max(...JSON.parse(JSON.stringify(props.numberXMax))) > xMax.value){
            resetXNeeded.value = false;
            xMax.value = Math.max(...JSON.parse(JSON.stringify(props.numberXMax)));
          }
          xMin.value = Math.min(JSON.parse(...JSON.stringify(props.numberXMin)));
          if(resetYNeeded.value === true || Math.max(JSON.parse(...JSON.stringify(props.numberYMax))) > yMax.value){
            resetYNeeded.value = false;
            yMax.value = Math.max(JSON.parse(...JSON.stringify(props.numberYMax)));
          }
          xMin.value = Math.min(JSON.parse(...JSON.stringify(props.numberXMin)));

            console.log("GET VALUE BEFORE ARRAYS ", JSON.parse(JSON.stringify(props.selectedXAxisRef))['value']);

            if(resetXNeeded.value === true || xMax.value < JSON.parse(JSON.stringify(props.selectedXAxisRef))['value'][1][0]){
              resetXNeeded.value = false;
              xMax.value = JSON.parse(JSON.stringify(props.selectedXAxisRef))['value'][1][0];
            }

            if(xMin.value > JSON.parse(JSON.stringify(props.selectedXAxisRef))['value'][0][0]){
              xMin.value = JSON.parse(JSON.stringify(props.selectedXAxisRef))['value'][0][0];
            }
            if(resetYNeeded.value === true || yMax.value < JSON.parse(JSON.stringify(props.selectedYAxisRef))['value'][1][0]){
              resetYNeeded.value = false;
              yMax.value = JSON.parse(JSON.stringify(props.selectedYAxisRef))['value'][1][0];
            }
            if(yMin.value > JSON.parse(JSON.stringify(props.selectedYAxisRef))['value'][0][0]){
              yMin.value = JSON.parse(JSON.stringify(props.selectedYAxisRef))['value'][0][0];
            }
            console.log(`xmin: ${xMin.value} / xmax: ${xMax.value} / ymin ${yMax.value} / ymax ${xMin.value}`)
        }

        // scales: map index / data values to pixel values on x-axis / y-axis
        const xScale = scaleLinear()
          .domain([xMin.value,xMax.value])
          //.domain([0, props.data.length - 1]) // input values...
          .range([0, width]); // ... output values
        
        const yScale = scaleLinear()
          .domain([yMin.value,yMax.value])
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
        Object.values(props.data).forEach((t,ind)=>{
          if(typeof t=== undefined){
            props.data=props.data.slice(ind)
          }
        })
        //////////////////////////////////////////////

        if(props.length < 1){
          return;
        } else {
          console.log("D3 NAMESPACES=> ", d3.namespaces);
          console.log("WTF IS GRAPHSTATE ", props.graphstate);
          if(props.graphstate === 0){
            dataRef1.value = props.data; 
           
            let vals = Object.values(JSON.parse(JSON.stringify(dataRef1.value)))
            for(let v = 0;v<vals.length-1;v++){
              console.log("hell ", Object.values(JSON.parse(JSON.stringify(dataRef1.value)))[v])
              if(typeof Object.values(JSON.parse(JSON.stringify(dataRef1.value)))[v] === "number"){

              } else {
                console.log("what type is this? ", typeof Object.values(JSON.parse(JSON.stringify(dataRef1.value)))[v]);
              }
            }
            createLine([dataRef1.value],props.color0,1.5,"line_0");
          }

          if(props.graphstate === 1){
            // This will be line #2
            dataRef2.value = JSON.parse(JSON.stringify(props.data)); 
            let toDel = svg.selectAll(`.line#line_1`);
            if(toDel.length > 0){
              for(let i = 0;i<toDel.length - 1;i++){
                console.log(toDel[i]);
                toDel[i].remove();
              }
            }
            if(dataRef2.value.length > 0){
              if(Math.max(JSON.parse(JSON.stringify(dataRef2.value)))> yMax.value){
                yMax.value = Math.max(...JSON.parse(JSON.stringify(dataRef2.value)))
              }
              createNewLine1([JSON.parse(JSON.stringify(dataRef2.value))],props.color1,1.75,"line_1");
            }
          }

          if(props.graphstate === 2){
            // this will be for line #3
            dataRef3.value = JSON.parse(JSON.stringify(props.data)); 
            let toDel = svg.selectAll(".line#line_2")
            if(toDel.length > 0){
              for(let i = 0;i<toDel.length - 1;i++){
                toDel[i].remove();
              }
            }
            if(dataRef3.value.length > 0){
              if(Math.max(JSON.parse(JSON.stringify(dataRef3.value)))> yMax.value){
                yMax.value = Math.max(...JSON.parse(JSON.stringify(dataRef3.value)))
              }
              createNewLine2([JSON.parse(JSON.stringify(dataRef3.value))],props.color2,2,"line_2");
            }
          }
          if(props.graphstate === 3){
            dataRef4.value = JSON.parse(JSON.stringify(props.data));
            let toDel = svg.selectAll(".line#line_3")
            if(toDel.length > 0){
              for(let i = 0;i<toDel.length - 1;i++){
                toDel[i].remove();
              }
            }
            if(dataRef4.value.length > 0){
              if(Math.max(JSON.parse(JSON.stringify(dataRef4.value)))> yMax.value){
                yMax.value = Math.max(...JSON.parse(JSON.stringify(dataRef4.value)))
              }
               createNewLine3([JSON.parse(JSON.stringify(dataRef4.value))],props.color3,2.25,"line_3");
            }
          }
          
          let textDivX = document.getElementById(`newVariable_${JSON.parse(JSON.stringify(props.currentLinesCount))-1}_xvar`);
        
          if(textDivX){
            textDivX.innerText = JSON.parse(JSON.stringify(props.valueX));
            console.log("inner text div x ", textDivX.innerText);
            if(lineLabelsArr.value.indexOf(textDivX.innerText) === -1){
              lineLabelsArr.value.push(textDivX.innerText);
            }
          }
          let textDivY = document.getElementById(`newVariable_${JSON.parse(JSON.stringify(props.currentLinesCount))-1}_yvar`);
      
          if(textDivY){
            textDivY.innerText = JSON.parse(JSON.stringify(props.valueY));
            console.log("text div Y: ", textDivY);
            if(lineLabelsArr.value.indexOf(textDivY.innerText) === -1){
              lineLabelsArr.value.push(textDivY.innerText);
            }
          }
        }

        // function to render path element with D3's General Update Pattern
        function createLine(dataIn,strokeColor,strokeWidth,chosenClassName){ 
          svg
            .selectAll(".line") // get all "existing" lines in svg
            .data(dataIn) // sync them with our data
            .join("path") // create a new "path" for new pieces of data (if needed)
            // everything after .join() is applied to every "new" and "existing" element
            .attr("id", `line_0`)
            .attr("class", "line") // attach class (important for updating)
            .attr("stroke", strokeColor)
            .attr("stroke-width", strokeWidth)
            .attr("d", lineGen); // shape and form of our line!
          return svg; 
        }

        // function to render new path element with D3's General Update Pattern
        // --------------------------------------------------------------------
        function createNewLine1(dataIn,strokeColor,strokeWidth,chosenClassName){ 
          JSON.parse(JSON.stringify(dataIn)).forEach((t,ind)=>{
            if(typeof t === "undefined" || typeof t === "null"){
              console.log("removed undefined point ", dataIn[ind]);
              dataIn=dataIn.slice(ind)
            }
          })
          //recreate original line
          svg.selectAll(`#line_0`).remove();
          createLine([dataRef1.value],props.color0,1.5,"line_0");
          svg
              .selectAll(`#line_1`)
              .data(dataIn) // sync them with our data
              .join(`path`) // create a new "path" for new pieces of data (if needed)
              .attr("stroke", strokeColor)
              .attr("id", "line_1")
              .attr("stroke-width", strokeWidth)
              .attr("d", lineGen); // shape and form of our line!          
          const xAxis = axisBottom(xScale);
                  
          return svg; 
        }

        // function to render new path element with D3's General Update Pattern
        function createNewLine2(dataIn,strokeColor,strokeWidth,chosenClassName){ 
          JSON.parse(JSON.stringify(dataIn)).forEach((t,ind)=>{
            if(typeof t === "undefined" || typeof t === "null"){
              console.log("removed undefined point ", dataIn[ind]);
              dataIn=dataIn.slice(ind)
            }
          })
          //recreate original line
          svg.selectAll(`#line_0`).remove();
          svg.selectAll(`#line_1`).remove();
          createLine([dataRef1.value],props.color0,1.5,"line_0");
          createNewLine1([JSON.parse(JSON.stringify(dataRef2.value))],props.color1,1.75,"line_1");
          svg
              .selectAll(`#line_2`)
              .data(dataIn) // sync them with our data
              .join(`path`) // create a new "path" for new pieces of data (if needed)
              .attr("stroke", strokeColor)
              .attr("id", "line_2")
              .attr("stroke-width", strokeWidth)
              .attr("d", lineGen); // shape and form of our line!          
          const xAxis = axisBottom(xScale);
                  
          return svg; 
        }
        
        
                // function to render new path element with D3's General Update Pattern
        function createNewLine3(dataIn,strokeColor,strokeWidth,chosenClassName){ 
            JSON.parse(JSON.stringify(dataIn)).forEach((t,ind)=>{
              if(typeof t === "undefined" || typeof t === "null"){
                console.log("removed undefined point ", dataIn[ind]);
                dataIn=dataIn.slice(ind)
              }
            })
            //recreate original line
            svg.selectAll(`#line_0`).remove();
            svg.selectAll(`#line_1`).remove();
            svg.selectAll(`#line_2`).remove();
            createLine([dataRef1.value],props.color0,1.5,"line_0");
            createNewLine1([JSON.parse(JSON.stringify(dataRef2.value))],props.color1,1.75,"line_1");
            createNewLine2([JSON.parse(JSON.stringify(dataRef3.value))],props.color2,2.00,"line_2");
            svg
                .selectAll(`#line_3`)
                .data(dataIn) // sync them with our data
                .join(`path`) // create a new "path" for new pieces of data (if needed)
                .attr("stroke", strokeColor)
                .attr("id", "line_3")
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
                .attr("x", resizeState.dimensions.width)
                .attr("y", 30)
                .attr("fill", "currentColor")
                .attr("text-anchor", "end")
                .text(JSON.parse(JSON.stringify(props.valueX))));
            // this should be new label!!
          if(props.graphstate < 1 && oldXLabel !== xMaxLabel.value && oldXLabel !== xMaxLabel.value){
            
            xMax.value = JSON.parse(JSON.stringify(props.numberXMax))[1];
            resetXNeeded.value = true;
          }
          return svg;
        }
        if(props.axisColorMatchBool){
          createYAxis(props.colorY)
        } else {
          createYAxis(props.colorX)
        }
          createXAxis(props.colorX);

        function createYAxis(color){
          const yAxis = axisLeft(yScale);
          let oldYLabel = svg
            .select(".y-axis")
            .selectAll(`text`)['_groups'][0][svg
            .select(".y-axis")
            .selectAll(`text`)['_groups'][0].length -1]
          if(oldYLabel){
            oldYLabel.remove();
          }
            svg.select(".y-axis")
                .style("color", color)
                .call(yAxis)
                // add y axis label
                .call(g => g.append("text")
                .attr("y", -12)
                .attr("x", -40)
                .attr("fill", "currentColor")
                .attr("text-anchor", "start")
       
                .text(JSON.parse(JSON.stringify(props.valueY))));

          console.log("NEW LABEL: ", oldYLabel)
          console.log("Y MAXXXXXXX LLLLLAAAABBBBEEELLLL VALUE: ", yMaxLabel.value);
          console.log("MAXXXXXXX LLLLLAAAABBBBEEELLLL VALUE: ", xMaxLabel.value);
          if(props.graphstate < 1 && oldYLabel !== yMaxLabel.value && oldYLabel !== xMaxLabel.value){
            console.log("RESETTING Y");
            console.log("OH YEAH>? ", JSON.parse(JSON.stringify(props.numberYMax))[1]);
            yMax.value = JSON.parse(JSON.stringify(props.numberYMax))[1];
            // emit("resetY")
            console.log("CHECK CURRENT PROPS DATA HERE ", props.data);
            resetYNeeded.value = true;
          }
          console.log("*** SVG y axis *** ", svg);
          return svg
        }


        svg.on('mouseover', function(d) {
          let selectedIndexX = Math.floor((d.offsetX/width) * props.data.length);
         
          if(!selectedIndexX ){
            return;
          } else {
            if(!selectedIndexX){
              return;
            }
            console.log("what is D? ", d);
            this.selectedIndexX = selectedIndexX;
         
            if(selectedIndexX > 0){
              console.log("emitting the selected x index ", selectedIndexX)
              emit('selected',selectedIndexX);
            }
          }
        })

        for(let i = 0; i < props.data.length - 1; i++){
          points.value.push({
            x: i,
            y: props.data[i],
            max: height
          })
        }
        console.log("!!##POINTS: ", points.value);
      });
    });
    console.log("RESIZEREF ", resizeRef);
    // return refs to make them available in template
    return { svgRef, resizeRef };
  },
  methods: {
    tryAppendTopics(newVal){
      let topicListWrapper = document.getElementById("topicListWrapper");
      if(topicListWrapper && tooltipInner.value){
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

    mouseMove(event) {
      const { clientX, clientY } = event;
      this.show = true;
      this.clientX = event.clientX;
      this.clientY = event.clientY;
    }
  }
};
</script>

<template>
  <div id="barChartWrapper" ref="resizeRef">
    <!-- :style="{ top: `${clientY}px`, left: `${clientX}px` }" -->
    <div
        id="tooltip"
          :style="{ top: `${0}px`, left: `${0}px`, width: `${60}vw`,position:`absolute` }"
          v-if="this.show"
          @mouseout="this.show = false"
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
  margin-left: 64px;
  margin-right: 64px;
  top: 20px;
}
#svgId {
    background: rgba(0,0,0,0.98);
    bottom: 20px;
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