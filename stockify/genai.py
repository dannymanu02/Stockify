import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv

import os

load_dotenv()

class responseGenerator:

    api_key = "AIzaSyBEYQX9IKFpZTdO7h-TbhgP7NcL3kiVGRY"
    genai.configure(api_key="AIzaSyBEYQX9IKFpZTdO7h-TbhgP7NcL3kiVGRY")
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def __init__(self) -> None:
        pass

    def gen_ai_text_generate(self, text, image):
        img = PIL.Image.open(image)
        response = self.model.generate_content([text, img])
        return response.text