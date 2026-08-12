# Inventory Manager module to maintain stock state

from typing import Dict

class InventoryManager:
    def __init__(self, initial_stock: Dict[str, dict]):
        # Deep copy to avoid modifying original reference
        self.inventory = {
            code: {"name": data["name"], "stock": data["stock"]}
            for code, data in initial_stock.items()
        }

    def get_stock(self, product_code: str) -> int:
        if product_code in self.inventory:
            return self.inventory[product_code]["stock"]
        return 0

    def get_all_inventory(self) -> Dict[str, dict]:
        return self.inventory