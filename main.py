"""
main_rover_vision.py

Main runtime loop for rover inspection system.

Responsibilities:
- Capture camera frames
- Preprocess image
- Run YOLO detection
- Command rover movement
- Stop rover on anomaly detection
"""

import cv2
import sys
from shared.ai.yolo8_detector import YOLOv8Detector
from rover.vision.preprocessing import preprocess


# ---- MOCK IMPLEMENTATIONS (Replace with real hardware modules) ---- #

class MCUBridge:
    """
    Handles communication between the computer and rover microcontroller.
    Responsible for sending motor and magnet commands.
    """

    def __init__(self):
        print("MCU Bridge Initialized")

    def send_motor_command(self, left_speed, right_speed):
        """
        Sends motor speed values to rover.

        Args:
            left_speed (int): Left motor speed (-100 to 100)
            right_speed (int): Right motor speed (-100 to 100)
        """
        print(f"Motors → Left: {left_speed}, Right: {right_speed}")

    def magnets(self, state: bool):
        """
        Controls magnetic adhesion system.

        Args:
            state (bool): True = ON, False = OFF
        """
        print(f"Magnets {'ON' if state else 'OFF'}")

    def stop_all(self):
        """
        Emergency stop for rover.
        """
        self.send_motor_command(0, 0)
        print("Emergency Stop Activated")


class RoverPlanner:
    """
    High-level motion planner for rover.
    Converts abstract commands into motor instructions.
    """

    def __init__(self, mcu_bridge: MCUBridge):
        self.mcu = mcu_bridge

    def move_forward(self, speed=40):
        """
        Moves rover forward.

        Args:
            speed (int): Forward speed percentage.
        """
        self.mcu.send_motor_command(speed, speed)

    def stop(self):
        """
        Stops rover movement.
        """
        self.mcu.stop_all()


# ------------------ MAIN EXECUTION LOOP ------------------ #

def main():
    """
    Entry point of rover vision system.
    """

    # Initialize hardware communication
    mcu = MCUBridge()
    planner = RoverPlanner(mcu)

    # Initialize detector
    detector = YOLOv8Detector(
        model_path="models/yolov8n_aircraft.pt",
        conf=0.35,
        device="cuda"  # Use "cpu" on Raspberry Pi
    )

    # Open camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        sys.exit(1)

    # Activate magnetic adhesion
    mcu.magnets(True)

    print("Rover Vision System Started")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Frame capture failed")
                break

            # Preprocess frame
            processed = preprocess(frame)

            # Run detection
            detections = detector.detect(processed)

            # Draw detection boxes
            frame_with_boxes = detector.draw(frame.copy(), detections)

            # Decision logic
            if len(detections.boxes) > 0:
                planner.stop()
                print("⚠️ Surface anomaly detected")
            else:
                planner.move_forward(45)

            # Display window
            cv2.imshow("Rover Vision", frame_with_boxes)

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user")

    finally:
        print("Shutting down safely...")

        planner.stop()
        mcu.magnets(False)

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
