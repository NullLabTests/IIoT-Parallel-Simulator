import multiprocessing
import time
import random

def sensor_worker(sensor_id, queue):
    """Simulates a sensor sending data to a queue."""
    for _ in range(10):
        data = random.uniform(20.0, 100.0)  # e.g., temperature
        queue.put((sensor_id, data))
        time.sleep(random.uniform(0.5, 1.5))

def processor_worker(queue, results):
    """Processes data from queue, simulates anomaly detection."""
    while True:
        try:
            sensor_id, data = queue.get(timeout=1)
            # Simple processing: check if data is anomalous
            if data > 80:
                print(f"Anomaly detected from sensor {sensor_id}: {data}")
            results.append(data)
        except multiprocessing.queues.Empty:
            break

if __name__ == "__main__":
    num_sensors = 4
    queue = multiprocessing.Queue()
    results = multiprocessing.Manager().list()

    # Start sensor workers
    sensors = [multiprocessing.Process(target=sensor_worker, args=(i, queue)) for i in range(num_sensors)]
    for s in sensors:
        s.start()

    # Start processor workers (parallel processing)
    processors = [multiprocessing.Process(target=processor_worker, args=(queue, results)) for _ in range(2)]
    for p in processors:
        p.start()

    # Wait for completion
    for s in sensors:
        s.join()
    for p in processors:
        p.join()

    # Aggregate results
    if results:
        avg = sum(results) / len(results)
        print(f"Aggregated average: {avg:.2f}")
    else:
        print("No data processed.")
