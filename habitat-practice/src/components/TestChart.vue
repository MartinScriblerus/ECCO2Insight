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
  props: ["data","newData","mode","tooltipmsg","graphstate", "color0", "color1", "color2", "color3","colorX","colorY","valueX","numberX","valueY","numberY", "currentLinesCount","secondTextRef"],
  emits:["selected"],
  watch: { 
    currentLinesCount:{
        deep: true,
        handler: function(newVal, oldVal){
          console.log("newCOL: ",JSON.parse(JSON.stringify(newVal)));
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
    numberX: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("new x number", newVal);
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    numberY: {
        deep: true,
        handler: function(newVal, oldVal){
          console.log("new y number", JSON.parse(JSON.stringify(newVal)));
          // alert('color3 changed: ', JSON.parse(JSON.stringify(newVal)))
        }
    },
    graphstate: {
        deep: true,
        handler: function(newVal, oldVal){
    
            console.log("graphstate changed in area! ", newVal)
            if(newVal > 0){
                this.graphState = newVal
                
                alert("we are now comparing");
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
      graphState: 'singleText',
      xAxisLabel: ''
    };
  },
  setup(props,{emit}) {
      const points = ref();
      points.value = [];
      const scaled = ref();
    
      const graphMode = ref()
      graphMode.value = "singleText";
      
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

    //this.data = newData;
    // this creates another ref to observe resizing, 
    // which we will attach to a DIV,
    // since observing SVGs with the ResizeObserver API doesn't work properly
    const { resizeRef, resizeState } = useResizeObserver();

    onMounted((event) => {
      // pass ref with DOM element to D3, when mounted (DOM available)
      const svg = select(svgRef.value);
      const tooltipInner = ref(null)


      
      // whenever any dependencies (like data, resizeState) change, call this!
      watchEffect(() => {
        console.log("sanity check: ", props.currentLinesCount);
     
        let textDivX = document.getElementById(`newVariable_${props.currentLinesCount-1}_xvar`);
        console.log("text div x ", textDivX);
        if(textDivX){
          textDivX.innerText = JSON.parse(JSON.stringify(props.valueX));
        }
        let textDivY = document.getElementById(`newVariable_${props.currentLinesCount-1}_yvar`);
        console.log("text div x ", textDivY);

        if(textDivY){
          textDivY.innerText = JSON.parse(JSON.stringify(props.valueY));
        }
        // tooltipMsg = props.tooltipMsg;
        // tooltipInner.value.innerText = props.tooltipMsg;
        document.getElementById('svgId').childNodes.forEach(c=>{
          console.log("SVG CHILD NODE: ", c);
        })
        console.log("RESIZEE STATE: ", resizeState);
        const { width, height } = resizeState.dimensions;
            console.log("WIDTH: ", width);
            console.log("HEIGHT: ", height);
            console.log("D3=> ", d3);
            if(!scaled.value.length){

            } else {
            console.log("SCALED X TAKE ONE: ", scaled.value.x);
            console.log("SCALED Y TAKE ONE: ", scaled.value.y);
            }
            
            scaled.value.x = d3.scaleLinear().range([0, width]);
            scaled.value.y = d3.scaleLinear().range([height, 0]);
            console.log("SCALED X TAKE TWO: ", scaled.value.x);
            console.log("SCALED Y TAKE TWO: ", scaled.value.y);
            d3.axisLeft().scale(scaled.value.x);
            d3.axisBottom().scale(scaled.value.y);
            // emit('width', width);
            // emit('height',height);
            console.log("what is props mode? ", JSON.parse(JSON.stringify(props.mode))[0])
        
        // scales: map index / data values to pixel values on x-axis / y-axis
        const xScale = scaleLinear()
          .domain([0, props.data.length - 1]) // input values...
          .range([0, width]); // ... output values
        console.log("What is props data in area?: ", props.data);

        const yScale = scaleLinear()
          .domain([min(props.data), max(props.data)]) // input values...
          .range([height, 0]); // ... output values
     
        // line generator: D3 method to transform an array of values to data points ("d") for a path element
        const lineGen = area()
          .curve(curveBasis)
          .x((value, index) => xScale(index))
          .y((value) => yScale(value));
        
        // removed undefined values that throw errors
        Object.values(props.data).forEach((t,ind)=>{
          if(typeof t=== undefined){
            props.data=props.data.slice(ind)
          }
        })
        
        // function to render path element with D3's General Update Pattern
        function createLine(dataIn,strokeColor,strokeWidth){ 
          console.log("creating line ", strokeColor);
            svg
                .selectAll(".line") // get all "existing" lines in svg
                //   .clone()
                
                .data(dataIn) // sync them with our data
                .join("path") // create a new "path" for new pieces of data (if needed)

                // everything after .join() is applied to every "new" and "existing" element
                .attr("class", "line") // attach class (important for updating)
                //   .attr("stroke", "green") // styling
                .attr("stroke", strokeColor)
                .attr("stroke-width", strokeWidth)
                .attr("d", lineGen); // shape and form of our line!
            return svg; 
        }

        // function to render new path element with D3's General Update Pattern
        function createNewLine(dataIn,strokeColor,strokeWidth){ 
          console.log("creating NEW line ", strokeColor);
            svg
                .selectAll(".line") // get all "existing" lines in svg
                  .clone()
                  .attr("id","clone")
            svg
                .selectAll(".line#clone")
                .data(dataIn) // sync them with our data
                .join("path") // create a new "path" for new pieces of data (if needed)

                // everything after .join() is applied to every "new" and "existing" element
                .attr("class", "line") // attach class (important for updating)
                //   .attr("stroke", "green") // styling
                .attr("stroke", strokeColor)
                .attr("stroke-width", strokeWidth)
                .attr("d", lineGen); // shape and form of our line!
            
            return svg; 
        }
        
        console.log('ugh', JSON.parse(JSON.stringify(props.secondTextRef)));
        if(typeof JSON.parse(JSON.stringify(props.data[0])) === "number"){
            if(props.graphstate > 0 ){
              console.log("0", props.color0);
              console.log("1", props.color1);
              console.log("2", props.color2);
              console.log("X", props.colorX);
              
              console.log("Y", props.colorY);
              if(props.color0 !== props.color1 && props.color1 === props.color2){
                console.log("are we creating new line?")
                createLine([props.data], props.color0,1.5);
              } else if (props.color1 !== props.color2 && props.color2 === props.color3) {
                createNewLine([props.data], props.color1,1.5);
              } else if (props.color2 !== props.color3 && props.color3 === "#00bd7e") {
                createNewLine([props.data], props.color2,1.5);
              } else {
               //createLine([props.data], props.color0,1.5);
               // createNewLine([props.data], props.color3,1.5);
              }
            } else {
              if(JSON.parse(JSON.stringify(props.secondTextRef))===true){
                createNewLine([props.data], 'yellow',1.5);
              } else {
                createLine([props.data],props.color0,1.5);
              }
            
            }
        } else {
            console.warn("we shouldn't be gettting here! / check data")
            createLine([props.data], 'pink',3);
        }

        function createXAxis(color){
          // render axes with help of scales
          // (we let Vue render our axis-containers and let D3 populate the elements inside it)
          const xAxis = axisBottom(xScale);
          svg
            .select(".x-axis")
            .style("transform", `translateY(${height}px)`) // position on the bottom
            .style("color", color)
            .call(xAxis);
          
          return svg;
        }
        createXAxis(props.colorX);


        function createYAxis(color){

          const yAxis = axisLeft(yScale);
          svg.select(".y-axis")
              .style("color", color)
              .call(yAxis);
          console.log("*** SVG y axis *** ", svg);
          return svg
        }
     
        createYAxis(props.colorY);

        svg.on('mouseover', function(d) {
          let selectedIndexX = Math.floor((d.offsetX/width) * props.data.length);
         
          if(!selectedIndexX ){
            return;
          } else {
             console.log("HOW LONG IS PROPS DATA? ", selectedIndexX);
            if(!selectedIndexX){
              return;
            }
            console.log(d)
            this.selectedIndexX = selectedIndexX;
            console.log("errr wtf??? ", this.selectedIndexX);
         
            if(selectedIndexX > 0){
           
              console.log("emitting the selected location ", selectedIndexX)
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
  <!-- $emit('mouseover') -->
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
    <span v-if="this.xAxisLabel" id="yAxisLabel">{{this.xAxisLabel}}</span>
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
#yAxisLabel {
    transform: rotate(270DEG);
    Z-INDEX: 9999;
    POSITION: FIXED;
    COLOR: WHITE;
    TOP: 44%;
    left: -50px;
}
</style>