import cv2
import os
import numpy as np

from functions import detect_face
from settings import Settings

def prepare_data(settings):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    dirs = os.listdir(settings.TRAINING_DATA)

    faces, labels = [], []

    for label, folder in enumerate(dirs):
        subject_path = settings.TRAINING_DATA + "/" + folder
        subject_images = os.listdir(subject_path)

        for image_name in subject_images:
            image_path = subject_path + "/" + image_name

            image = cv2.imread(image_path)
            resized = cv2.resize(image, settings.RESIZED_FRAME)
            settings.FRAME_WIDTH, settings.FRAME_HEIGHT, _ = resized.shape

            rect = detect_face(image, settings)
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

            faces.append(gray[rect[1]:rect[3], rect[0]:rect[2]])
            
            labels.append(label)

    return faces, labels

settings = Settings()

faces, labels = prepare_data(settings)
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))
face_recognizer.write(settings.RECOGNIZER_FILE)