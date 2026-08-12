# Inventory Manager module with Thread-Safe inventory validation and reduction

import threading
from typing import Dict, Tuple

class InventoryManager:
    def __init__(self, initial_stock: Dict[str, dict]):
        self.inventory = {
            code: {"name": data["name"], "stock": data["stock"]}
            for code, data in initial_stock.items()
        }
        # Lock to protect Critical Section (Inventory reads and writes)
        self.lock = threading.Lock()

    def process_order_items(self, items: Dict[str, int]) -> Tuple[bool, str]:
        """
        Thread-safe method to validate and update inventory atomically.
        Returns: (success: bool, message: str)
        """
        # CRITICAL SECTION BEGINS
        with self.lock:
            # 1. Validation phase (Check if product exists and if stock is sufficient)
            if not items:
                return False, "Order contains no items"

            for code, qty in items.items():
                if code not in self.inventory:
                    return False, f"Product {code} does not exist"
                if qty <= 0:
                    return False, f"Invalid quantity ({qty}) requested for {code}"
                if self.inventory[code]["stock"] < qty:
                    return False, f"Insufficient stock for product {code} (Requested: {qty}, Available: {self.inventory[code]['stock']})"

            # 2. Reduction phase (Only if ALL items are available)
            for code, qty in items.items():
                self.inventory[code]["stock"] -= qty

            return True, "Approved"
        # CRITICAL SECTION ENDS

    def get_all_inventory(self) -> Dict[str, dict]:
        with self.lock:
            return {code: data["stock"] for code, data in self.inventory.items()}