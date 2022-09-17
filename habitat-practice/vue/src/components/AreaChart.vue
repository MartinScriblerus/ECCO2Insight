<script>
import { onMounted, ref, watchEffect } from "vue";
import * as d3 from 'd3';
import {
  select,
  line,
  scaleLinear,
  min,
  max,
  curveBasis,
  axisBottom,
  axisLeft,
} from "d3";
// import useResizeObserver from "@/use/resizeObserver";

export default {
  name: "ResponsiveLineChart",
  props: ["data","newData","mode","tooltipmsg"],
    watch: { 
      tooltipmsg: {
        deep: true,
        handler: function(newVal, oldVal){
           console.log('Prop changed: ', newVal, ' | was: ', oldVal)
            console.log("YOYOYOYO ENTITY ARR", JSON.parse(JSON.stringify(newVal)).sentenceGrammarArray);
            console.log("YOYOYOYO GRAMMAR ARR ", JSON.parse(JSON.stringify(newVal)).sent);
            let tooltip = document.getElementById("tooltipInner");
            if(tooltip){
              tooltip.innerHTML = `
              <div id="sentimentDisplay">
            
                <h4 class="HUD-half-div">Comp: ${JSON.parse(JSON.stringify(newVal)).sentimentCompound}</h1>
                <h4 class="HUD-half-div">Neg: ${JSON.parse(JSON.stringify(newVal)).sentimentNegative}</h1>
                <h4 class="HUD-half-div">Neu: ${JSON.parse(JSON.stringify(newVal)).sentimentNeutral}</h1>
                <h4 class="HUD-half-div">Pos: ${JSON.parse(JSON.stringify(newVal)).sentimentPositive}</h1>
              </div>
          
              <div id="topicListWrapper">
                ${this.entityArr.toString()}
              </div> 
              `
            }
            let topicWrapper = document.getElementById("topicListWrapper");
            console.log(JSON.parse(JSON.stringify(JSON.parse(JSON.stringify(newVal)).entityArrays)));
            JSON.parse(JSON.stringify(JSON.parse(JSON.stringify(newVal)).entityArrays)).forEach(i=>topicWrapper.append(`${i[0]}\n`))
        }
      }
    },
  emits:["selected"],
  data(){
    return {
      show: false,
      clientX: 0,
      clientY: 0,
      closestPoint: null,
      entityArr:[]
    };
  },
  setup(props,{emit}) {
      const points = ref();
      points.value = [];
      const scaled = ref();
     
      
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

  
    
    console.log("PROPS DATA IN AREA COMPONENT: ", props.data);
    
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
        // tooltipInner.value.innerText = props.tooltipMsg;
        // document.getElementById('svgId').childNodes.forEach(c=>{
        //   console.log("SVG CHILD NODE: ", c);
        // })
        console.log("RESIZEE STATE: ", resizeState);
        const { width, height } = resizeState.dimensions;
            console.log("WIDTH: ", width);
            scaled.value.x = d3.scaleLinear().range([0, width]);
            scaled.value.y = d3.scaleLinear().range([height, 0]);
            d3.axisLeft().scale(scaled.value.x);
            d3.axisBottom().scale(scaled.value.y);
            console.log("SCALED? ", scaled.value);
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
        const lineGen = line()
          .curve(curveBasis)
          .x((value, index) => xScale(index))
          .y((value) => yScale(value));

        //console.log("CRIKEY: ", svg.attr('d'))
        console.log("AAAAA WHAT IS PROPS DATA TYPE? ", Object.keys(props.data));
        Object.values(props.data).forEach((t,ind)=>{
          if(typeof t=== undefined){
          props.data=props.data.slice(ind)
          }
        })
        // render path element with D3's General Update Pattern
        svg
          .selectAll(".line") // get all "existing" lines in svg
          .data([props.data]) // sync them with our data
          .join("path") // create a new "path" for new pieces of data (if needed)

          // everything after .join() is applied to every "new" and "existing" element
          .attr("class", "line") // attach class (important for updating)
          .attr("stroke", "green") // styling
          .attr("d", lineGen); // shape and form of our line!
    
        // render axes with help of scales
        // (we let Vue render our axis-containers and let D3 populate the elements inside it)
        const xAxis = axisBottom(xScale);
        svg
          .select(".x-axis")
          .style("transform", `translateY(${height}px)`) // position on the bottom
          .call(xAxis);

        const yAxis = axisLeft(yScale);
        svg.select(".y-axis").call(yAxis);
        console.log("*** SVG *** ", svg);
     
        svg.on('mouseover', function(d) {
          let selectedIndexX = Math.floor((d.offsetX/width) * props.data.length);
          if(!selectedIndexX ){
            return;
          } else {
            console.log(typeof d)
            this.selectedIndexX = selectedIndexX || 0;
            console.log(this.selectedIndexX);
            emit('selected',this.selectedIndexX);
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
        v-if="show"
        @mouseout="show = false"
      >
    
        <div id="tooltipInner" ref="tooltipInner">
        
        </div>

    </div>
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
  margin-left: 44px;
  margin-right: 12px;
  top: -42px;
  pointer-events: all;
}
#svgId {
  background: rgba(0,0,0,0.98);
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
}
#tooltipInner {
  width: 100%;
  height: 80px;
}
.HUD-half-div {
  width:23%;
  min-width:23%;
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