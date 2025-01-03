import cv2
import tensorflow as tf
import sys
import numpy as np
from keras_facenet import FaceNet

class Recognizer():
    def __init__(self, model_path):
        self.recognizer = FaceNet()

    def pre_process(self, img):
        image = cv2.resize(img, (160, 160))
        image = np.expand_dims(image, axis=0)
        return image

    def get_encoding(self, img):
        img = self.pre_process(img)
        encoding = self.recognizer.embeddings(img)
        encoding = encoding.tolist()
        return encoding[0]
    