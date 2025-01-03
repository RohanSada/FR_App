from flask import Flask, render_template, request, jsonify
import base64
import sys
from FR_Server.FR import *
from FR_Server.utils.db import *
import json
import numpy as np
import cv2
import argparse
import time

class MyFlaskApp:
    def __init__(self, config_file):
        config_data = self.read_config(config_file)
        self.db = MongoDB(config_data['MongoDB']['url'], config_data['MongoDB']['database_name'], config_data['MongoDB']['collection_name'])
        self.app = Flask(__name__, template_folder='./FR_UI/templates', static_folder='./FR_UI/static')
        self.host = config_data["Server_Details"]['Host']
        self.port = config_data["Server_Details"]['Port']
        self.fr = FR(config_data['Detector']["prototxt_path"], config_data['Detector']['model_path'], config_data['Recognizer']['model_path'], self.db)
        self._add_routes()

    def read_config(self, config_path):
        with open(config_path, "r") as file:
            data = json.load(file)
        return data

    def _add_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/register.html')
        def register():
            return render_template('register.html')

        @self.app.route('/detect.html')
        def detect():
            return render_template('detect.html')
        
        @self.app.route('/register_face', methods=['POST'])
        def register_face():
            try:
                data = request.get_json()
                label = data.get('label')
                cropped_image_url = data.get('croppedImageURL')

                if not label or not cropped_image_url:
                    return jsonify({'error': 'Label and image are required.'}), 400

                base64_data = cropped_image_url.split(",")[1]
                image_data = base64.b64decode(base64_data)
                np_image = np.frombuffer(image_data, np.uint8)
                cv2_image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
                self.fr.register_face(cv2_image, label)
                return jsonify({'message': 'Face registered successfully.'}), 200
            except Exception as e:
                print(f"Error: {e}")
                return jsonify({'error': 'An error occurred while processing the image.'}), 500

        @self.app.route('/get_bbox', methods=['POST'])
        def get_bbox():
            data = request.json.get("imageData")
            if not data:
                return jsonify({"error": "No image data provided"}), 400
            
            image_data = base64.b64decode(data.split(',')[1])
            np_image = np.frombuffer(image_data, np.uint8)
            cv2_image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
            bboxes = self.fr.detector.get_bounding_boxes(cv2_image)
            return jsonify({"BoundingBoxes": bboxes})

        @self.app.route('/detect_face', methods=['POST'])
        def detect_face():
            try:
                t1 = time.time()
                data = request.get_json()

                frame_data = data.get('image')
                if frame_data.startswith('data:image'):
                    header, frame_data = frame_data.split(',', 1)

                image_data = base64.b64decode(frame_data)
                np_image = np.frombuffer(image_data, np.uint8)
                cv2_image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
                names, bboxes = self.fr.recognize_face(cv2_image)
                t2 = time.time()
                print("Recognized time: ", t2-t1)
                return jsonify({"BoundingBoxes": bboxes, "Names": names}), 200
            except Exception as e:
                print(e)
                return jsonify({"BoundingBoxes": [], "Names": []}), 200
            
    def run(self):
        self.app.run(host=self.host, port=self.port, debug=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run server with config file")
    parser.add_argument(
        "config_file",
        type=str,
        help="Path to the configuration file (e.g., ./config.json)"
    )
    args = parser.parse_args()
    app_instance = MyFlaskApp(args.config_file)
    app_instance.run()