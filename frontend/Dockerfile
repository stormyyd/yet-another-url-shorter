FROM debian:stretch

WORKDIR /root

RUN apt-get update && apt-get install -y curl gnupg1 apt-transport-https ca-certificates \
    && curl -o nginx_signing.key https://nginx.org/keys/nginx_signing.key \
    && apt-key add nginx_signing.key \
    && echo "deb http://nginx.org/packages/mainline/debian/ stretch nginx" >> /etc/apt/sources.list \
    && echo "deb-src http://nginx.org/packages/mainline/debian/ stretch nginx" >> /etc/apt/sources.list \
    && curl -o setup_8.x.sh https://deb.nodesource.com/setup_8.x \
    && bash setup_8.x.sh \
    && apt-get install -y nginx nodejs

WORKDIR /usr/src/app

COPY . .

RUN npm install && npm run build && cp nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]