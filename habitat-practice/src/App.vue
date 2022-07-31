<script lang="ts">
//import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'

import { ref, onMounted, reactive } from 'vue'

const scrape:any = {
  basicData:Object,
  letterData:Object
};
scrape.basicData = scrape.basicData || {};
scrape.letterData = scrape.letterData || {};

export default {
  props: {
    data: {
      type: Object,
      default: () => ({}),
    },
    loaded: {
      type: Boolean,
      default: () => (false),
    },
    authorSearch: {
      type: String,
      default: () => (''),
    },
    titleSearch: {
      type: String,
      default: () => (''),
    },
    yearSearchBegin: {
      type: String,
      default: () => (''),
    },
    yearSearchEnd: {
      type: String,
      default: () => {''}
    },
    letterFilter: {
      type: String,
      default: () => (''),
    }
  },
  data(this:any) {
    return {
        currentState: false,
        comparing:false
    }
  },
  computed: {
    isActive(this:any) {
        return this.currentState;
    },
    isComparing(this:any) {
        return this.comparing;
    },
    checkedValue: {
        get(this:any) {
            return this.currentState;
        },
        set(this:any,newValue:any) {
            this.currentState = newValue;
        }
    },
    checkedValueComparison: {
        get(this:any) {
            return this.comparing;
        },
        set(this:any,newValue:any) {
            this.comparing = newValue;
        }
    }
  },
  components: {
    TheWelcome
  },
  // data() {
  //   return scrape.letterData
  // },
  setup(props:any) { 
    const state:any = reactive({
      data: null,
      loaded: null,
    });
    props = state; 
    onMounted(async () => {
      const response = await fetch("http://localhost:5000");
      state.data = await response.json();
      //state.data = state.data.filter(item => item.author.indexOf(props.authorSearch) > -1);    
      console.log("state data: ", state.data);
      
      const totalVuePackages = await state.data;
      if(state && state.data){
        state.loaded = true;
        let jumbotron = document.getElementById("jumbotron");
        let searchForms = document.getElementById("headerDiv");
        let main = document.getElementById("main");
        if(jumbotron){
          jumbotron.classList.remove("intro-cover");
        }
        
        setTimeout(()=>{
          if(main){
            main.style.visibility = "visible";
          }
          if(searchForms){
            searchForms.style.visibility = "visible";
            if(searchForms.classList.contains("noDisplay")){
              searchForms.classList.remove("noDisplay");
            }
          }
        }, 1000);
        clearTimeout();
      }   
    });

    props = state;

    return {
    state,
    props
    };
  }, 
  methods: {
    scrapeBasic: async function (this:any) {
      scrape.basicData = await fetch('http://localhost:5000/scraper', {
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify({titleSearch: this.props.titleSearch, authorSearch: this.props.authorSearch, publishedSearch: this.props.yearSearch})
      }); 
      console.log("BASIC_DAT!A: ", scrape.basicData);
    },
    handleKeyUpAuthor: async function (this: any) {
      this.state.data = {}
      console.log("here is author search query: ", this.props.authorSearch);

      scrape.basicData = await fetch('http://localhost:5000/scraper_author_filter', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({author_filter: this.props.authorSearch})
      }).then(response => response.json()).then(result => {
        if(result.length){
          let arr = [];
          for(let i = 0; i < result.length; i++){
            JSON.parse(result[i]).published = JSON.parse(result[i]).published.slice(0,1);
            arr.push(JSON.parse(result[i]));
          }
          scrape.basicData = arr;
          return scrape.basicData;
        } else {
          return null;
        }
        }).catch(error => {
          console.log('Error:', error);
        }); 
        this.state.data = scrape.basicData
        return this.state;
    },
    handleKeyUpTitle: async function (this:any) {
      this.state.data = {}
      console.log("here is author search query: ", this.props.titleSearch);

      scrape.basicData = await fetch('http://localhost:5000/scraper_title_filter', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({title_filter: this.props.titleSearch})
      }).then(response => response.json()).then(result => {
              if(result.length){
                let arr = [];
                for(let i = 0; i < result.length; i++){
                  
                  // console.log("efd ois i ", result[i]);
                  arr.push(JSON.parse(result[i]));
                }

                scrape.basicData = arr;
                return scrape.basicData;
              } else {
                return null;
              }

             }).catch(error => {
              console.log('Error:', error);
             }); 
        this.state.data = scrape.basicData
        return this.state;
    },
    handleKeyUpYear: async function (this:any) {
      console.log("here is year search begin query: ", this.props.yearSearchBegin);
      console.log("here is year search end query: ", this.props.yearSearchEnd);

      this.state.data = {}
  
      let yearBegin = this.props.yearSearchBegin;
      let yearEnd = this.props.yearSearchEnd;
      console.log(`begin ${yearBegin} // end ${yearEnd}`)
      if(yearBegin && yearEnd){
      scrape.basicData = await fetch('http://localhost:5000/scraper_year_filter', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({yearBegin: yearBegin, yearEnd: yearEnd})
      }).then(response => response.json()).then(result => {
              console.log("RESULT ", result);
              let arr = [];
              for(let i = 0; i < result.length; i++){
                
                // console.log("efd ois i ", result[i]);
                arr.push(JSON.parse(result[i]));
              }

              scrape.basicData = arr;
              return scrape.basicData;

             }).catch(error => {
              console.log('Error:', error);
             }); 
        this.state.data = scrape.basicData
        return this.state;
      } else {
        return null;
      }
    },
    handleKeyUpLetter: async function(this:any,letter:String) {
      this.state.data = {}
      console.log("the letter is... ", letter);
      this.props.letterFilter = letter;
      scrape.basicData = await fetch('http://localhost:5000/scraper_letter_filter', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({letter: letter, filter_mode: this.currentState})
      }).then(response => response.json()).then(result => {
              
              let arr = [];
              for(let i = 0; i < result.length; i++){
                
                // console.log("efd ois i ", result[i]);
                arr.push(JSON.parse(result[i]));
              }

              scrape.basicData = arr;
              return scrape.basicData;

             }).catch(error => {
              console.log('Error:', error);
             }); 
        this.state.data = scrape.basicData
        return this.state;
 
    },
  },

}

