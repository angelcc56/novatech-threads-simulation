# Main entry point: Orchestrates threads, monitor, and clean termination

import time
import threading
from data.inventory import INITIAL_INVENTORY
from core.inventory_manager import InventoryManager
from core.loader import load_orders_into_queue
from core.stats import SimulationStats
from core.worker import OrderWorker
from core.monitor import SystemMonitor

def main():
    print("=== NovaTech Concurrent Order Processing Simulation ===")
    start_time = time.time()

    # 1. Initialize core components
    inv_manager = InventoryManager(INITIAL_INVENTORY)
    stats = SimulationStats()
    order_queue = load_orders_into_queue()
    total_orders = order_queue.qsize()

    print(f"[INIT] Shared queue loaded with {total_orders} orders.")
    print(f"[INIT] Starting 3 OrderWorker threads and 1 SystemMonitor thread...\n")

    # 2. Create Worker Threads (RF-03)
    workers = []
    for i in range(1, 4):
        worker = OrderWorker(f"WORKER-{i}", order_queue, inv_manager, stats)
        workers.append(worker)

    # Function to calculate active worker threads
    def get_active_workers_count():
        return sum(1 for w in workers if w.is_alive())

    # 3. Create and start SystemMonitor Thread (RF-07)
    stop_monitor_event = threading.Event()
    monitor = SystemMonitor(order_queue, stats, stop_monitor_event, get_active_workers_count)
    monitor.start()

    # 4. Start Worker Threads
    for worker in workers:
        worker.start()

    # 5. Wait for all worker threads to complete (RF-09 / Join)
    for worker in workers:
        worker.join()

    # 6. Stop and join Monitor Thread cleanly
    stop_monitor_event.set()
    monitor.join()

    elapsed_time = time.time() - start_time
    summary = stats.get_summary()

    # 7. Print Final Summary (RF-10)
    print("\n" + "="*50)
    print("FINAL SUMMARY")
    print("="*50)
    print(f"Total Orders Processed: {summary['total_processed']} / {total_orders}")
    print(f"  - Approved: {summary['approved']}")
    print(f"  - Rejected: {summary['rejected']}")
    print(f"  - Failed/Invalid: {summary['failed']}")
    print(f"Total Execution Time: {elapsed_time:.2f} seconds")
    print(f"Active Threads Remaining: {threading.active_count() - 1}")
    print("\nRemaining Inventory Stock:")
    for code, stock in inv_manager.get_all_inventory().items():
        print(f"  - {code}: {stock} units")
    print("="*50)

if __name__ == "__main__":
    main()