<script lang="ts">
  //import HelloWorld from './components/HelloWorld.vue'
  import TheWelcome from './components/TheWelcome.vue'
  console.log("RITA! ", window);
  // @ts-ignore
  import { ref, onMounted, reactive } from 'vue'
  
  // import "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"
  // import "https://unpkg.com/rita"



  

// @ts-ignore
const scrape:any = {
  basicData:Object,
  letterData:Object
};
scrape.basicData = scrape.basicData || {};
scrape.letterData = scrape.letterData || {};
const textsToReturn : any = ref([])
const triedWikiExtension1 = ref(false);
const triedWikiExtension2 = ref(false);
const triedWikiExtension3 = ref(false);
const in_toc = ref(false)
export default {
  props: {
    data: {
      type: Object,
      default: () => ({}),
    },
    watch: [in_toc],
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
    const firstOne = ref(true);
    firstOne.value = true;
    const authorPortraits:any = ref([]);
    // authorPortraits.value = [];
    props = state; 
  
    function tryWikiExtension1(wikiString,firstName,lastName, title, published, bookId){

  
      wikiString = wikiString + "_(writer)";
      tryGetWikiImage(wikiString,firstName,lastName, title, published, bookId)
    }
    function tryWikiExtension2(wikiString,firstName,lastName, title, published, bookId){

      wikiString = wikiString + "_(poet)";
      tryGetWikiImage(wikiString,firstName,lastName, title, published, bookId)
    }
    function tryWikiExtension3(wikiString,firstName,lastName, title, published, bookId){
  
      wikiString = wikiString + "_(satirist)";
      tryGetWikiImage(wikiString,firstName,lastName, title, published, bookId)
    }

    async function tryGetWikiImage(wikiString,firstName,lastName, title, published, bookId){
      if(in_toc.value === true){
        return;
      }

      if(wikiString === "https://en.wikipedia.org/wiki/Robert_Herrick"){
        wikiString = "https://en.wikipedia.org/wiki/Robert_Herrick_(poet)";
      } 
      if(wikiString === "https://en.wikipedia.org/wiki/Charles_Churchill"){
        wikiString = "https://en.wikipedia.org/wiki/Charles_Churchill_(satirist)";
      }
      if(wikiString === "https://en.wikipedia.org/wiki/Cavendish_Newcastle"){
        wikiString = "https://en.wikipedia.org/wiki/Margaret_Cavendish,_Duchess_of_Newcastle-upon-Tyne";
      }
      if(wikiString === "https://en.wikipedia.org/wiki/Charles_Brown"){
        wikiString = " https://en.wikipedia.org/wiki/Charles_Brockden_Brown";
      }
      if(wikiString === "https://en.wikipedia.org/wiki/Home_Kames"){
        wikiString = "https://en.wikipedia.org/wiki/Henry_Home,_Lord_Kames"; 
      }
      if(wikiString === "https://en.wikipedia.org/wiki/Mrs_Leapor"){
        wikiString = "https://en.wikipedia.org/wiki/Mary_Leapor";
      }
      if(wikiString === "https://en.wikipedia.org/wiki/Nicholas_Rowe"){
        wikiString = "https://en.wikipedia.org/wiki/Nicholas_Rowe_(writer)";
      }
      if(wikiString === "https://en.wikipedia.org/wiki/Charlotte_Smith"){
        wikiString = "https://en.wikipedia.org/wiki/Charlotte_Smith_(writer)";
      }
      if(wikiString === "https://en.wikipedia.org/wiki/alMalik"){
        wikiString = "https://en.wikipedia.org/wiki/Ibn_Tufail";
      }
      if(wikiString === "https://en.wikipedia.org/wiki/"){
        wikiString = "https://en.wikipedia.org/wiki/Elizabeth_I";
      }
      if(wikiString === "https://en.wikipedia.org/wiki/I"){
        wikiString = "https://en.wikipedia.org/wiki/Charles_I_of_England";
      }
      if(wikiString === "https://en.wikipedia.org/wiki/W_Kenrick"){
        wikiString = "https://en.wikipedia.org/wiki/William_Kenrick_(writer)";
      }
   
      let getImg = await fetch('http://localhost:5000/tryWikiImg', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({"wikiString": wikiString, 'first_name': firstName, 'last_name': lastName, 'title':title, 'published':published, 'book_id': bookId})
      }).then(response => response.json()).then(result => {
        if(in_toc.value === true){
          return Promise.all([]);
        }
        
        let relevantImgEl = document.getElementById(`authorImage_${result['book_id']}`);
        
          if(result['img_possible'].length < 1){
            if(triedWikiExtension1.value === false){
              tryWikiExtension1(wikiString, firstName,lastName, title, published, bookId);
              triedWikiExtension1.value = true;
            }
            if(triedWikiExtension2.value === false){
              tryWikiExtension2(wikiString, firstName,lastName, title, published, bookId);
              triedWikiExtension2.value = true;
            }
            if(triedWikiExtension3.value === false){
              tryWikiExtension3(wikiString, firstName,lastName, title, published, bookId);
              triedWikiExtension3.value = true;
            }
            console.log("what was the problematic wiki string? ", wikiString);
          } 
          if(relevantImgEl && result && result['img_possible']){
            relevantImgEl['src'] = result['img_possible'][0];
          }
        if(result.length){

          return result;
        } else {
          return null;
        }
        }).catch(error => {
        
        });   
    }
    
    
    onMounted(async () => {
     

// ///
// // UNCOMMENT TO RE-SCRAPE DATABASE:
    // let test = await fetch('http://localhost:5000/scraper', {
    //   headers: {
    //     'Accept': 'application/json',
    //     'Content-Type': 'application/json'
    //   },
    //   method: "POST",
    //   body: JSON.stringify({"test": "test"})
    // }).then(response => response.json())
    // console.log(test);
// ///
      




      if (!localStorage.getItem("url"))
        localStorage.setItem("url", "");
      // this.localStorage = localStorage
      // localStorage.setItem("url", "hello");
      const response = await fetch("http://localhost:5000");

      state.data = await response.json();
      //state.data = state.data.filter(item => item.author.indexOf(props.authorSearch) > -1);    
      // console.log("state data: ", state.data);
   
      let rawAuthorName = JSON.parse(JSON.stringify(state.data));
      
      tryGetWikiURL(rawAuthorName)
      
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
        }, 10);
        clearTimeout();
      }   
    });

    async function tryGetWikiURL(rawAuthorName:any){
      // rawAuthorName.forEach((i)=>{ 
        for(let i = 0; i < rawAuthorName.length; i++){
          if(in_toc.value === true){
            // console.log("ENDING LOOP!");
            return;
          }
          let published = new Date(); 
          let first = '';
          let last = ''; 
          let title = ''; 
          let bookId = 0;
          let sub_url = ''
          let splitSpaces : any = []
          if(rawAuthorName[i]['author'].indexOf(' ')){
            splitSpaces = rawAuthorName[i]['author'].split(' ');
            let getFirst = false;
            // splitSpaces = splitSpaces.filter(i=>i.length > 2)
            for(let s = 0; s < splitSpaces.length; s++){          
              if(splitSpaces[s].length < 3){
                splitSpaces.slice(0,s);
              }
              if(s>2){
                splitSpaces.slice(s,2);
              }

              if(splitSpaces[s].indexOf(',') !== -1){
                let cutIndex = splitSpaces[s].indexOf(',');
                first = splitSpaces[s].slice(0,cutIndex) 
                if(s === 0){
                  last = splitSpaces[s].slice(0,cutIndex);
                  getFirst = true;
                }
              } else {
                if(getFirst){
                  getFirst = false;
                  first = splitSpaces[1]
                } else {
                }
              }
            }
            if(first.indexOf(',') !== -1 ){ 
              let cutIndex = first.indexOf(',');  
              first = first.slice(0,cutIndex);
            }
            if(last.indexOf(',') !== -1){ 
              let cutIndex = last.indexOf(',');  
              last = last.slice(0,cutIndex);
            }
            if(last === ''){
              sub_url = first;
            } else if(last === 'Ibn') {
              sub_url = last + '_' + first;
            } else {
              sub_url = first + '_' + last;
            }
          } 
          if(splitSpaces.length === 1){
            sub_url = splitSpaces[0]
          }

          published = rawAuthorName[i]['published'];
          title = rawAuthorName[i]['title']
          bookId = rawAuthorName[i]['id']

          let wikiString = 'https://en.wikipedia.org/wiki/' + sub_url;

            let images = await tryGetWikiImage(wikiString, first, last, title, published, bookId);

        }
    }

    props = state;

    return {
    state,
    props,
    tryGetWikiURL
    };
  }, 
  methods: {
    scrapeBasic: async function (this:any) {
      console.log("CALLING SCRAPER");
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
      this.state.data = {};
      if(this.props && this.props.authorSearch && this.props.authorSearch.length < 2){
        return null;
      }
      scrape.basicData = await fetch('http://localhost:5000/scraper_author_filter', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({author_filter: this.props.authorSearch})
      }).then(response => response.json()).then(result => {
        if(result.length){
          let arr  : Array<Object> = [];
          for(let i = 0; i < result.length; i++){
            JSON.parse(result[i]).published = JSON.parse(result[i]).published.slice(0,1);
            // tryGetWikiURL(scrape.basicData);
            arr.push(JSON.parse(result[i]));
          }
          scrape.basicData = arr;
 
          return scrape.basicData;
        } else {
          return null;
        }
        }).catch(error => {
          // console.log('Error:', error);
        }); 
        this.state.data = scrape.basicData

        return this.state;
    },
    in_toc_now: function(this:any) {
      in_toc.value = true;
    },
    handleKeyUpTitle: async function (this:any) {
      this.state.data = {};
      if(this.props.titleSearch.length < 2){
        return null;
      }
      scrape.basicData = await fetch('http://localhost:5000/scraper_title_filter', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({title_filter: this.props.titleSearch})
      }).then(response => response.json()).then(result => {
              if(result.length){
                let arr : Array<Object> = [];
                for(let i = 0; i < result.length; i++){
                  arr.push(JSON.parse(result[i]));
                }

                scrape.basicData = arr;
                
                // tryGetWikiURL(scrape.basicData);
                return scrape.basicData;
              } else {
                return null;
              }

             }).catch(error => {
              // console.log('Error:', error);
             }); 
        this.state.data = scrape.basicData
        return this.state;
    },
    handleKeyUpYear: async function (this:any) {
      // console.log("here is year search begin query: ", this.props.yearSearchBegin);
      // console.log("here is year search end query: ", this.props.yearSearchEnd);

      this.state.data = {}
  
      let yearBegin = this.props.yearSearchBegin;
      let yearEnd = this.props.yearSearchEnd;
      // console.log(`begin ${yearBegin} // end ${yearEnd}`)
      if(yearBegin && yearEnd){
      scrape.basicData = await fetch('http://localhost:5000/scraper_year_filter', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({yearBegin: yearBegin, yearEnd: yearEnd})
      }).then(response => response.json()).then(result => {
              // console.log("RESULT ", result);
              let arr : Array<Object> = [];
              for(let i = 0; i < result.length; i++){
                
                // console.log("efd ois i ", result[i]);
                arr.push(JSON.parse(result[i]));
              }

              scrape.basicData = arr;
              return scrape.basicData;

             }).catch(error => {
              // console.log('Error:', error);
             }); 
        this.state.data = scrape.basicData
        return this.state;
      } else {
        return null;
      }
    },
    letterFilterDisplay: function(){
      let getLetterFilter = document.getElementById("letter-wrapper");
      if(getLetterFilter && getLetterFilter.style.display !== "flex"){
        getLetterFilter.style.display = "flex";
      } else if(getLetterFilter){
        getLetterFilter.style.display = "none";
      } else {

      } 
    },
    fullTextSearchDisplay: async function(this:any,fullTextSearchInput:String){
      this.state.data = {};
      this.props.fullTextSearchInput = fullTextSearchInput;
      scrape.basicData = await fetch('http://localhost:5000/scraper_fulltext_search_new', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({fullTextSearchInput: "monkeys", filter_mode: this.currentState})
      }).then(response => response.json()).then(result => {
              console.log("RESULT OF FULLTEXT SEARCH IS... ", result);
              let arr : Array<Object> = [];
              for(let i = 0; i < result.length; i++){
                
                // console.log("efd ois i ", result[i]);
                arr.push(JSON.parse(result[i]));
              }

              scrape.basicData = arr;
              // console.log("FULL SEARCH RESULTS: ", arr);
              return scrape.basicData;

             }).catch(error => {
              // console.log('Error:', error);
             }); 
        this.state.data = scrape.basicData
        return this.state;
 
    },
    handleKeyUpLetter: async function(this:any,letter:String) {
      this.state.data = {}
      // console.log("the letter is... ", letter);
      this.props.letterFilter = letter;
      scrape.basicData = await fetch('http://localhost:5000/scraper_letter_filter', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({letter: letter, filter_mode: this.currentState})
      }).then(response => response.json()).then(result => {
              
              let arr : Array<Object> = [];
              for(let i = 0; i < result.length; i++){
                
                // console.log("efd ois i ", result[i]);
                arr.push(JSON.parse(result[i]));
              }

              scrape.basicData = arr;
              return scrape.basicData;

             }).catch(error => {
              // console.log('Error:', error);
             }); 
        this.state.data = scrape.basicData
        return this.state;
 
    },
    searchBasicOrchestrate: async function(this:any){
      // let authors = this.searchBasicAuthor();
      // let titles = this.searchBasicTitle();
      let titles : Array<String> = [];
      let authors : Array<String> = [];
      // console.log("TITLE SEARCH IN ORCHESTRATE: ",this.props.titleSearch);
      // console.log("AUTHOR SEARCH IN ORCHESTRATE: ",this.props.authorSearch);
      if(this.props && this.props.titleSearch){
        titles = await this.searchBasicTitle();
        textsToReturn.value.push(titles);
      } 
      if(this.props && this.props.authorSearch){
        authors = await this.searchBasicAuthor();
        textsToReturn.value.push(authors);
      } 

      // console.log("Texts to return ", textsToReturn.value); 
      return textsToReturn.value;
    },
    searchBasicTitle: async function(this:any){
      this.state.data = {}
      // console.log("here is title search query: ", this.props.titleSearch);
      if(this.props && this.props.titleSearch && this.props.titleSearch.length < 2){
        return null;
      }
      // console.log("ABOUT TO SEARCH FOR THIS TITLE: ", this.props.titleSearch);
      scrape.basicData = await fetch('http://localhost:5000/scraper_title_filter', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({title_filter: this.props.titleSearch})
      }).then(response => response.json()).then(result => {
              if(result.length){

                let arr : Array<Object> = [];
                for(let i = 0; i < result.length; i++){
                  if(this.props.yearSearchEnd){
                    // console.log("we've got to check year search end: ", this.props.yearSearchEnd)
                    if(parseInt(JSON.parse(result[i]).published) < parseInt(this.props.yearSearchEnd)){
                      // console.log("this result happened before search end: ", JSON.parse(result[i]))
                      if(arr.indexOf(JSON.parse(result[i])) !== -1){
                        arr.push(JSON.parse(result[i]));
                      }
                    } 
                    else {
                      console.log("out of year range: ", result[i])
                    }
                  } 
                  
                  else {
                    arr.push(JSON.parse(result[i]));
                  }
                }

                scrape.basicData = arr;
                
                // tryGetWikiURL(scrape.basicData);
                return scrape.basicData;
              } else {
                return null;
              }

             }).catch(error => {
              // console.log('Error:', error);
             }); 
        this.state.data = scrape.basicData
        return this.state;
    },
    searchBasicAuthor: async function(this:any){
      this.state.data = {}
      // console.log("here is author search query: ", this.props.authorSearch);
      if(this.props && this.props.authorSearch && (this.props.authorSearch.length < 2 )){
        // console.log("author search length too short --> returning")
        return null;
      }

      scrape.basicData = await fetch('http://localhost:5000/scraper_author_filter', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({author_filter: this.props.authorSearch})
      }).then(response => response.json()).then(result => {

        if(result.length){
          let arr  : Array<Object> = [];
          for(let i = 0; i < result.length; i++){
            JSON.parse(result[i]).published = JSON.parse(result[i]).published.slice(0,1);
            
            if(this.props.yearSearchBegin){
              if(parseInt(JSON.parse(result[i]).published) > parseInt(this.props.yearSearchBegin)){
                if(this.props.yearSearchEnd){
                  if(parseInt(JSON.parse(result[i]).published) < parseInt(this.props.yearSearchEnd)){
                    if(this.props.titleSearch && this.props.titleSearch.length > 1 && JSON.parse(result[i]).title.indexOf(this.props.titleSearch) !== -1){
                    arr.push(JSON.parse(result[i]));
                  } else if(this.props.titleSearch && this.props.titleSearch.length > 1 && JSON.parse(result[i]).title.indexOf(this.props.titleSearch) === -1) {
                    console.log("title mismatch")
                  } else {
                    arr.push(JSON.parse(result[i]));
                  }
                  } else {
                    console.log("out of year range: ", result[i])
                  }
                } else {
                  if(this.props.titleSearch && this.props.titleSearch.length > 1 && JSON.parse(result[i]).title.indexOf(this.props.titleSearch) !== -1){
                    arr.push(JSON.parse(result[i]));
                  } else if(this.props.titleSearch && this.props.titleSearch.length > 1 && JSON.parse(result[i]).title.indexOf(this.props.titleSearch) === -1) {
                    console.log("title mismatch")
                  } else {
                    arr.push(JSON.parse(result[i]));
                  }
                }
              } else {
                console.log("out of year range: ", result[i])
              }
            } else {
              if(this.props.yearSearchEnd){
                  if(parseInt(JSON.parse(result[i]).published) < parseInt(this.props.yearSearchEnd)){
                    if(this.props.titleSearch && this.props.titleSearch.length > 1 && JSON.parse(result[i]).title.indexOf(this.props.titleSearch) !== -1){
                    arr.push(JSON.parse(result[i]));
                  } else if(this.props.titleSearch && this.props.titleSearch.length > 1 && JSON.parse(result[i]).title.indexOf(this.props.titleSearch) === -1) {
                    console.log("title mismatch")
                  } else {
                    arr.push(JSON.parse(result[i]));
                  }
                } else {
                  console.log("out of year range: ", result[i])
                }
              } else {
                if(this.props.titleSearch && this.props.titleSearch.length > 1 && JSON.parse(result[i]).title.indexOf(this.props.titleSearch) !== -1){
                  arr.push(JSON.parse(result[i]));
                } else if(this.props.titleSearch && this.props.titleSearch.length > 1 && JSON.parse(result[i]).title.indexOf(this.props.titleSearch) === -1) {
                  console.log("title mismatch")
                } else {
                  arr.push(JSON.parse(result[i]));
                }
              }
            }
          }
          scrape.basicData = arr;

          this.tryGetWikiURL(arr)
          return scrape.basicData;
        } else {
          return null;
        }
        }).catch(error => {
          // console.log('Error:', error);
        }); 
        this.state.data = scrape.basicData

        return this.state;
    },
    // reset_opened_toc: function(this:any){
    //   opened_toc.value =
    // }
  },
  

}

