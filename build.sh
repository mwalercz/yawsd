#!/usr/bin/env bash

set -ex
USERNAME=mwalercz
IMAGE=dq_worker
docker build -t ${USERNAME}/${IMAGE}:latest -f docker/Dockerfile .