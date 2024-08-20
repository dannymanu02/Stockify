from flask import Flask, render_template, request

from stockify.getData import dataAnalytics

import os
from dotenv import load_dotenv

from stockify.genai import responseGenerator

app = Flask(__name__, static_folder='static')

def perform_analytics(name):
    da = dataAnalytics(name=name)
    
    comp = da.fetch_company_details(name)
    
    data = da.get_historical_data(name)

    da.plot_closing_prices(data)

    da.plot_volume_traded(data)

    da.plot_intraday_diff(data)

    da.plot_intraday_change_trend(data)

    da.plot_decomposition(data)

    crisis_data, covid_data = da.get_crisis_covid_data(data)

    da.plot_rec_analysis(crisis_data)

    da.plot_covid_analysis(covid_data)

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

    responses.append(rg.gen_ai_text_generate(cpot, "static/"+company+'_cpot.png'))
    responses.append(rg.gen_ai_text_generate(vtot, "static/"+company+'_vtot.png'))
    responses.append(rg.gen_ai_text_generate(iddot, "static/"+company+'_iddot.png'))
    responses.append(rg.gen_ai_text_generate(idctot, "static/"+company+'_idctot.png'))
    responses.append(rg.gen_ai_text_generate(dec, "static/"+company+'_dec.png'))
    responses.append(rg.gen_ai_text_generate(crisis_cpot, "static/"+company+'_crisis_cpot.png'))
    responses.append(rg.gen_ai_text_generate(crisis_vtot, "static/"+company+'_crisis_vtot.png'))
    responses.append(rg.gen_ai_text_generate(crisis_dec, "static/"+company+'_crisis_dec.png'))
    responses.append(rg.gen_ai_text_generate(covid_cpot, "static/"+company+'_covid_cpot.png'))
    responses.append(rg.gen_ai_text_generate(covid_vtot, "static/"+company+'_covid_vtot.png'))
    responses.append(rg.gen_ai_text_generate(covid_dec, "static/"+company+'_covid_dec.png'))

    return responses

# @app.after_request
# def delete_files(response):
#     static_dir = os.path.join(app.root_path, 'static')
    
#     for filename in os.listdir(static_dir):
#         file_path = os.path.join(static_dir, filename)
#         if os.path.isfile(file_path):
#             os.remove(file_path)
    
#     return response


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/main", methods = ["POST"])
def main_page():
    company = request.form.get('search_query')

    comp = perform_analytics(company)

    generated_text = genai_text(company)

    return render_template('main.html', company = company.upper(), res = comp, gen_text = generated_text)

if __name__ == '__main__':
    app.run(debug=True)
