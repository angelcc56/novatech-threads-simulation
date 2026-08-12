# System Architecture & Thread Flow Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Main as Main Thread
    participant Queue as Shared Queue (Queue.Queue)
    participant W1 as Worker 1
    participant W2 as Worker 2
    participant W3 as Worker 3
    participant Lock as Inventory Lock (Mutex)
    participant Inv as Shared Inventory
    participant Mon as System Monitor Thread

    Main->>Queue: Load 20 Orders
    Main->>Mon: Start Monitor Thread
    Main->>W1: Start Worker 1
    Main->>W2: Start Worker 2
    Main->>W3: Start Worker 3

    loop Periodic Logging
        Mon->>Queue: Check pending size
        Mon->>Inv: Read snapshot state
    end

    par Concurrent Processing
        W1->>Queue: get() Order
        W2->>Queue: get() Order
        W3->>Queue: get() Order
    end

    opt Critical Section Access
        W1->>Lock: Acquire Lock
        W1->>Inv: Validate & Update Stock
        W1->>Lock: Release Lock
    end

    Main->>W1: join()
    Main->>W2: join()
    Main->>W3: join()
    Main->>Mon: Signal stop_event & join()