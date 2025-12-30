import multiprocessing
import time
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest

def sensor_worker(sensor_id, queue):
    """Simulates a sensor sending data to a queue with potential faults."""
    for _ in range(30):  # More data for ML training
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
                print(f"Threshold anomaly from sensor {sensor_id}: {data}")
            results.append((sensor_id, data))
        except multiprocessing.queues.Empty:
            break

if __name__ == "__main__":
    num_sensors = 8
    queue = multiprocessing.Queue()
    results = multiprocessing.Manager().list()

    # Start sensor workers
    sensors = [multiprocessing.Process(target=sensor_worker, args=(i, queue)) for i in range(num_sensors)]
    for s in sensors:
        s.start()

    # Start processor workers
    processors = [multiprocessing.Process(target=processor_worker, args=(queue, results)) for _ in range(4)]
    for p in processors:
        p.start()

    # Wait for completion
    for s in sensors:
        s.join()
    for p in processors:
        p.join()

    # Aggregate and ML anomaly detection
    if results:
        sensor_data = {}
        all_data = []
        for sid, data in results:
            if sid not in sensor_data:
                sensor_data[sid] = []
            sensor_data[sid].append(data)
            all_data.append([data])  # For IsolationForest (expects 2D)

        # ML anomaly detection
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomalies = iso_forest.fit_predict(all_data)
        anomaly_indices = np.where(anomalies == -1)[0]
        for idx in anomaly_indices:
            sid, val = results[idx]
            print(f"ML-detected anomaly from sensor {sid}: {val}")

        # Plotting
        plt.figure(figsize=(12, 8))
        for sid, data_list in sensor_data.items():
            plt.plot(np.arange(len(data_list)), data_list, label=f"Sensor {sid}")
        plt.title("IIoT Sensor Data Streams (Parallel Processing with ML Anomalies)")
        plt.xlabel("Time Steps")
        plt.ylabel("Sensor Value (e.g., Temperature)")
        plt.legend()
        plt.grid(True)
        plt.savefig("sensor_data_plot.png")
        # plt.show()  # Commented for non-interactive

        # Averages
        averages = {sid: sum(data_list)/len(data_list) for sid, data_list in sensor_data.items()}
        print("Per-sensor averages:", averages)
    else:
        print("No data processed.")
