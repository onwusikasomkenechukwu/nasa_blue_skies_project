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
├── Diagram.png
├── README.txt
├── Vision Code Layout (Raspberry Pi).txt
├── machinevision.py
├── main.py
├── rovermain.py
├── phase1.py
├── outline.txt
└── requirements.txxt
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
File Descriptions

`Diagram.png`

High-level system diagram illustrating:

* Rover and drone roles
* Sensor placement
* Data flow between vision, control, and backend systems

Used for documentation, presentations, and design reviews.

---

`Vision Code Layout (Raspberry Pi).txt`

Describes the **intended modular vision architecture** for the Raspberry Pi deployment, including:

* Camera driver
* YOLO model wrapper
* Inference throttling and persistence
* Network upload logic

This file serves as a software design reference and target architecture for refactoring existing scripts into a clean module-based system.

---

`machinevision.py`

Prototype implementation of the **computer vision pipeline**, including:

* Camera capture
* YOLO-based inference
* Initial detection logic

This file is used for early testing and validation of model performance on embedded hardware.

---

`main.py`

Primary entry point for general system testing and integration.

Responsibilities may include:

* Initializing vision components
* Running test loops
* Verifying runtime behavior during development

This file is expected to evolve as modules are finalized.

---

`rovermain.py`

Rover-specific runtime script.

Intended responsibilities:

* Integrating vision with rover motion control
* Handling rover state and safety logic
* Coordinating inspection behavior while attached to aircraft surfaces

This file separates rover logic from drone or general-purpose testing code.

---

`phase1.py`

Implements Phase 1 system objectives, including:

* Proof-of-concept vision functionality
* Basic inspection workflow
* Early integration testing

Used to track progress against project milestones and deliverables.

---

`outline.txt`

Development planning document outlining:

* Project phases
* Feature priorities
* Future integration steps

Serves as a roadmap for continued development.

---

`requirements.txxt`

Lists Python dependencies required to run the software.

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
