#!/usr/bin/env bash

set -ex

USERNAME=mwalercz
IMAGE=dq_worker

VERSION=`git rev-parse --short HEAD`
echo "version: $VERSION"

./build.sh

docker tag ${USERNAME}/${IMAGE}:latest ${USERNAME}/${IMAGE}:${VERSION}
docker push ${USERNAME}/${IMAGE}:latest
docker push ${USERNAME}/${IMAGE}:${VERSION}