</script>

<template>
  
  <h1 id="jumbotron" class="jumbotron intro-cover">TCP Data Viz</h1>
  <div id="searchFields" class="outer-row">
    <header id="headerDiv">
      <div id="headerWrapper"> 
        <div  id="letter-wrapper">
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
          <div class="toggle-wrapper">
            <div id="letterFilterToggleWrapper">
              <label for="toggle_button" class="switch">
                <input type="checkbox" id="toggle_button" v-model="checkedValue">
                <div class="slider round"></div>
                <span class="toggle-text" v-if="isActive">Search Authors</span>
                <span class="toggle-text" v-if="! isActive">Search Titles</span>
              </label>
            </div>
          
          
          
          </div>
      
        </div>
        <h3 id="mainTextSubheader">Main Text Subheader</h3>
        <p id="mainText">
          Lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem
          Lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem.

        </p>
      </div>
   


      <!-- <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" /> -->
      <!-- <a id="rowanButton" href="https://www.youtube.com/watch?v=vRulmmH5G4U" width="125" height="125">CLICK ME ROWAN!!!</a> -->

    </header>
    <div class="wrapper-outer">
      <div class="wrapper search">

        <div class="inputsRowWrapper">
          <div id="titleAuthorInputWrapper">
            <span class="label-wrap">
              <input id="titleSearch" placeholder="ex. King Lear" v-model='props.titleSearch' :maxlength="30"/>
              <label class="green" for="titleSearch">Title</label>
            </span>
            <span class="label-wrap">
              <input id="authorSearch" placeholder="ex. Shakespeare, William" v-model='props.authorSearch' :maxlength="30"/>
              <label class="green" for="authorSearch">Author</label>
            </span>
            <button id="searchBtnMain" class="green header" v-on:click="searchBasicOrchestrate">Search</button>
        </div>

        <div id="yearsBetweenInputWrapper">
          <div id="letterSearchBtnColumnWrap">
            <button class="green header" v-on:click="letterFilterDisplay">Letter Search</button>
            <button class="green header" disabled id="disableFullText" v-on:click="fullTextSearchDisplay">Full Text Search</button>
            <div id="yearsBetweenRowWrapper">
              <span class="label-wrap">
                <input id="yearSearch1" placeholder="1660" v-model='props.yearSearchBegin'/>
                <label class="green" for="yearSearch1">Begin</label>
              </span>
            
              <span class="label-wrap">
                <input id="yearSearch2" placeholder="1745" v-model='props.yearSearchEnd'/>
                <label class="green" for="yearSearch2">End</label>
              </span>
            </div>
          </div>
          
        </div>
      </div>
      </div>       
      <!-- <button class="green header" v-on:click="scrapeBasic">Reset DB</button> -->
      
    </div>


  </div>

  <main id="main">
  
    <TheWelcome 
      :items="state.data" 
      @in_toc_now="in_toc_now"
    />
  </main>
