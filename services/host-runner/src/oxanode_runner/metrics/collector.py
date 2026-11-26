
import time
from datetime import datetime, timezone
from typing import Any

import psutil


class MetricsCollector:
    def __init__(self):
        self._previous_network = None
        self._previous_time = None
        psutil.cpu_percent(interval=None)

    def collect(self) -> dict[str, Any]:
        current_time = time.monotonic()
        boot_time = psutil.boot_time()
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage("/")
        network = psutil.net_io_counters()

        network_rates = {
            "bytes_sent_per_second": None,
            "bytes_received_per_second": None,
            "packets_sent_per_second": None,
            "packets_received_per_second": None,
        }

        if (
            network is not None
            and self._previous_network is not None
            and self._previous_time is not None
        ):
            elapsed = current_time - self._previous_time

            if elapsed > 0:
                network_rates = {
                    "bytes_sent_per_second": max(
                        0.0,
                        (network.bytes_sent - self._previous_network.bytes_sent) / elapsed,
                    ),
                    "bytes_received_per_second": max(
                        0.0,
                        (network.bytes_recv - self._previous_network.bytes_recv) / elapsed,
                    ),
                    "packets_sent_per_second": max(
                        0.0,
                        (network.packets_sent - self._previous_network.packets_sent) / elapsed,
                    ),
                    "packets_received_per_second": max(
                        0.0,
                        (network.packets_recv - self._previous_network.packets_recv) / elapsed,
                    ),
                }

        if network is not None:
            self._previous_network = network
            self._previous_time = current_time

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": {
                "uptime_seconds": max(0.0, time.time() - boot_time),
                "boot_time": datetime.fromtimestamp(
                    boot_time, timezone.utc
                ).isoformat(),
                "cpu": {
                    "usage_percent": psutil.cpu_percent(interval=None),
                    "logical_cores": psutil.cpu_count(logical=True),
                    "physical_cores": psutil.cpu_count(logical=False),
                },
                "memory": {
                    "total_bytes": memory.total,
                    "available_bytes": memory.available,
                    "used_bytes": memory.used,
                    "usage_percent": memory.percent,
                },
                "swap": {
                    "total_bytes": swap.total,
                    "used_bytes": swap.used,
                    "free_bytes": swap.free,
                    "usage_percent": swap.percent,
                },
                "disk": {
                    "mountpoint": "/",
                    "total_bytes": disk.total,
                    "used_bytes": disk.used,
                    "free_bytes": disk.free,
                    "usage_percent": disk.percent,
                },
                "network": {
                    "bytes_sent": network.bytes_sent if network else 0,
                    "bytes_received": network.bytes_recv if network else 0,
                    "packets_sent": network.packets_sent if network else 0,
                    "packets_received": network.packets_recv if network else 0,
                    **network_rates,
                },
            },
        }


_default_collector = MetricsCollector()


def collect_metrics() -> dict[str, Any]:
    return _default_collector.collect()
