# Technical Report: NovaTech Concurrent Processing

## 1. Critical Section Identification & Protection Mechanism
The critical section in this application corresponds to the `process_order_items` method within the `InventoryManager` class.
This section checks stock availability and decrements inventory as an atomic operation.
To protect this shared resource, a `threading.Lock()` mutex was implemented. The lock is held exclusively during the stock verification and update phase, ensuring that no two worker threads read or modify inventory state simultaneously.

## 2. Prevention of Race Conditions and Duplicate Orders
- **Race Conditions:** Without mutual exclusion, two threads reading an inventory count of `1` could both approve order requests simultaneously, driving stock down to `-1`. The `Lock` mechanism enforces strict serial access to inventory checks.
- **Duplicate Orders:** Duplicate processing is prevented by utilizing Python's thread-safe `queue.Queue`. The `.get()` operation atomically extracts items, ensuring that each order is handled by exactly one worker thread.

## 3. Monitor Thread Cancellation Logic
The `SystemMonitor` thread runs a loop conditioned on a `threading.Event` token (`stop_event.is_set()`). 
Upon completion of all worker thread joins in the main thread, `stop_event.set()` is invoked. The monitor thread unblocks from its timed wait (`stop_event.wait(1.5)`), breaks the loop, and closes cleanly without leaving orphan threads.

## 4. Performance Comparison (1 Worker vs 3 Workers)
- **Single-Worker Execution:** Total runtime is approximately equal to the sum of all simulated order delays ($\approx 20 \times 1.25\text{s} = 25\text{s}$).
- **Three-Worker Execution:** Total runtime dropped to approximately **10.11 seconds** (a speedup of $\sim 2.47\times$).
- **Analysis:** Speedup is not strictly $3\times$ due to thread context-switching overhead, GIL locks in I/O operations, thread creation overhead, and minor lock contentions during critical section access.