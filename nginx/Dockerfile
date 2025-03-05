FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir -p /etc/nginx/ssl
RUN chmod 600 /etc/nginx/ssl

COPY nginx.conf /etc/nginx/conf.d/default.conf