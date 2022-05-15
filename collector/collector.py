#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2021 dvolkov


from prometheus_client import REGISTRY
from prometheus_client.core import GaugeMetricFamily

from .sysbench_sqlite import SysbenchSQLite


class SigTermException(Exception):
    """SIGTERM signal"""


class CustomCollector(object):
    def __init__(self, db_fqn):
        self.s = SysbenchSQLite(db_name=db_fqn)

    def configure(self):
        # clean all default collectors
        collectors = list(REGISTRY._collector_to_names.keys())
        for collector in collectors:
            REGISTRY.unregister(collector)

    def collect(self):
        letency_g = GaugeMetricFamily(
            "sysbench_latency", "sysbench p95 latency", labels=["benchmark"]
        )
        threads_g = GaugeMetricFamily(
            "sysbench_threads", "sysbench threads", labels=["benchmark"]
        )
        tps_g = GaugeMetricFamily("sysbench_tps", "sysbench tps", labels=["benchmark"])
        row = self.s.get_latest_metrics(seconds_ago=30)

        if row is not None:
            print(row)
            letency_g.add_metric([row.get("benchmark")], row.get("latency"))
            threads_g.add_metric([row.get("benchmark")], row.get("threads"))
            tps_g.add_metric([row.get("benchmark")], row.get("tps"))
            yield letency_g
            yield threads_g
            yield tps_g
