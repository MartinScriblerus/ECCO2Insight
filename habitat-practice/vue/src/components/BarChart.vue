<template>
  <div id="generalChartWrapper" ref="resizeRef">
    <svg ref="svgRef">
      <g class="x-axis" />
      <g class="y-axis" />
    </svg>
  </div>
</template>

<script>
import { onMounted, ref, watchEffect } from "vue";
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
  props: ["data"],
  setup(props) {
    // create ref to pass to D3 for DOM manipulation
    const svgRef = ref(null);

    // this creates another ref to observe resizing, 
    // which we will attach to a DIV,
    // since observing SVGs with the ResizeObserver API doesn't work properly
    const { resizeRef, resizeState } = useResizeObserver();

    onMounted(() => {
      // pass ref with DOM element to D3, when mounted (DOM available)
      const svg = select(svgRef.value);

      // whenever any dependencies (like data, resizeState) change, call this!
      watchEffect(() => {
        const { width, height } = resizeState.dimensions;
        console.log('does resize state work?? ', resizeState);
        // scales: map index / data values to pixel values on x-axis / y-axis
        const xScale = scaleLinear()
          .domain([0, props.data.length - 1]) // input values...
          .range([0, width]); // ... output values

        const yScale = scaleLinear()
          .domain([min(props.data), max(props.data)]) // input values...
          .range([height, 0]); // ... output values

        // line generator: D3 method to transform an array of values to data points ("d") for a path element
        const lineGen = line()
          .curve(curveBasis)
          .x((value, index) => xScale(index))
          .y((value) => yScale(value));

        // render path element with D3's General Update Pattern
        svg
          .selectAll(".line") // get all "existing" lines in svg
          .data([props.data]) // sync them with our data
          .join("path") // create a new "path" for new pieces of data (if needed)
          .append("defs").append("clipPath")
          .attr("id", "clip")
          .append("rect")
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
        // console.log("*** SVG *** ", svg);
        // console.log("* X AXIS * ", xAxis);
        // console.log("* Y AXIS * ", yAxis);
      });
    });
    // console.log(" ***** SVG REF ***** ", svgRef);
    // return refs to make them available in template
    return { svgRef, resizeRef };
  },
};
</script>
<style>
#generalChartWrapper {
  display: flex;
  height: 100%;
  z-index: 10;
}
.area {
  fill: steelblue;
  clip-path: url(#clip);
}
</style>