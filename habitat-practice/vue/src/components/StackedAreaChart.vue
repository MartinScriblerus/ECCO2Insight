
<template>
  <div id="stackedAreaWrapper">
  <h1>{{paths.area}}</h1>
  <h1>{{paths.line}}</h1>
  <h1>{{paths.selector}}</h1>
    <svg @mousemove="mouseover" :width="width" :height="height">
      <g :style="{transform: `translate(${margin.left}px, ${margin.top}px)`}">
        <path class="area" :d="paths.area" />
        <path class="line" :d="paths.line" />
        <path class="selector" :d="paths.selector" />
      </g>
    </svg>
  </div>
</template>

<script allowJs="true">
/* globals window, requestAnimationFrame */
import * as d3 from 'd3';

import TWEEN from '@tweenjs/tween.js';
const props = {
  data: {
    type: Array,
    default: () => [1,2,3,4,5,6,7,8,9,10],
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
  ceil: {
    type: Number,
    default: 100,
  },
};
export default {
  name: 'StackedAreaChart',
  props,
  data() {
    return {
      width: 0,
      height: 0,
      paths: {
        area: '',
        line: '',
        selector: '',
      },
      lastHoverPoint: {},
      scaled: {
        x: null,
        y: null,
      },
      animatedData: [],
      points: [],
    };
  },
  computed: {
    padded() {
      const width = this.width - this.margin.left - this.margin.right;
      const height = this.height - this.margin.top - this.margin.bottom;
      console.log(`width: ${width} / height ${height}`);
      return { width, height };
    },
  },
  mounted() {
    window.addEventListener('resize', this.onResize);
    this.onResize();
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  },
  watch: {
    data: function dataChanged(newData, oldData) {
      this.tweenData(newData, oldData);
    },
    width: function widthChanged() {
      this.initialize();
      this.update();
    },
  },
  methods: {
    getScales() {
      const x = d3.scaleTime().range([0, 430]);
      const y = d3.scaleLinear().range([210, 0]);
      d3.axisLeft().scale(x);
      d3.axisBottom().scale(y);
      
      x.domain(d3.extent(this.data, (d, i) => i));
      y.domain([0, d3.max(this.data, d => d)]);

      return { x, y };
    },
    calculatePath() {
      const scale = this.getScales();
      const path = d3.line()
        .x((d, i) => scale.x(i))
        .y(d => scale.y(d));
      console.log('PATH VALUE: ', path);
      this.line = path(this.data);
      console.log("LINE VALUE: ", this.line);
      console.log("GOING INSANE ", this.paths);
    },
    onResize() {
      this.width = this.$el.offsetWidth;
      this.height = this.$el.offsetHeight;
    },
    createArea: d3.area().x(d => d.x).y0(d => d.max).y1(d => d.y),
    createLine: d3.line().x(d => d.x).y(d => d.y),
    createValueSelector: d3.area().x(d => d.x).y0(d => d.max).y1(0),
    initialize() {
      this.scaled.x = d3.scaleLinear().range([0, this.padded.width]);
      this.scaled.y = d3.scaleLinear().range([this.padded.height, 0]);
      d3.axisLeft().scale(this.scaled.x);
      d3.axisBottom().scale(this.scaled.y);
    },
    
    tweenData(newData, oldData) {
      const vm = this;
      function animate(time) {
        window.requestAnimationFrame(animate);
        TWEEN.update(time);
      }
      new TWEEN.Tween(oldData)
        .easing(TWEEN.Easing.Quadratic.Out)
        .to(newData, 500)
        .onUpdate(function onUpdate() {
          vm.animatedData = this;
          console.log("anim data: ", this)
          vm.update();
        })
        .start();
      animate();
    },
    update() {
        console.log("UPDATE: ", this.data);
        
      this.scaled.x.domain(d3.extent(this.data, (d, i) => i));
      this.scaled.y.domain([0, this.ceil]);
      this.points = [];
      
    console.log("general this: ", this);
  
    //   if( this.animatedData){


    //   } else {
    //     console.log("??????? ", this.data);
        // for (const [i, d] of this.animatedData.entries()) {
        for (const [i, d] of this.data.entries()) {
            console.log("THIS IS D: ", d);
            this.points.push({
                x: this.scaled.x(i),
                y: this.scaled.y(d),
                max: this.height,
            });
            console.log("POINTS: ", this.points);
        }
    //   }



      this.paths.area = this.createArea(this.points);
      this.paths.line = this.createLine(this.points);
      console.log("PATHS: ", this.paths.line);
    },
    mouseover({ offsetX }) {
      if (this.points.length > 0) {
        const x = offsetX - this.margin.left;
        const closestPoint = this.getClosestPoint(x);
        if (this.lastHoverPoint.index !== closestPoint.index) {
          const point = this.points[closestPoint.index];
          this.paths.selector = this.createValueSelector([point]);
          console.log('closest point: ', this.data[closestPoint.index]);
          this.$emit('select', this.data[closestPoint.index]);
          this.lastHoverPoint = closestPoint;
        }
      }
    },
    getClosestPoint(x) {
      return this.points
        .map((point, index) => ({ x:
          point.x,
          diff: Math.abs(point.x - x),
          index,
        }))
        .reduce((memo, val) => (memo.diff < val.diff ? memo : val));
    },
  },
};
</script>
<style lang="css" scoped>
svg{
  margin: 25px;
}
path{
  fill: none;
  stroke: #76BF8A;
  stroke-width: 3px;
}
#stackedAreaWrapper {
    z-index:9999;
}

</style>