</template>

<style>
@import './assets/base.css';


#app {
  /*max-width: 1280px;*/
  margin: 0 auto;

  grid-template-columns: 1fr;
  font-weight: normal;
  position:absolute;
  top:0px;
  left:0px;
  max-width: 100vw;

  -webkit-animation: fadein 4s; /* Safari, Chrome and Opera > 12.1 */
  -moz-animation: fadein 4s; /* Firefox < 16 */
   -ms-animation: fadein 4s; /* Internet Explorer */
    -o-animation: fadein 4s; /* Opera < 12.1 */
       animation: fadein 4s;
}

@keyframes fadein {
from { opacity: 0; }
to   { opacity: 1; }
}

/* Firefox < 16 */
@-moz-keyframes fadein {
from { opacity: 0; }
to   { opacity: 1; }
}

/* Safari, Chrome and Opera > 12.1 */
@-webkit-keyframes fadein {
from { opacity: 0; }
to   { opacity: 1; }
}

/* Internet Explorer */
@-ms-keyframes fadein {
from { opacity: 0; }
to   { opacity: 1; }
}

/* Opera < 12.1 */
@-o-keyframes fadein {
from { opacity: 0; }
to   { opacity: 1; }
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
  color: #e6e4d6;
  justify-content: center;
  transition: 0.4s;
  text-align: center;
  font-weight: 300;
  font-size:16px; 

  padding-left: 10%;
  padding-right: 10%;
  line-height: 1.7;

}

