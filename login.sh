#!/bin/bash
docker-compose up -d && winpty docker-compose exec shift_management_system bash --login
