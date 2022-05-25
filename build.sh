#!/bin/sh
docker-compose build shift_management_system && \
  docker rmi $(docker image ls -qf dangling=true)