.letterClick {
    background: #181818;
    padding-left: 8px;
    padding-right: 8px;
    margin-bottom: 0px;
    font-size: 18px;
}

.letterClick:hover {
  background-color: #333;
  color: #f6f6f6;
}

button {
  background: #181818;
  cursor: pointer;
  flex-direction: column;
  font-size: 14px;
  min-width: 100px;
  align-items: center;
  border: black;
  margin: 4px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  width: 100%;
  /* color: hsla(160, 100%, 37%, 1); */
  background-color: var(--color-background-mute);
  min-height: 40px;
}

button:hover, .button:hover {
  background-color: #9ea5e9;
  color: #181818;
}

button.green-btn {
  background-color: var(--color-background-mute);
  color: #181818;
  height: 56px;
  width: 180px;
  margin: 4px;
  font-size: 20px;
  color: #e6e4d6;
  margin-bottom: 8px;
}

button.green-btn:hover {
  background: #9ea5e9;
  color: #181818;
}

button.green-btn.bottom-btn {
  width: 25%;
  max-height: 40px;
  top: 16px;
}

input {
  margin-top: 8px;
  background: #333;
  height: 32px;
  border-radius: 4px;
  border: none;
  padding: 8px;
}

#main {
  max-height: 100vh;
  overflow-y: scroll;
  
  visibility: hidden;
  display: flex;
  flex-direction: column;
  padding-bottom:400px;
  transition: all 1s;
}

