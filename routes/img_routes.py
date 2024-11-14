from flask import Blueprint, request, jsonify
from services.img_service import ImgService

img_bp = Blueprint("model", __name__)

@img_bp.route('/ocr', methods=['POST'])
def img_txt():
    data = request.get_json()
    response = ImgService.create_text(data)
    #print("\nData From Img_routes\n", response)
    return response