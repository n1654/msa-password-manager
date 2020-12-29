FROM alpine:latest

RUN apk add --no-cache openssh openssl bash python3 py3-pip

RUN mkdir /start
WORKDIR /start
COPY . /start

RUN ["chmod", "+x", "-R", "/start/"]
ENTRYPOINT ["/start/entrypoint.sh"]
