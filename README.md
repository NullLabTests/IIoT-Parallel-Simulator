# IIoT-Parallel-Simulator

A Python project simulating parallelism in an Industrial Internet of Things (IIoT) system, based on concepts from K. Eric Harper's "Industrial Internet Reference Architecture" (2015). This demonstrates concurrent processing of sensor data using Python's multiprocessing module to handle real-time streams, fault tolerance, and scalable analytics. Now enhanced with graphics visualization using Matplotlib and next-level project ideas.

## Features
- Virtual sensors generating random data (e.g., temperature, pressure) with fault simulation.
- Parallel workers processing data streams for aggregation, anomaly detection, and fault handling.
- Graphics: Generates plots of sensor data streams (saved as PNG).
- Advanced concurrency: Scaled-up sensors and processors for better parallelism demo.

## Installation
1. Clone the repo: `git clone https://github.com/NullLabTests/IIoT-Parallel-Simulator.git`
2. Install dependencies: `pip install -r requirements.txt`

## Usage
Run the simulator: `python main.py`

It will spawn multiple processes to handle sensor data in parallel, output aggregated results, and generate a plot (sensor_data_plot.png).

## Next-Level Ideas
See [IDEAS.md](IDEAS.md) for advanced extensions, including real hardware integration, ML analytics, and more.

## Inspiration
Drawn from Harper's work on IIoT architectures, emphasizing distributed concurrency for industrial scalability.

## License
MIT
