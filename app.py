from datetime import timedelta
from flask import Flask, render_template
import requests_cache


app = Flask(__name__)


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


# main driver function
if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=5000,threaded=True)
    app.run(debug=True)
