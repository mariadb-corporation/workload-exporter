#!/usr/bin/env bash

WORKLOAD_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)

PYTHONPATH=$WORKLOAD_DIR
export PYTHONPATH

cd $WORKLOAD_DIR
bin/sysbench_parser.py
