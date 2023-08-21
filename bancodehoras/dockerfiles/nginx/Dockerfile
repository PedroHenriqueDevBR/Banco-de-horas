FROM nginx:1.21-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY ./dockerfiles/nginx/cert/ /etc/nginx/cert/
COPY ./dockerfiles/nginx/default.conf /etc/nginx/conf.d
