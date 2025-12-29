# IIoT-Parallel-Simulator

A simple Python project simulating parallelism in an Industrial Internet of Things (IIoT) system, based on concepts from K. Eric Harper's "Industrial Internet Reference Architecture" (2015). This demonstrates concurrent processing of sensor data using Python's multiprocessing module to handle real-time streams, fault tolerance basics, and scalable analytics.

## Features
- Virtual sensors generating random data (e.g., temperature, pressure).
- Parallel workers processing data streams for aggregation and anomaly detection.
- Basic fault simulation with retry mechanisms.

## Installation
1. Clone the repo: `git clone https://github.com/NullLabTests/IIoT-Parallel-Simulator.git`
2. Install dependencies: `pip install -r requirements.txt`

## Usage
Run the simulator: `python main.py`

It will spawn multiple processes to handle sensor data in parallel and output aggregated results.

## Inspiration
Drawn from Harper's work on IIoT architectures, emphasizing distributed concurrency for industrial scalability.

## License
MIT
