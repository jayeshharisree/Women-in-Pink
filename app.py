from datetime import timedelta
from flask import Flask, render_template,request,redirect, jsonify, abort
import flask_monitoringdashboard as dashboard
import requests_cache
import numpy as np
import pandas as pd
import pickle
import db
import json


expire_after = timedelta(minutes=30)
requests_cache.install_cache('main_cache',expire_after=expire_after)

app = Flask(__name__)
dashboard.bind(app)

model = pickle.load(open('model.pkl', 'rb'))



@app.template_filter()
def numberFormat(value):
    return format(int(value), ',d')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/faq')
def faq():
    return render_template("faq.html")


@app.route('/prevention')
def prevention():
    return render_template("prevention.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/diagnosis')
def diagnosis():
    return render_template("Diagnosis.html")


@app.route('/types')
def types():
    return render_template("types.html")


@app.route('/stages')
def stages():
    return render_template("stages.html")


@app.route('/facts')
def facts():
    return render_template("facts.html")


@app.route('/detection',methods=['GET','POST'])
def detection():
    if request.method == 'GET':
        return render_template('detection.html')
    else:
        input_features = [float(x) for x in request.form.values()]
        features_value = [np.array(input_features)]

        features_name = ['mean radius', 'mean texture', 'mean perimeter', 'mean area',
                         'mean smoothness', 'mean compactness', 'mean concavity',
                         'mean concave points', 'mean symmetry', 'mean fractal dimension',
                         'radius error', 'texture error', 'perimeter error', 'area error',
                         'smoothness error', 'compactness error', 'concavity error',
                         'concave points error', 'symmetry error', 'fractal dimension error',
                         'worst radius', 'worst texture', 'worst perimeter', 'worst area',
                         'worst smoothness', 'worst compactness', 'worst concavity',
                         'worst concave points', 'worst symmetry', 'worst fractal dimension']

        df = pd.DataFrame(features_value, columns=features_name)
        output = model.predict(df)

        if output == 0:
            res_val = "** breast cancer **"
        else:
            res_val = "no breast cancer"

        return render_template('detection.html', prediction_text='Patient has {}'.format(res_val))


@app.route('/subscribed/<email>')
def subscribed(email):
    if(db.validateuser(email)):
        return render_template('subscribed.html')
    else:
        text='Email does not exist.'
        return render_template('error.html', text=text, again=True)


@app.route('/unsubscribe/<email>')
def unsubscribe(email):
    if(db.deluser(email)):
        return render_template('unsubscribed.html')
    else:
        text='You are not subscribed to this newsletter.'
        return render_template('error.html',text=text, again=False)


@app.route('/users')
def getusers():
    return str(db.getusers())


@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.form
    email = data['email'].strip()

    if db.adduser(email):
        return render_template('index.html')
    else:
        text = 'User Already Exists'
        return render_template('index.html', text=text, again=True)


# main driver function
if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=5000,threaded=True)
    app.run(debug=True)
