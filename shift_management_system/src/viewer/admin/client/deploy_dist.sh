#!/bin/bash
if [ "$1" = "" ]
then
    echo "第1引数にS3BUCKETを指定して下さい。"
    # 処理を中断。
    exit 1
fi
S3BUCKET=$1
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR && \
  aws s3 sync vuejs_project/customer_viewer/dist/ s3://$S3BUCKET --delete