</script>

<template>
  <h1 id="jumbotron" class="jumbotron intro-cover">ECCO Insights</h1>
  <header id="headerDiv">



    <!-- <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" /> -->
    <!-- <a id="rowanButton" href="https://www.youtube.com/watch?v=vRulmmH5G4U" width="125" height="125">CLICK ME ROWAN!!!</a> -->
    <div class="wrapper-outer">
      <div class="wrapper">

        <div class="inputsRowWrapper">
          <div id="titleAuthorInputWrapper">
            <span class="label-wrap">
              <input id="titleSearch" @keyup='handleKeyUpTitle' v-model='props.titleSearch'/>
              <label class="green" for="titleSearch">Title</label>
            </span>
            <span class="label-wrap">
              <input id="authorSearch" @keyup='handleKeyUpAuthor' v-model='props.authorSearch'/>
              <label class="green" for="authorSearch">Author</label>
            </span>
        </div>

        <div id="yearsBetweenInputWrapper">

            <span class="label-wrap">
              <input id="yearSearch" @keyup='handleKeyUpYear' v-model='props.yearSearchBegin'/>
              <label class="green" for="yearSearch">Begin</label>
            </span>
            <span class="label-wrap">
              <input id="yearSearch" @keyup='handleKeyUpYear' v-model='props.yearSearchEnd'/>
              <label class="green" for="yearSearch">End</label>
            </span>
          
        </div>
      </div>
      <div id="letter-wrapper">
        <div class="toggle-wrapper">
          <div id="letterFilterToggleWrapper">
            <label for="toggle_button" class="switch">
              <input type="checkbox" id="toggle_button" v-model="checkedValue">
              <div class="slider round"></div>
              <span class="toggle-text" v-if="isActive">Filter Authors</span>
              <span class="toggle-text" v-if="! isActive">Filter Titles</span>
            </label>
          </div>

          <!-- <div id="searchModeToggleWrapper">
            <label for="search_mode_toggle_button" class="switch">
              <input type="checkbox" id="search_mode_toggle_button" v-model="checkedValueComparison">
              <div class="slider round"></div>
              <span class="toggle-text" v-if="isComparing">Single Text</span>
              <span class="toggle-text" v-if="! isComparing">Comparisons</span>
            </label>
          </div> -->
        </div>
        <div id="alphabetWrapper" class="wrapper green">
          <span class="letterClick green" v-on:click="handleKeyUpLetter('A')">A</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('B')">B</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('C')">C</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('D')">D</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('E')">E</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('F')">F</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('G')">G</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('H')">H</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('I')">I</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('J')">J</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('K')">K</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('L')">L</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('M')">M</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('N')">N</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('O')">O</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('P')">P</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('Q')">Q</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('R')">R</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('S')">S</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('T')">T</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('U')">U</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('V')">V</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('W')">W</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('X')">X</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('Y')">Y</span>
          <span class="letterClick green" v-on:click="handleKeyUpLetter('Z')">Z</span>
        </div>
      </div>


      </div>       
      <!-- <button class="green header" v-on:click="scrapeBasic">Reset DB</button> -->
      
    </div>
  </header>

  <main id="main">
  
    <TheWelcome :items="state.data" />
  </main>
