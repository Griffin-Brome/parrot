import parrot
import os
from flask import (Flask, flash, request, redirect, url_for, 
    render_template, session)
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './var/www/uploads'
ALLOWED_EXTENSIONS = {'txt'}
SECRET_KEY = 'PppZt00xEdHalhWKkb_Lpw'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-file', methods=['GET', 'POST']) 
def upload_file():
    if len(os.listdir(app.config['UPLOAD_FOLDER'])) > 0:
        purge_uploads()

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect('/')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            flash('File successfully uploaded')
            session['current_file'] = filename
            return redirect('/')
        else:
            flash('Filetype not supported')
            return redirect('/') 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/text')
def text_output():
    parrot.process_input(session['current_file'])
    session['paragraph'] = parrot.gen_paragraph()  
    return render_template('text.html')

def purge_uploads():
    for item in os.scandir(app.config['UPLOAD_FOLDER']):
        try:
            os.remove(item)
        except FileNotFoundError:
            continue