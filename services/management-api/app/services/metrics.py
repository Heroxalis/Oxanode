import asyncio
from typing import Any

from oxanode_runner.metrics.collector import MetricsCollector

class MetricsService:
    def __init__(self, interval: float = 2.0):
        self.interval = interval
        self.collector = MetricsCollector()
        self.latest_snapshot : dict[str, Any] | None = None
        self._task : asyncio.Task | None = None
        
    async def start(self):
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._collection_loop())
            
    async def stop(self):
        if self._task is None:
            return
        
        self._task.cancel()
        
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        
        self._task = None
        
    async def _collection_loop(self):
        while True:
            try:
                snapshot = await asyncio.to_thread(self.collector.collect)
                self.latest_snapshot = snapshot
            except asyncio.CancelledError:
                raise
            
            except Exception:
                await asyncio.sleep(self.interval)
                continue
            
            await asyncio.sleep(self.interval)
            
    def get_latest_snapshot(self):
        return self.latest_snapshot