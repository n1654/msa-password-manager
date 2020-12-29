#!/usr/bin/env bash

echo $1 | openssl enc -aes-256-cbc -a -pbkdf2 -iter 100000 -salt -pass pass:$2
