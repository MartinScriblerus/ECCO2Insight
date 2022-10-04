<template>
  <svg :width="width" :height="height">
    <g style="transform: translate(0, 10px)">
    
      <path :d="line" />
    </g>
  </svg>
</template>

<script allowJs="true">
import * as d3 from 'd3';
import TWEEN from '@tweenjs/tween.js';
const props = {
  data: {
    type: Array,
    default: () => [],
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
  ceil: {
    type: Number,
    default: 100,
  },
};


export default {
  name: 'LineChart',
  props,
  data() {
    //console.log("inner what is this: ", this);
    return {
      data: [99, 71, 78, 25, 36, 92],
      line: '',


      width: 500,
      height: 500,
    //   paths: {
    //     area: '',
    //     line: '',
    //     selector: '',
    //   },
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
      //console.log(`width: ${width} / height ${height}`);
      return { width, height };
    },
  },
  mounted() {
    this.calculatePath();
    window.addEventListener('resize', this.onResize);
    this.onResize();
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  },
  watch: {
    data: function dataChanged(newData, oldData) {
    //   this.tweenData(newData, oldData);
        console.log(`old data: ${oldData} / new data: ${newData}`);
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
      this.line = path(this.data);
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
    }  
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
</style>