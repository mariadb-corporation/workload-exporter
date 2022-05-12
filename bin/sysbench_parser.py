#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2021 dvolkov

import fileinput
import re
import sys

from collector import SysbenchSQLite

SQLITE_DB = "/xbench/db/metrics.db"

# sysbench oltp_read_write <> | sysbench_parser.py
if __name__ == "__main__":

    s = SysbenchSQLite(SQLITE_DB)

    for line in fileinput.input():
        if re.match(r"^\[", line):
            threads, throughput, latency = s.parse_sysbench_line(line)
            print(threads, throughput, latency)
            s.store_metrics(threads, throughput, latency)

        if line.startswith("Latency histogram"):
            break
