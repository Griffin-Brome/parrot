# TODO sanitize input, upload random paragraph, user account functionality (mysql?)

import parrot
from flask import Flask, flash, request, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload-file', methods=['GET', 'POST']) 
def upload_file():
    if request.method == 'POST':
        if request.files:
            file = (request.files['file'])
            return redirect(request.url)
    return render_template("index.html")

@app.route('/text')
def text_output(paragraph=None): #TODO change this value
    return render_template('text.html')