#searchFields {
  border-bottom: solid 1px #9ea5e9;
  top:0px;

  transition: all 6s;
}

#headerDiv {
  visibility:hidden;
  width:84%;
  /*height:100vh;*/
}

#mainText {
  padding-top: 4px;
  line-height: 1.5;
  text-align: left;

  font-size: 16px;

  padding-left: 4%;
  padding-right: 0%;

  width: 100%;
}

#mainTextSubheader {
  font-size: 24px;
  padding-left: 4%;
}

#searchBtnMain {
  margin-left:6%;
  max-width: 88%;
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
    box-shadow: inset 0 0 1px #9ea5e9;
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

  display:flex;
  flex-direction:row;
  width: 100%;
  position: absolute;
  margin:0%;
  max-height: 300px;
  z-index: 1;
  height: 100%;
  background: var(--color-background);
  display: none;
}

#letterSearchBtnColWrap {
  display: flex;
  flex-direction: column;
  bottom:12px;
}

#yearsBetweenRowWrapper {
  display: flex;
  flex-direction: row;
  text-align:center;
  justify-content: center;
}

#titleAuthorInputWrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding-top: 20px;
  padding-bottom: 20px;
  padding-right: 4%;
  padding-left: 4%;
}
#titleAuthorInputWrapper > .label-wrap {
  width:100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

