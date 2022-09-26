# TCP DATA Viz

## Objectives 
### TCP Data Viz aggregates over 50,000 digitized texts from three archives assembled by the Text Creation Partnership: Early American Imprints, Eighteenth-Century Collections Online, and Early English Books Online.

### The current version is a minimal viable demonstration of the site, and future roadmap items include:
    * Automated build and deploy process for ongoing updates
    * Many more D3 graphs (see the console for a glimpse at available NLP data)
    * Sonification of poetic features
    * Machine Learning for generative tasks, analysis, and comparison
    * The ability to create, label, and graph groups of texts
    * Full Text Searches in EAI, ECCO, and EEBO
    * An extended database structure including knowledge graphs and text classification
    * User management, data persistence, and collaboration features
    * A feature section showcasing contributions from users

## Build Instructions

### Local Testing
* Build the frontend by running 'npm run build-only' in the /vue directory

* Create Docker images and containers for backend, frontend, db, and proxy server by entering the root directory ('habitat-practice') and running 'docker compose build --no-cache' and 'docker compose up --force-recreate'.

* Before this will work, you'll need to recreate the database. Uncomment the lines beginning on 239 in App.vue and run the program once. Then you can uncomment those again (a more efficient process is in the works...)  

* While the frontend will be proxied at localhost:8080, you can also test updates on localhost:8000 by running 'npm run dev' in the /vue folder

![Landing Page](./habitat-practice/vue/src/assets/landingpage.png?raw=true)
![Loading Screen](./habitat-practice/vue/src/assets/loadingscreen.png?raw=true)
![Initial Line Graph](./habitat-practice/vue/src/assets/initialline.png?raw=true)

![Line Color Picker](./habitat-practice/vue/src/assets/colorpicker.png?raw=true)

![Multiple Lines](./habitat-practice/vue/src/assets/twolines.png?raw=true)