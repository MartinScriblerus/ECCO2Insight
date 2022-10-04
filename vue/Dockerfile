FROM node:lts-alpine

# install simple http server for serving static content
RUN npm install -g http-server

# make the 'app' folder the current working directory
WORKDIR /
ARG VUE_APP_FRONTEND_URL                       
ENV VUE_APP_FRONTEND_URL=$VUE_APP_FRONTEND_URL 
# copy both 'package.json' and 'package-lock.json' (if available)
# COPY vue/package*.json ./
COPY vue/package*.json /

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
# COPY ./vue ./
COPY /vue /

# build app for production with minification
# RUN npm run build-only
RUN npm run build

EXPOSE 8080

CMD [ "http-server", "dist" ]