#!/usr/bin/env bash

set -e

poetry install


cd ipor_scrapper/

docker-compose -f docker-compose.yml rm -s -v -f

docker-compose up -d


pytest tests -vvv

cd ..
echo -e "\n\e[32mBuild scrapper docker...\e[0m\n"
docker build --platform linux/arm64 -f Dockerfile -t ipor_scrapper:v1 .

docker run scrapper:v1