#yearsBetweenInputWrapper > .label-wrap {
  text-align: center;
  height: 100%;
  justify-content: center;
}
#disableFullText {
  opacity:0.5;
  pointer-events: none;
}
#yearsBetweenInputWrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 60%;
}

.inputsRowWrapper {
  flex-direction: row;
  display:inline-flex;
  overflow:auto;
  width:100%;
  padding-left:0%;
  padding-right:2%;
}

#alphabetWrapper {
  overflow-x: scroll;
  overflow-wrap: break-word;
  align-items: center;
  width: 70%;
  position: absolute;
  /* top: 52px; */
  background: transparent;
  z-index: 2;
  right: 0px;
  height: 100%;
  
}

.wrapper-outer {
  width:100%;
  max-height:300px;
  padding-right:2%;
}

.wrapper.search {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.jumbotron {
width: 100%;
  z-index: 40;
  height: 68px;
  padding-left:2%;
  font-size: 48px;
  font-weight: 100;
  top: 0px;
  left: 0px;
  background: rgba(0, 0, 0, 1);
  transition: height 1s ease-in;
  pointer-events: none;

  -webkit-animation: fadein 4s; /* Safari, Chrome and Opera > 12.1 */
  -moz-animation: fadein 4s; /* Firefox < 16 */
   -ms-animation: fadein 4s; /* Internet Explorer */
    -o-animation: fadein 4s; /* Opera < 12.1 */
       animation: fadein 4s;
}

@keyframes fadein {
from { opacity: 0; }
to   { opacity: 1; }
}

/* Firefox < 16 */
@-moz-keyframes fadein {
from { opacity: 0; }
to   { opacity: 1; }
}

/* Safari, Chrome and Opera > 12.1 */
@-webkit-keyframes fadein {
from { opacity: 0; }
to   { opacity: 1; }
}

/* Internet Explorer */
@-ms-keyframes fadein {
from { opacity: 0; }
to   { opacity: 1; }
}

/* Opera < 12.1 */
@-o-keyframes fadein {
from { opacity: 0; }
to   { opacity: 1; }
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
  background-color: var(--color-background);
  height: 100%;
  white-space: nowrap;
  /* padding-top: 188px; */
  width: 100%;

}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  top: 30%;
  left:5%;
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
  background-color:#9ea5e9;
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
  left:-12%;
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
#headerWrapper {
  max-height: 300px;
  padding-left: 4%;
}
#titleAuthorInputWrapper {
  display:flex;
  flex-direction: column;
}

