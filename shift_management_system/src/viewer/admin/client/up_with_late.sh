#/bin/bash
#docker-sync start && \
sleep 10 && \
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d
