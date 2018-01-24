#!/usr/bin/env bash

set -ex

IMAGE=yawsd
VERSION=`git rev-parse --short HEAD`
echo "version: $VERSION"

./build-gcr.sh
gcloud docker -- push gcr.io/dist-queue/${IMAGE}:${VERSION}