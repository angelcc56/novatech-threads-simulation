# Main entry point for NovaTech order processing simulation

from data.inventory import INITIAL_INVENTORY
from core.inventory_manager import InventoryManager
from core.loader import load_orders_into_queue

def main():
    print("=== NovaTech Concurrent Order Processing Simulation ===")

    # Initialize Inventory
    inv_manager = InventoryManager(INITIAL_INVENTORY)
    print(f"[INIT] Loaded inventory with {len(inv_manager.get_all_inventory())} products.")

    # Populate Shared Queue
    order_queue = load_orders_into_queue()
    print(f"[INIT] Loaded shared queue with {order_queue.qsize()} orders.")

if __name__ == "__main__":
    main()