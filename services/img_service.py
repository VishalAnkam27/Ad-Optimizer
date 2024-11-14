from models.img import Img

class ImgService:
    @staticmethod
    def create_text(data):
        return Img.img_txt(data)