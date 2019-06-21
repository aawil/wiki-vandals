from flask import Flask, Response, request, render_template, jsonify
import json
import pandas as pd
from wtforms import StringField, SubmitField, Form
from api import *

# Initialize the app

app = Flask(__name__)

pcts = pd.read_pickle("static/geog_damage.pkl")
top_articles = pd.read_pickle("static/geog_top_articles.pkl")
top_vandalized = pd.read_pickle("static/geog_top_vandalized.pkl")
geogs = list(pcts.index)

class SearchForm(Form):
    autocomp = StringField('Country, state, city, or ZIP:', id='geog_autocomplete')
    button = SubmitField('Go!', id='submit')


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = SearchForm(request.form)
    return render_template('index.html', form=form)

@app.route("/autocomplete", methods=['GET'])
def autocomplete():
    return Response(json.dumps(geogs), mimetype='application/json')

@app.route("/showresults")
def showresults():
    geog = request.args.get('geog')
    pct_diff = int(pcts.loc[geog][0])

    result = f"Edits coming from {geog} are "
    if pct_diff > 0:
        result += f"<b>{pct_diff}% MORE</b> damaging than average!"
    elif pct_diff < 0:
        pct_diff = abs(pct_diff)
        result += f"<b>{pct_diff}% LESS</b> damaging than average!"
    else:
        result += f"no more or less damaging than average!"

    result += "<br/><br/>"
    result += "<b>Most <i>edited</i> articles</b>:<br/>"

    if geog in top_articles.index:
        titles = top_articles.loc[geog]['rc_title']
        if type(titles)==str:
            result += title_to_link(titles)
            result += "<br/>"
        else:
            for title in titles:
                result += title_to_link(title)
                result += "<br/>"
    else:
        result += "Sorry, no data!"

    result += "<br/>"
    result += "<b>Most <i>vandalized</i> articles</b>:<br/>"

    if geog in top_vandalized.index:
        titles = top_vandalized.loc[geog]['rc_title']
        if type(titles)==str:
            result += title_to_link(titles)
            result += "<br/>"
        else:
            for title in titles:
                result += title_to_link(title)
                result += "<br/>"
    else:
        result += "Sorry, no data!"

    return result

if __name__=="__main__":
    # For local development:
    # app.run(debug=True)
    # For public web serving:
    #app.run(host='0.0.0.0')
    app.run()
