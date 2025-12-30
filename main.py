import multiprocessing
import time
import random
import matplotlib.pyplot as plt
import numpy as np

def sensor_worker(sensor_id, queue):
    """Simulates a sensor sending data to a queue with potential faults."""
    for _ in range(30):  # Increased data points for better graphing
        try:
            data = random.uniform(20.0, 100.0)  # e.g., temperature
            if random.random() < 0.1:  # 10% chance of fault
                raise ValueError("Sensor fault simulated")
            queue.put((sensor_id, data))
            time.sleep(random.uniform(0.5, 1.5))
        except ValueError:
            print(f"Fault in sensor {sensor_id}, retrying...")
            time.sleep(1)  # Retry delay

def processor_worker(queue, results):
    """Processes data from queue, simulates anomaly detection with parallelism."""
    while True:
        try:
            sensor_id, data = queue.get(timeout=1)
            # Simple processing: check if data is anomalous
            if data > 80:
                print(f"Anomaly detected from sensor {sensor_id}: {data}")
            results.append((sensor_id, data))
        except multiprocessing.queues.Empty:
            break

if __name__ == "__main__":
    num_sensors = 8  # Scaled up for next-level demo
    queue = multiprocessing.Queue()
    results = multiprocessing.Manager().list()

    # Start sensor workers with fault tolerance
    sensors = [multiprocessing.Process(target=sensor_worker, args=(i, queue)) for i in range(num_sensors)]
    for s in sensors:
        s.start()

    # Start processor workers (more for better parallelism)
    processors = [multiprocessing.Process(target=processor_worker, args=(queue, results)) for _ in range(4)]
    for p in processors:
        p.start()

    # Wait for completion
    for s in sensors:
        s.join()
    for p in processors:
        p.join()

    # Aggregate and visualize results
    if results:
        sensor_data = {}
        for sid, data in results:
            if sid not in sensor_data:
                sensor_data[sid] = []
            sensor_data[sid].append(data)
        
        # Plotting graphics: Time-series for each sensor
        plt.figure(figsize=(12, 8))
        for sid, data_list in sensor_data.items():
            plt.plot(np.arange(len(data_list)), data_list, label=f"Sensor {sid}")
        plt.title("IIoT Sensor Data Streams (Parallel Processing)")
        plt.xlabel("Time Steps")
        plt.ylabel("Sensor Value (e.g., Temperature)")
        plt.legend()
        plt.grid(True)
        plt.savefig("sensor_data_plot.png")
        plt.show()  # Optional: show in interactive mode
        print("Graphics generated: sensor_data_plot.png")
        
        # Advanced aggregation: Compute averages per sensor
        averages = {sid: sum(data_list)/len(data_list) for sid, data_list in sensor_data.items()}
        print("Per-sensor averages:", averages)
    else:
        print("No data processed.")