.outer-row {
  padding-top: 12px;
  padding-bottom: 12px;
  border-bottom: solid 1px var(--color-text);
}


@media (max-width: 900px) {

  #headerWrapper {
    padding-left: 2%;
  }

  #headerDiv.noDisplay {
    display: none;
  }
  #newTextPopup {
    padding: 64px !important;
  }

  #mainText {
    font-size: 14px;
  }
  .toggle-wrapper {
    width: 100%;
    background: var(--color-background);
    z-index: 1;
    bottom: 0px;
  }
  .inputsRowWrapper{
    margin-top:8px;
    margin-bottom:8px;
    padding-left:2%;
    padding-right:4%;
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  input {
    width:88%;
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
    margin-left: 12%;
    margin-right: 12%;
    width: 76%;
    top: 4%;
    bottom: 4%;
    height: 92%;
    border-radius: 12px;
    border: solid 1px #e6e4d6;
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

  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
    overflow: auto;


  }
  #yearsBetweenInputerWrapper {
    width: 40%;
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

@media(max-width:600px){
  .outer-row {
    flex-direction: column;
  }
  .author-image {
    min-width: 64px;
  }


  
  #headerDiv, #wrapper-outer {
    width: 100%;
    height: 100%;
    padding-right: 4%;
    padding-left: 0%;
  }
  #letter-wrapper {
    min-height:100px;
  }
  .book-item {
    display:none;
  }
}

@media(min-width:600px){
  .outer-row {
    display: flex;
    flex-direction: row;
    max-width: 100%;
    position: relative;
  }
  #headerDiv, #wrapper-outer {
    width: 76%;
    height:100%;
  }
  .book-item {
    display:flex;
  }
  .author-image {
    min-width: 164px;
    transition: all 1s;
  }
}





</style>
