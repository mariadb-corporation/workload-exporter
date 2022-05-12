#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2021 dvolkov

import signal
import sys
import time

from collector import CustomCollector, SigTermException
from prometheus_client import REGISTRY, start_http_server


def _on_sighup(sig, frame):
    raise SigTermException


HTTP_PORT = 9300

if __name__ == "__main__":
    # Setup handler for SIGTERM
    signal.signal(signal.SIGHUP, _on_sighup)

    try:
        db_fqn = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <full path to sqlite db>")

    # Start up the server to expose the metrics.
    start_http_server(HTTP_PORT)

    cc = CustomCollector(db_fqn=db_fqn)
    cc.configure()
    REGISTRY.register(cc)

    while True:
        try:
            time.sleep(1)
        except SigTermException as e:
            print("g0t it")
