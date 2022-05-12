#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2021 dvolkov


import re
from typing import Dict, Optional

from sqlite_client import SQLiteClient


class SysbenchSQLite(SQLiteClient):
    def __init__(self, benchmark: str = "9010", db_name: str = "test.db"):
        self.benchmark = benchmark
        super().__init__(db_name)
        self.connect()
        self.execute(
            "create table IF NOT EXISTS sysbench_stats ( benchmark varchar,  dtime timestamp  DEFAULT (datetime('now','localtime')), threads int, tps real, latency real, errors int default 0)"
        )

    def parse_sysbench_line(self, line: str) -> tuple:
        """Parse one line of sysbench output

        Args:
            line (_type_): line from sysbench output

        Returns:
            tuple: threads, tps, latency)
        """
        match = re.search("thds: (.*?) ", line)
        threads = float(match.group(1))
        match = re.search("tps: (.*?) ", line)
        tps = float(match.group(1))
        match = re.search(r"lat \(.*?\): (.*?) ", line)
        latency = float(match.group(1))
        match = re.search(r"qps: (.*?) \(.*?\) ", line)
        qps = float(match.group(1))
        return (threads, tps, latency)

    def store_metrics(self, threads, throughput, latency):
        self.execute(
            "insert into sysbench_stats (benchmark, threads, tps, latency ) values (?, ?, ?, ?)",
            (self.benchmark, threads, throughput, latency),
        )

    def get_latest_metrics(self, seconds_ago: int = 30) -> Optional[Dict]:
        rows = self.select_all_rows(
            f"select * from sysbench_stats where dtime > datetime('now', '-{seconds_ago} seconds', 'localtime') order by dtime desc limit 1"
        )

        if len(rows) > 0:
            return rows[0]
        else:
            return None
