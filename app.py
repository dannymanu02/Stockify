from flask import Flask, render_template, request

from stockify.getData import dataAnalytics

import os
from dotenv import load_dotenv

from stockify.genai import responseGenerator

from PIL import Image

import base64

app = Flask(__name__, static_folder='static')

plots = []
images = []

def perform_analytics(name):

    da = dataAnalytics(name=name)
    
    comp = da.fetch_company_details(name)
    
    data = da.get_historical_data(name)

    plots.append(da.plot_closing_prices(data))

    plots.append(da.plot_volume_traded(data))

    plots.append(da.plot_intraday_diff(data))

    plots.append(da.plot_intraday_change_trend(data))

    plots.append(da.plot_decomposition(data))

    crisis_data, covid_data = da.get_crisis_covid_data(data)

    plots.append(da.plot_rec_analysis(crisis_data))

    plots.append(da.plot_covid_analysis(covid_data))

    return comp

def genai_text(company):

    responses = []

    tail = ", what inferences can  be made from this chart? limit is 500 words. Generate text as HTML unordered list so that it's easy to display in a html page. This text is being sent to a html page to render and this is a flask application. Make sure that the text is rendered properly. Don't include html tags, head tags and body tags, just the unordered list tags. Don't include markdown content as well, use the corresponding html tags wherever markdown is there."
    cpot = f"This is a chart of closing prices of each day of {company} over time since it's inception in the market{tail}"
    vtot = f"This is a chart of volumes traded in a particular day of {company} over time since it's inception in the market{tail}"
    iddot = f"This is a chart of absolute difference between the closing and opening prices for each day of {company} over time since it's inception in the market{tail}"
    idctot = f"In the previous chart we had absolute difference, in this chart we have the signs which are positive and negative{tail}"
    dec = f"This is a chart of decomposition(additive type) for the closing prices of {company}'s stock{tail}"
    crisis_cpot = f"This is a chart of closing prices of each day of {company} during the 2008-09 recession{tail}"
    crisis_vtot = f"This is a chart of volumes traded in a particular day of {company} during the 2008-09 recession{tail}"
    crisis_dec = f"This is a chart of decomposition(additive type) for the closing prices of {company}'s stock during the 2008-09 recession{tail}"
    covid_cpot = f"This is a chart of closing prices of each day of {company} during the covid period{tail}"
    covid_vtot = f"This is a chart of volumes traded in a particular day of {company} during the covid period{tail}"
    covid_dec = f"This is a chart of decomposition(additive type) for the closing prices of {company}'s stock during the covid period{tail}"

    rg = responseGenerator()

    cpot_img = plots[0]
    cpot_img = base64.b64encode(cpot_img.getvalue()).decode('utf-8')
    images.append(cpot_img)
    vtot_img = plots[1]
    vtot_img = base64.b64encode(vtot_img.getvalue()).decode('utf-8')
    images.append(vtot_img)
    iddot_img = plots[2]
    iddot_img = base64.b64encode(iddot_img.getvalue()).decode('utf-8')
    images.append(iddot_img)
    idctot_img = plots[3]
    idctot_img = base64.b64encode(idctot_img.getvalue()).decode('utf-8')
    images.append(idctot_img)
    dec_img = plots[4]
    dec_img = base64.b64encode(dec_img.getvalue()).decode('utf-8')
    images.append(dec_img)

    crisis_cpot_img = plots[5][0]
    crisis_cpot_img = base64.b64encode(crisis_cpot_img.getvalue()).decode('utf-8')
    images.append(crisis_cpot_img)
    crisis_vtot_img = plots[5][1]
    crisis_vtot_img = base64.b64encode(crisis_vtot_img.getvalue()).decode('utf-8')
    images.append(crisis_vtot_img)
    crisis_dec_img = plots[5][2]
    crisis_dec_img = base64.b64encode(crisis_dec_img.getvalue()).decode('utf-8')
    images.append(crisis_dec_img)

    covid_cpot_img = plots[6][0]
    covid_cpot_img = base64.b64encode(covid_cpot_img.getvalue()).decode('utf-8')
    images.append(covid_cpot_img)
    covid_vtot_img = plots[6][1]
    covid_vtot_img = base64.b64encode(covid_vtot_img.getvalue()).decode('utf-8')
    images.append(covid_vtot_img)
    covid_dec_img = plots[6][2]
    covid_dec_img = base64.b64encode(covid_dec_img.getvalue()).decode('utf-8')
    images.append(covid_dec_img)

    # images.append(img_base64)
    responses.append(rg.gen_ai_text_generate(cpot, cpot_img))
    responses.append(rg.gen_ai_text_generate(vtot, vtot_img))
    responses.append(rg.gen_ai_text_generate(iddot, iddot_img))
    responses.append(rg.gen_ai_text_generate(idctot, idctot_img))
    responses.append(rg.gen_ai_text_generate(dec, dec_img))
    responses.append(rg.gen_ai_text_generate(crisis_cpot, crisis_cpot_img))
    responses.append(rg.gen_ai_text_generate(crisis_vtot, crisis_vtot_img))
    responses.append(rg.gen_ai_text_generate(crisis_dec, crisis_dec_img))
    responses.append(rg.gen_ai_text_generate(covid_cpot, covid_cpot_img))
    responses.append(rg.gen_ai_text_generate(covid_vtot, covid_vtot_img))
    responses.append(rg.gen_ai_text_generate(covid_dec, covid_dec_img))

    return responses

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/main", methods = ["POST"])
def main_page():
    company = request.form.get('search_query')

    comp = perform_analytics(company)

    generated_text = genai_text(company)

    return render_template('main.html', company = company.upper(), res = comp, gen_text = generated_text, images = images)

if __name__ == '__main__':
    app.run(debug=True)
