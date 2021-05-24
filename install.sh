#!/bin/bash

BASEDIR=$(dirname $(readlink -f "$BASH_SOURCE"))

sed -e "s:__BASEDIR__:$BASEDIR:g" \
    mystrom-backend.service.template > /etc/systemd/system/mystrom-backend.service

systemctl enable mystrom-backend
