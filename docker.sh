#!/bin/bash

git pull
docker stop pou
docker build -t pou:latest -f Dockerfile .
docker run --rm --name pou pou:latest