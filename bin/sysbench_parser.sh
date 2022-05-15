#!/usr/bin/env bash

WORKLOAD_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)

PYTHONPATH=$WORKLOAD_DIR
export PYTHONPATH

SQLITE_DIR="/xbench/db"
SQLITE_DB="metrics.db"

sudo chmod -R 777 $SQLITE_DIR/$SQLITE_DB

cd $WORKLOAD_DIR
bin/sysbench_parser.py
