#!/usr/bin/env sh
/usr/sbin/sshd
worker -c docker.ini
"$@"
