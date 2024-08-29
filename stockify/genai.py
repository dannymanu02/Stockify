import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv

from io import BytesIO

import base64

import os

load_dotenv()

class responseGenerator:

    api_key = "AIzaSyBEYQX9IKFpZTdO7h-TbhgP7NcL3kiVGRY"
    genai.configure(api_key="AIzaSyBEYQX9IKFpZTdO7h-TbhgP7NcL3kiVGRY")
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def __init__(self) -> None:
        pass

    def gen_ai_text_generate(self, text, image):
        image_data = base64.b64decode(image)
        img = PIL.Image.open(BytesIO(image_data))
        response = self.model.generate_content([text, img])
        return response.text