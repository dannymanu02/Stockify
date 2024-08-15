import google.generativeai as genai
import PIL.Image
import os

genai.configure(api_key="AIzaSyBEYQX9IKFpZTdO7h-TbhgP7NcL3kiVGRY")
img = PIL.Image.open('static/JPM_covid_cpot.png')

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
tail = ", what inferences can  be made from this chart? limit is 500 words. Generate text as HTML unordered list so that it's easy to display in a html page. This text is being sent to a html page to render and this is a flask application. Make sure that the text is rendered properly. Don't include html tags, head tags and body tags, just the unordered list tags. Don't include markdown content as well, use the corresponding html tags wherever markdown is there."
cpot = f"This is a chart of closing prices of each day of jpm over time since it's inception in the market{tail}"
response = model.generate_content([cpot, "static/orcl_cpot.png"])

print(response.text)