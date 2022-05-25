#!/bin/bash
docker compose stop && \
docker compose -f docker-compose.yml -f docker-compose-dev.yml up -d
