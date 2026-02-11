import cv2
from comms.mcu_bridge import MCUBridge
from navigation.rover_planner import RoverPlanner
from vision.preprocessing import preprocess
from shared.ai.crack_detection import CrackDetector

mcu = MCUBridge()
planner = RoverPlanner(mcu)
detector = CrackDetector()

cap = cv2.VideoCapture(0)

mcu.magnets(True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    processed = preprocess(frame)
    detections = detector.detect(frame)

    if len(detections[0].boxes) > 0:
        planner.stop()
        print("Damage detected")
    else:
        planner.move_forward(50)
