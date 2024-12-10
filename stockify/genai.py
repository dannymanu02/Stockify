import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv

from io import BytesIO

import base64

import os

import time
load_dotenv()

class responseGenerator:

    api_key = os.getenv("API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def __init__(self) -> None:
        self.last_request_time = 0 
        self.request_interval = 1

    def gen_ai_text_generate(self, text, image):
        current_time = time.time()
        if current_time - self.last_request_time < self.request_interval:
            time.sleep(self.request_interval - (current_time - self.last_request_time))

        image_data = base64.b64decode(image)
        img = PIL.Image.open(BytesIO(image_data))
        try:
            response = self.model.generate_content([text, img])
        except Exception as e:
            print(f"Error: {e}")
            response = None
        self.last_request_time = time.time()
        return response.text if response else "Quota exceeded, try again later."