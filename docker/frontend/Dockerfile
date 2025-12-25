FROM nginx:1.25-alpine

WORKDIR /web
COPY ./landing/index.html /usr/share/nginx/html

USER root
RUN chmod -R 755 /usr/share/nginx/html && chown -R nginx:nginx /usr/share/nginx/html

# Nginx configuration will be injected via volume or file
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]