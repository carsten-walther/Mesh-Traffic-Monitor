#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Packet:
    from_node: str
    to_node: str
    relay_node: str
    channel: str
    port_number: str
    payload_size: int
    id: int
    rx_time: datetime
    from_id: Optional[str] = None
    to_id: Optional[str] = None
    rx_snr: Optional[float] = None
    rx_rssi: Optional[int] = None
    hop_limit: Optional[int] = None
    hop_start: Optional[int] = None
    payload: Optional[str] = None
