FROM nginx:1.21-alpine

# RUN apk add --no-cache nginx-mod-http-perl



# COPY ./etc/nginx/nginx.conf .
COPY /etc/nginx/nginx.conf .
EXPOSE 80/tcp
EXPOSE 443/tcp

CMD ["nginx", "-g", "daemon off;"]

