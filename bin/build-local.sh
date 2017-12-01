#!/usr/bin/env bash

set -ex
PROJECT=dist-queue
IMAGE=dq-worker

VERSION=`git rev-parse --short HEAD`
echo "version: $VERSION"

docker build -t ${PROJECT}/${IMAGE}:latest -f ../docker/Dockerfile ..
docker tag ${PROJECT}/${IMAGE}:latest ${PROJECT}/${IMAGE}:${VERSION}
