#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Node:
    node_id: str
    short_name: str
    long_name: str
    hardware: str
    last_seen: datetime
    position: Optional[tuple] = None  # (lat, lon, alt)
    snr: Optional[float] = None
    rssi: Optional[int] = None
    battery_level: Optional[int] = None
