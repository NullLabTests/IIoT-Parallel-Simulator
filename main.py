import multiprocessing
import time
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest
import logging
import argparse
import paho.mqtt.client as mqtt

# Setup logging (Feature 4: Enhanced logging)
logging.basicConfig(filename='iiot_sim.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def on_connect(client, userdata, flags, reason_code, properties):
    logging.info(f"MQTT connected with result code {reason_code}")

def sensor_worker(sensor_id, queue, args):
    """Simulates a sensor sending data to a queue with potential faults."""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect("localhost", 1883, 60)  # Assume local MQTT broker (Feature 1: MQTT integration)
    client.loop_start()
    
    for _ in range(args.load):  # Scalability: Variable load (Feature 5)
        try:
            data = random.uniform(20.0, 100.0)
            if random.random() < 0.1:
                raise ValueError("Sensor fault simulated")
            
            # Edge computing sim: Pre-process at 'edge' (Feature 3)
            processed_data = data * 1.1 if data > 50 else data  # Simple edge transformation
            
            queue.put((sensor_id, processed_data))
            client.publish(f"sensor/{sensor_id}", str(processed_data))  # Publish to MQTT
            logging.info(f"Sensor {sensor_id} sent: {processed_data}")
            time.sleep(random.uniform(0.5, 1.5))
        except ValueError:
            logging.warning(f"Fault in sensor {sensor_id}, retrying...")
            time.sleep(1)
    
    client.loop_stop()

def processor_worker(queue, results):
    """Processes data from queue."""
    while True:
        try:
            sensor_id, data = queue.get(timeout=1)
            if data > 80:
                print(f"Threshold anomaly from sensor {sensor_id}: {data}")
                logging.info(f"Threshold anomaly from sensor {sensor_id}: {data}")
            results.append((sensor_id, data))
        except multiprocessing.queues.Empty:
            break

def digital_twin_worker(results):
    """Basic digital twin: Mirrors and monitors aggregated data (Feature 2)."""
    time.sleep(10)  # Wait for some data
    mirrored_data = list(results)  # Mirror
    avg = np.mean([d[1] for d in mirrored_data]) if mirrored_data else 0
    logging.info(f"Digital twin mirror average: {avg}")
    print(f"Digital twin detected overall average: {avg}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IIoT Simulator")
    parser.add_argument('--num_sensors', type=int, default=8, help="Number of sensors (scalability)")
    parser.add_argument('--load', type=int, default=30, help="Data points per sensor (load testing)")
    args = parser.parse_args()
    
    queue = multiprocessing.Queue()
    results = multiprocessing.Manager().list()

    # Start sensor workers
    sensors = [multiprocessing.Process(target=sensor_worker, args=(i, queue, args)) for i in range(args.num_sensors)]
    for s in sensors:
        s.start()

    # Start processor workers
    processors = [multiprocessing.Process(target=processor_worker, args=(queue, results)) for _ in range(4)]
    for p in processors:
        p.start()

    # Start digital twin
    twin = multiprocessing.Process(target=digital_twin_worker, args=(results,))
    twin.start()

    # Wait for completion
    for s in sensors:
        s.join()
    for p in processors:
        p.join()
    twin.join()

    # ML anomaly detection
    if results:
        sensor_data = {}
        all_data = []
        for sid, data in results:
            if sid not in sensor_data:
                sensor_data[sid] = []
            sensor_data[sid].append(data)
            all_data.append([data])

        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomalies = iso_forest.fit_predict(all_data)
        anomaly_indices = np.where(anomalies == -1)[0]
        for idx in anomaly_indices:
            sid, val = results[idx]
            print(f"ML-detected anomaly from sensor {sid}: {val}")
            logging.info(f"ML anomaly from sensor {sid}: {val}")

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

        averages = {sid: sum(data_list)/len(data_list) for sid, data_list in sensor_data.items()}
        print("Per-sensor averages:", averages)
    else:
        print("No data processed.")
