import tensorflow as tf
import cv2 
import numpy as np

class Detector():
    def __init__(self, prototxt_path, model_path, threshold=0.5):
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        self.threshold = threshold

    def PreprocessImage(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
        return blob
    
    def detect(self, frame):
        blob = self.PreprocessImage(frame)
        self.net.setInput(blob)
        detections = self.net.forward()
        return detections

    def get_bounding_boxes(self, frame):
        bboxes = []
        detections = self.detect(frame)
        (h, w) = frame.shape[:2]
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.threshold:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                startX, startY, endX, endY = box.astype("int")
                bboxes.append([int(startX), int(startY), int(endX), int(endY)])
        return bboxes

    def get_cropped_images(self, frame):
        bboxes = self.get_bounding_boxes(frame)
        cropped_images = []
        for bbox in bboxes:
            startX, startY, endX, endY = bbox
            cropped_img = frame[startY:endY, startX:endX]
            cropped_images.append(cropped_img)
        return cropped_images, bboxes

    def detectAndCrop(self, frame):
        (h, w) = frame.shape[:2]
        detections = self.detect(frame)
        confidence = detections[0, 0, 0, 2]
        if confidence > self.threshold:
            box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            cropped_img = frame[startY:endY, startX:endX]
            return cropped_img, (startX, startY, endX, endY)
        return frame, (0, 0, 0, 0)

    def detectAndDraw(self, frame):
        (h, w) = frame.shape[:2]
        detections = self.detect(frame)
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > self.threshold:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                text = f"{confidence * 100:.2f}%"
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                cv2.putText(frame, text, (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame
