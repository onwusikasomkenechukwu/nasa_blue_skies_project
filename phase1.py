


"""
yolo8_detector.py

This module provides a clean wrapper around the Ultralytics YOLOv8 model.
It handles:
- Model loading
- Running inference
- Drawing bounding boxes on frames
"""

from ultralytics import YOLO
import cv2


class YOLOv8Detector:
    """
    YOLOv8Detector encapsulates the YOLOv8 object detection model.

    Attributes:
        model (YOLO): Loaded YOLO model instance.
        conf (float): Confidence threshold for filtering detections.
    """

    def __init__(self, model_path="yolov8n.pt", conf=0.35, device="cpu"):
        """
        Initializes the detector.

        Args:
            model_path (str): Path to YOLOv8 model weights.
            conf (float): Minimum confidence threshold.
            device (str): Device to run inference on ("cpu" or "cuda").
        """
        self.model = YOLO(model_path)
        self.model.to(device)
        self.conf = conf

    def detect(self, frame):
        """
        Runs object detection on a single frame.

        Args:
            frame (numpy.ndarray): Input image (BGR format).

        Returns:
            results[0]: YOLO detection result for the frame.
        """
        results = self.model(
            frame,
            conf=self.conf,
            imgsz=640,
            verbose=False
        )
        return results[0]

    def draw(self, frame, detections):
        """
        Draws bounding boxes and labels on the frame.

        Args:
            frame (numpy.ndarray): Original image frame.
            detections: YOLO detection output.

        Returns:
            numpy.ndarray: Frame with bounding boxes drawn.
        """
        for box in detections.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            label = f"{self.model.names[cls]} {conf:.2f}"

            # Draw bounding rectangle
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw label above bounding box
            cv2.putText(
                frame,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )

        return frame


#Image Preprocessing (Optimized for Aircraft Surfaces)
import cv2
import numpy as np

def preprocess(frame):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    return cv2.merge((l,a,b))

#Rover Vision Loop
import cv2
from rover.comms.mcu_bridge import MCUBridge
from rover.navigation.rover_planner import RoverPlanner
from rover.vision.preprocessing import preprocess
from shared.ai.yolo8_detector import YOLOv8Detector

mcu = MCUBridge()
planner = RoverPlanner(mcu)

detector = YOLOv8Detector(
    model_path="models/yolov8n_aircraft.pt",
    conf=0.35,
    device="cuda"  # "cpu" if Raspberry Pi
)

cap = cv2.VideoCapture(0)
mcu.magnets(True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    proc = preprocess(frame)
    detections = detector.detect(proc)

    if len(detections.boxes) > 0:
        planner.stop()
        print("⚠️ Surface anomaly detected")
    else:
        planner.move_forward(45)


"""
- crack
- corrosion
- dent
- paint_peel
- fastener_missing

"""