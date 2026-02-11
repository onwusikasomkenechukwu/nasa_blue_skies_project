Embedded Vision Pipeline (Raspberry Pi) - README

This directory contains the onboard computer vision pipeline used by the A.N.T.S. (Autonomous Navigation Technician Swarm) rover and drone platforms. The software is designed to run on a Raspberry Pi-class embedded system and perform reliable, low-power surface defect detection using a YOLOv8n model.

The architecture prioritizes stability, power efficiency, and deployability over raw inference throughput, making it suitable for safety-critical robotic inspection tasks.

---

System Overview

The vision system performs the following functions:

1. Captures images from an onboard camera
2. Runs controlled YOLOv8n inference on selected frames
3. Filters detections using temporal persistence
4. Uploads confirmed defect images and metadata to a backend service

All processing is performed on-device, with only validated results transmitted offboard.

---

Directory Structure

```
vision/
├── config.yaml          # Runtime configuration (no code changes needed)
├── camera_driver.py     # Lightweight camera interface
├── model.py             # YOLOv8 model wrapper (loads once)
├── infer.py             # Minimal detection parsing
├── utils.py             # Inference throttling + persistence logic
├── uploader.py          # Non-blocking HTTP upload
├── vision_loop.py       # Main runtime loop
└── weights/
    └── yolov8n.pt       # Trained YOLOv8n weights
```

Each module has a single responsibility, allowing the system to scale or adapt to new hardware with minimal refactoring.

---

Configuration (`config.yaml`)

All performance-critical parameters are defined in `config.yaml`, allowing tuning without modifying source code.

Key settings include:

* Camera resolution and frame rate
* Inference image size and confidence threshold
* Inference throttling interval
* Detection persistence across frames
* Network upload endpoint
* Device identifier

This configuration-driven approach enables rapid adaptation to different lighting conditions, surfaces, and power budgets.

---

Core Components

Camera Interface (`camera_driver.py`)

* Uses OpenCV for direct camera access
* Explicitly sets resolution to avoid CPU overload
* Designed to fail gracefully if frames cannot be read

Model Wrapper (`model.py`)

* Loads YOLOv8n weights once at startup
* Prevents repeated initialization and memory fragmentation
* Abstracts model internals from the rest of the system

Detection Parsing (`infer.py`)

* Extracts only essential information:

  * Class label
  * Confidence score
* Avoids passing large tensors or raw model outputs downstream

Inference Control (`utils.py`)

Implements two key reliability mechanisms:

* **Inference throttling**: Limits how often inference runs to prevent CPU saturation and thermal throttling
* **Temporal persistence**: Requires detections to appear across multiple frames before being confirmed

This trades latency for improved confidence and robustness.

Upload Interface (`uploader.py`)

* Encodes images as JPEG and Base64
* Sends compact JSON payloads via HTTP POST
* Enforces timeouts to prevent blocking the main loop

Only confirmed detections are transmitted, conserving bandwidth and backend resources.

---

Main Runtime Loop (`vision_loop.py`)

`vision_loop.py` orchestrates the entire pipeline:

1. Capture frame
2. Check inference throttle
3. Run YOLO inference
4. Parse and validate detections
5. Upload confirmed results

The loop is event-driven, not frame-driven, ensuring predictable behavior and long-term stability during continuous operation.

---

Model Details

* Model: YOLOv8n
* Framework: Ultralytics YOLO
* Training: Offline (Roboflow Universe dataset)
* Deployment: CPU-only inference on Raspberry Pi

YOLOv8n was selected for its balance of speed, size, and accuracy under embedded constraints.

---

Requirements

* Python 3.8+
* OpenCV
* Ultralytics YOLO
* PyYAML
* Requests

Example install:

```bash
pip install ultralytics opencv-python pyyaml requests
```

---

Usage

1. Place trained weights in `weights/yolov8n.pt`
2. Update `config.yaml` as needed
3. Run:

```bash
python vision_loop.py
```

On startup, the system will initialize the camera and model and begin monitoring for surface defects.

---

Design Philosophy

This system is built on the principle that embedded machine vision is a systems engineering problem, not just a machine learning problem. Reliable autonomy is achieved through:

* Controlled inference frequency
* Defensive programming
* Clear data contracts
* Modular design

---

Notes

* This pipeline is shared between rover and drone platforms
* Backend endpoints are assumed to be available but are decoupled from vision logic
* The system is designed to scale to higher-performance hardware (e.g., Jetson Nano) with minimal changes

---