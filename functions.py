import cv2
import os
from gtts import gTTS
import threading
from playsound import playsound
import time
from stat import ST_MTIME
import json

def text_to_speech(settings):
    modified = False
    date_modified, messages = [], []

    for text in os.listdir("messages"):
        if ".txt" in text:
            metadata = os.stat("messages/" + text)
            date_modified.append(metadata[ST_MTIME])

            with open("messages/" + text) as f:
                messages.append(f.read())

    try:
        with open("messages/metadata.json", "r") as f:
            json_data = json.load(f)

    except FileNotFoundError:
        with open("messages/metadata.json", "w") as f:
            json.dump(date_modified, f)

        for i, message in enumerate(messages):
            speech_file = gTTS(text=message, lang=settings.LANGUAGE)
            speech_file.save("messages/" + settings.LABEL_TEXT[i] + ".mp3")

    else:
        for i, data in enumerate(zip(date_modified, json_data)):
            if data[0] != data[1]:
                speech_file = gTTS(text=messages[i], lang=settings.LANGUAGE)
                speech_file.save("messages/" + settings.LABEL_TEXT[i] + ".mp3")

                modified = True

    if modified:
        with open("messages/metadata.json", "w") as f:
            json.dump(date_modified, f)

class playMessage(threading.Thread):
    def __init__(self, label, settings):
        super().__init__()

        self.file_path = "messages/" + label + ".mp3"
        self.settings = settings

    def run(self):
        self.settings.IS_SPEAKING = True

        playsound(self.file_path)
        time.sleep(1)

        self.settings.IS_SPEAKING = False

def detect_face(image, settings):
    net = cv2.dnn.readNetFromTensorflow(settings.MODEL_FILE, settings.CONFIG_FILE)
    blob = cv2.dnn.blobFromImage(image, settings.SCALE_FACTOR, settings.RESIZED_FRAME, [104, 117, 123], swapRB=True)

    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > settings.CONFIDENCE_BOUNDRY:
            x1 = int(detections[0, 0, i, 3] * settings.FRAME_WIDTH)
            y1 = int(detections[0, 0, i, 4] * settings.FRAME_HEIGHT)
            x2 = int(detections[0, 0, i, 5] * settings.FRAME_WIDTH)
            y2 = int(detections[0, 0, i, 6] * settings.FRAME_HEIGHT)

            return (x1, y1, x2, y2)
        
        else:
            return None

def recognize_face(image, rect_coords, face_recognizer, settings):
    face = image[rect_coords[1]:rect_coords[3], rect_coords[0]:rect_coords[2]]
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

    label, _ = face_recognizer.predict(gray)
    label = settings.LABEL_TEXT[label]

    return label