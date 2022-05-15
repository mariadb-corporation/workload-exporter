#!/usr/bin/env bash

WORKLOAD_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)

PYTHONPATH=$WORKLOAD_DIR
export PYTHONPATH

SQLITE_DIR="/xbench/db"
mkdir -p $SQLITE_DIR
chmod -R 777 /xbench/db
SQLITE_DB="metrics.db"

cd $WORKLOAD_DIR
bin/workload_exporter.py $SQLITE_DIR/$SQLITE_DB
