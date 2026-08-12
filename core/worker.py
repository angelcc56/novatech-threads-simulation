# Worker thread implementation for processing orders concurrently

import threading
import time
import random
import queue
from datetime import datetime
from core.inventory_manager import InventoryManager
from core.stats import SimulationStats

class OrderWorker(threading.Thread):
    def __init__(self, worker_id: str, order_queue: queue.Queue, inventory_mgr: InventoryManager, stats: SimulationStats):
        super().__init__()
        self.worker_id = worker_id
        self.order_queue = order_queue
        self.inventory_mgr = inventory_mgr
        self.stats = stats

    def run(self):
        while True:
            try:
                # Non-blocking get or timeout to allow checking if queue is empty
                order = self.order_queue.get(timeout=0.5)
            except queue.Empty:
                break  # Termination condition: No more pending orders

            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] [{self.worker_id}] Processing order {order.order_id} | Customer: {order.customer_name}")

            # RF-04: Simulate processing time between 0.5s and 2.0s OUTSIDE critical section
            time.sleep(random.uniform(0.5, 2.0))

            # Attempt atomic inventory check and reduction (Critical Section)
            success, message = self.inventory_mgr.process_order_items(order.items)

            timestamp_end = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            order.processed_by = self.worker_id

            if success:
                order.status = "APPROVED"
                self.stats.increment_approved()
                print(f"[{timestamp_end}] [{self.worker_id}] {order.order_id} APPROVED | Items: {order.items}")
            else:
                if "Insufficient stock" in message:
                    order.status = "REJECTED"
                    order.rejection_reason = message
                    self.stats.increment_rejected()
                    print(f"[{timestamp_end}] [{self.worker_id}] {order.order_id} REJECTED | Reason: {message}")
                else:
                    order.status = "INVALID"
                    order.rejection_reason = message
                    self.stats.increment_failed()
                    print(f"[{timestamp_end}] [{self.worker_id}] {order.order_id} FAILED | Reason: {message}")

            self.order_queue.task_done()