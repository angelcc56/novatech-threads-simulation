# Helper module to convert seed data into Order objects and populate the Queue

import queue
from data.models import Order
from data.orders_data import RAW_ORDERS

def load_orders_into_queue() -> queue.Queue:
    order_queue = queue.Queue()
    for data in RAW_ORDERS:
        order = Order(
            order_id=data["order_id"],
            customer_name=data["customer"],
            items=data["items"]
        )
        order_queue.put(order)
    return order_queue