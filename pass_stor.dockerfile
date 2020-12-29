FROM alpine:latest

RUN apk add --no-cache openssh openssl bash

RUN mkdir /start
WORKDIR /start
COPY ./entrypoint.sh /start
COPY ./encrypt.sh /start
COPY ./decrypt.sh /start

RUN ["chmod", "+x", "-R", "/start/"]
ENTRYPOINT ["/start/entrypoint.sh"]
