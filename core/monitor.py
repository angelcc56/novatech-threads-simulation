# Monitor thread to periodically report system status

import threading
import time
import queue
from core.stats import SimulationStats

class SystemMonitor(threading.Thread):
    def __init__(self, order_queue: queue.Queue, stats: SimulationStats, stop_event: threading.Event, get_active_workers_func):
        super().__init__()
        self.order_queue = order_queue
        self.stats = stats
        self.stop_event = stop_event
        self.get_active_workers = get_active_workers_func

    def run(self):
        while not self.stop_event.is_set():
            summary = self.stats.get_summary()
            pending = self.order_queue.qsize()
            active_workers = self.get_active_workers()

            print(f"[MONITOR] Pending: {pending} | Approved: {summary['approved']} | Rejected: {summary['rejected']} | Failed: {summary['failed']} | Active Workers: {active_workers}")

            # Wait 1.5 seconds or until stop event is triggered
            self.stop_event.wait(1.5)