</template>

<style>
@import './assets/base.css';


#app {
  /*max-width: 1280px;*/
  margin: 0 auto;
  padding: 2%;
  grid-template-columns: 1fr 1fr;
  font-weight: normal;
  position:absolute;
  top:0px;
  left:0px;
  max-width: 100vw;
}

/* Hide scrollbar for Chrome, Safari and Opera */
.scrollbar-hidden::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge add Firefox */
.scrollbar-hidden {
  -ms-overflow-style: none;
  scrollbar-width: none; /* Firefox */
}

header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

a,
.green {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
  text-align:center;
}

.letterClick {
    background: #181818;
    padding-left: 10px;
    padding-right: 8px;
    margin-bottom: 0px;
    font-size: 22px;
}

.letterClick:hover {
  background-color: hsla(160, 100%, 37%, 1);
  color: #f6f6f6;
}

button {
  background: #181818;
  font-weight: 600;
  font-size: 18px;
  cursor:pointer;
}

input {
  margin-top: 8px;
  background: rgba(255,255,255,0.94);
  margin-left: 8px;
  margin-right: 8px;
  height: 32px;
  border-radius: 4px;
}

#main {
  max-height: 100vh;
  overflow-y: scroll;
  top:52px;
  visibility: hidden;
}

#headerDiv {
  visibility:hidden;

  /*height:100vh;*/
}

.toggle__button {
    vertical-align: middle;
    user-select: none;
    cursor: pointer;
    color: hsla(160, 100%, 37%, 1);
    background: rgba(255,255,255,0.78);
}
.toggle__button input[type="checkbox"] {
    opacity: 0;
    position: absolute;
    width: 1px;
    height: 1px;
    color: hsla(160, 100%, 37%, 1);
    background: rgba(255,255,255,0.78);
    background-color: rgba(255,255,255,0.78);
    
}
.toggle__button .toggle__switch {
    display:inline-block;
    height:12px;
    border-radius:6px;
    width:40px;
    background: hsla(160, 100%, 37%, 1);
    box-shadow: inset 0 0 1px hsla(160, 100%, 37%, 1);
    position:relative;
    margin-left: 10px;
    transition: all .25s;
    color:red;
}

.toggle__button .toggle__switch::after, 
.toggle__button .toggle__switch::before {
    content: "";
    position: absolute;
    display: block;
    height: 18px;
    width: 18px;
    border-radius: 50%;
    left: 0;
    top: -3px;
    transform: translateX(0);
    transition: all .25s cubic-bezier(.5, -.6, .5, 1.6);
    background: rgba(255,255,255,0.78);
}

.toggle__button .toggle__switch::after {
    box-shadow: 0 0 1px #666;
    background-color: rgba(255,255,255,0.78);
}
.toggle__button .toggle__switch::before {
    background: hsla(160, 100%, 37%, 1);
    color: hsla(160, 100%, 37%, 1);
    box-shadow: 0 0 0 3px rgba(0,0,0,0.1);
    background: rgba(255,255,255,0.78);
    opacity:0;
}

