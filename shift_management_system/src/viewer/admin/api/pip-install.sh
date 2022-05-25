#!/bin/sh
docker run --rm \
    -v /"$PWD"://var/task \
    -w //work \
    lambci/lambda:build-python3.8 \
    bash -c "\
    cp /var/task/requirements.txt ./ && \
    pip install -r requirements.txt -t site-packages && \
    (rm -rf /var/task/site-packages; \
    mv /work/* /var/task/) && \
    echo 'pip install completed!!'
    "
