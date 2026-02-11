import cv2

def preprocess(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    return blur

from ultralytics import YOLO

class CrackDetector:
    def __init__(self, model_path="models/crack_yolo.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, conf=0.4)
        return results


import torch
import torchvision.transforms as T

class CorrosionSegmenter:
    def __init__(self, model):
        self.model = model.eval()

    def segment(self, image):
        x = T.ToTensor()(image).unsqueeze(0)
        with torch.no_grad():
            mask = self.model(x)
        return mask
