import cv2
import threading

from settings import Settings
from functions import detect_face, recognize_face, text_to_speech, playMessage

cap = cv2.VideoCapture(0)

settings = Settings()
settings.set_conditions(cap)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(settings.RECOGNIZER_FILE)

while True:
    _, frame = cap.read()
    rect_coords = detect_face(frame, settings)

    text_to_speech(settings)

    if rect_coords:
        label = recognize_face(frame, rect_coords, face_recognizer, settings)

        cv2.rectangle(frame, (rect_coords[0], rect_coords[1]), (rect_coords[2], rect_coords[3]), settings.RECTANGLE_COLOUR, 2)
        cv2.putText(frame, label.title(), (rect_coords[0], rect_coords[3]+27), cv2.FONT_HERSHEY_SIMPLEX, 1, settings.RECTANGLE_COLOUR, 2)

        if not settings.IS_SPEAKING:
            play_message = playMessage(label, settings)
            play_message.start()
    
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()