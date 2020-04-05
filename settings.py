import cv2
import os

class Settings():
    def __init__(self):
        self.MODEL_FILE = "detection_models/opencv_face_detector_uint8.pb"
        self.CONFIG_FILE = "detection_models/opencv_face_detector.pbtxt"
        self.RECOGNIZER_FILE = "detection_models/face_recognizer.yml"
        self.TRAINING_DATA = "training_data"
        
        self.SCALE_FACTOR = 1.3
        self.CONFIDENCE_BOUNDRY = 0.6

        self.LABEL_TEXT = []

        self.RESIZED_FRAME = (300, 300)
        self.FRAME_WIDTH = None
        self.FRAME_HEIGHT = None
        
        self.RECTANGLE_COLOUR = (0 ,0, 255)

        self.IS_SPEAKING = False
        self.LANGUAGE = "en"
    
    def set_conditions(self, cap):
        self.FRAME_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.FRAME_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        for dir in os.listdir(self.TRAINING_DATA):
            self.LABEL_TEXT.append(dir)