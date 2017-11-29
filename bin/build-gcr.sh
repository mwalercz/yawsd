#!/usr/bin/env bash

set -ex

PROJECT=dist-queue
IMAGE=dq-worker
VERSION=`git rev-parse --short HEAD`
echo "version: $VERSION"

docker build -t gcr.io/${PROJECT}/${IMAGE}:${VERSION} -f ../docker/Dockerfile ..