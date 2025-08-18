#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Packet:
    timestamp: datetime
    from_node: str
    to_node: str
    message_type: str
    payload_size: int
    snr: Optional[float] = None
    rssi: Optional[int] = None
    hop_limit: Optional[int] = None
    payload: Optional[str] = None