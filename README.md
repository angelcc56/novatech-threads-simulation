# NovaTech - Concurrent Order Processing Simulator

Concurrency simulation using real Threads, Locks, and Queues in Python.

## Description
This application simulates a real-time order processing system for NovaTech, ensuring thread-safe inventory management and status monitoring.

# NovaTech - Concurrent Order Processing Simulator

Simulation of a multi-threaded concurrent order processing system in Python, built for NovaTech to demonstrate thread safety, critical section protection, and performance gains without race conditions.

## Requirements & Environment
- **Language:** Python 3.8+
- **Libraries used:** Standard Library only (`threading`, `queue`, `time`, `random`, `dataclasses`)
- **Tested OS:** Linux / macOS / Windows

## How to Run

1. Clone the repository:
   ```bash
   git clone [https://github.com/angelcc56/novatech-threads-simulation.git](https://github.com/angelcc56/novatech-threads-simulation.git)
   cd novatech-threads-simulation

   Execution options:
   
   a. Run the concurrent simulation:
   
   python main.py
   
   b. Run automatic invariant and test checks:
   
   python -m tests.test_cases

## Concurrency Architecture & Synchronizations

- **Main Thread:** Loads initial state, spawns 3 workers + 1 monitor, waits via `join()`, and reports final metrics.
- **Worker Threads (3x):** Process orders concurrently from a shared `queue.Queue`. Critical inventory modification is guarded by a `threading.Lock()` mutex.
- **System Monitor Thread (1x):** Periodically logs active queue size, approved/rejected counters, and active worker count until signaled by a `threading.Event` token.
- **Shared Resources:** 
  - Inventory dict protected via `threading.Lock`
  - Statistics counters protected via `threading.Lock`
  - Order queue managed via thread-safe `queue.Queue`

  ## Test Cases Summary

| Test Case | Description | Expected & Verified Result |
| :--- | :--- | :--- |
| **CP-01** | Normal Flow | Valid orders processed and approved concurrently. |
| **CP-02** | Contention | Multiple workers compete for P005 stock; stock never drops below 0. |
| **CP-03** | Insufficient Stock | Orders exceeding stock (e.g., ORD-009) are rejected without stock deduction. |
| **CP-04** | Invalid Order | Malformed orders (e.g., non-existent products) trigger safe errors without crash. |
| **CP-05** | Clean Closure | All threads join properly with 0 active orphan threads remaining. |