input[type="checkbox"] {
  background: rgba(255,255,255,0.78);
}

#letter-wrapper {
  border: 1px solid rgba(255,255,255,0.78);
  display:flex;
  flex-direction:row;
  min-height:108px;
}

#titleAuthorInputWrapper {
    display: flex;
    flex-direction: column;
    width: 64%;
    padding-top: 20px;
    padding-bottom: 20px;
}
#titleAuthorInputWrapper > .label-wrap {
  width:100%;
}

#yearsBetweenInputWrapper > .label-wrap {
  text-align: center;
  height: 100%;
  justify-content: center;
}

#yearsBetweenInputWrapper {
  display:flex;
  flex-direction:row;
  float: right;
  width: 40%;
}

.inputsRowWrapper {
  flex-direction: row;
  display:inline-flex;
  overflow:auto;
  width:100%;
  padding-left:0%;
  padding-right:0%;
}

#alphabetWrapper {
  overflow-wrap:normal;
  overflow-x:scroll;
  padding-left:8%;
  overflow-wrap:break-word;
}

.wrapper-outer {
  border: 1px solid rgba(255,255,255,0.78);

  width: 100%;
}

.jumbotron {
width: 100%;
  position: fixed;
  z-index: 40;
  height: 68px;
  padding-left: 40px;
  font-size: 48px;
  font-weight: 100;
  top: 0px;
  left: 0px;
  background: rgba(0, 0, 0, 1);
  transition: height 1s ease-in;
  pointer-events: none;
} 

.intro-cover {
  height: 100vh;
  width:100vw;
  background: #181818;
  color: rgba(255,255,255,1);
  z-index:100;
  transition: height 3s ease-in;
}

#letterFilterToggleWrapper, #searchModeToggleWrapper {
  min-width: 16%;
  height:50%;
  white-space:nowrap
}
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  top: 32px;
  left: 8px;
}

.switch input {
  display: none;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: hsla(160, 100%, 37%, 1);
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: #101010;
}

input:focus + .slider {
  box-shadow: 0 0 1px #101010;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
.toggle-text {
  top:32px;
  position:absolute;
  padding-left:4px;
}

/*
.toggle-wrapper {
  width: 50%
}
*/

@media (hover: hover) {
  a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
    cursor:pointer;
  }
}

  .letterClick {
    line-height:2;
  }

@media (max-width: 900px) {

  #main {
    top:80px;
  }
  #headerDiv.noDisplay {
    display: none;
  }
  #headerDiv {
    top: 72px;
  }
  .toggle-wrapper {
    width: 12%;
  }
  .inputsRowWrapper{
    margin-top:24px;
    margin-bottom:24px;
    padding-left:10%;
    padding-right:10%;
  }
  input {
    width:64%;
  }
  #toggle_button {
    max-width: 12px;
  }
  
  /*.switch {
    top:12px;
  }*/

  #titleAuthorInputWrapper {
    padding-top: 0px;
    padding-bottom: 0px;
  }

  .modal.searching {
    width: 100vw;
  }
  
}







@media (min-width: 900px) {
  body {
    display: flex;
    place-items: center;
    overflow-y:hidden;
  }

  #app {
    display: grid;
    /* grid-template-columns: 1fr 1fr;
    padding: 0 2rem; */
  }

  header {
    place-items: center;
    padding-right: calc(var(--section-gap) / 6);
    top:72px;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
    overflow: auto;


  }

  #letterWrapper {
    padding-bottom: 32px;
    overflow-wrap: normal;
    flex-direction:column;
    padding-right: 8px;
  }

  .wrapper-outer {
    display: flex;
    flex-direction: column;
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  .custom-control-input:checked ~ .custom-control-label::before, .custom-control-label::after {
    color: #fff;
    border-color:hsla(160, 100%, 37%, 0.2);
    background-color:hsla(160, 100%, 37%, 0.2);
  }

  .label-wrap {
    display: flex;
    flex-direction: column;
    width: 46%;
    padding-right: 0%;
    padding-left: 4%;
  }
}
</style>
