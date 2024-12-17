from flask import Blueprint, request, jsonify
import cv2
import numpy as np
from app.models.vision_model import VisionModel

vision_bp = Blueprint('vision', __name__)
vision_model = VisionModel()

@vision_bp.route('/vision/analyze', methods=['POST'])
def analyze_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        image_file = request.files['image']
        image_array = cv2.imdecode(
            np.frombuffer(image_file.read(), np.uint8),
            cv2.IMREAD_COLOR
        )
        
        result = vision_model.analyze(image_array)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
