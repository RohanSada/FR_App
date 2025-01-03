import sys
sys.path.append('./FR_Server/Detector/')
sys.path.append('./FR_Server/Recognizer/')
from Detector import *
from Recognizer import *
import numpy as np

class FR():
    def __init__(self, detector_prototxt_path, detector_model_path, recognizer_model_path, db):
        self.detector = Detector(detector_prototxt_path, detector_model_path)
        self.recognizer = Recognizer(recognizer_model_path)
        self.db = db

    def register_face(self, image, label):
        embedding = self.recognizer.get_encoding(image)
        self.db.add_data(label, image, embedding)
    
    def compare_encodings(self, encoding1, encoding2):
        encoding1 = np.array(encoding1)
        encoding2 = np.array(encoding2)
        cosine_similarity = np.dot(encoding1, encoding2)
        return cosine_similarity

    def recognize_face(self, frame):
        cropped_images, bboxes = self.detector.get_cropped_images(frame)
        recognized_names = []
        for img in cropped_images:
            rec_usr = None
            rec_usr_score = -1
            embedding = self.recognizer.get_encoding(img)
            all_encodings = self.db.get_all_encodings() # {"Names": [], "Encodings": []}
            for idx in range(len(all_encodings['Names'])):
                similarity = self.compare_encodings(all_encodings['Encodings'][idx], embedding)
                if similarity > 0.5:
                    if similarity > rec_usr_score:
                        rec_usr = all_encodings['Names'][idx]
                        rec_usr_score = similarity
            recognized_names.append(rec_usr)
        return recognized_names, bboxes