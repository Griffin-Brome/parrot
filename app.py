import parrot
import os
from flask import Flask, flash, request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './var/www/uploads'
ALLOWED_EXTENSIONS = {'txt'} # I might try to implement other filetypes in the future

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'PppZt00xEdHalhWKkb_Lpw' # secrets.token_urlsafe(16)

@app.route('/')
def index():
    return render_template('index.html')

# Flask boilerplate
# http://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/#uploading-files

@app.route('/upload-file', methods=['GET', 'POST']) 
def upload_file():
    # Clear out www/uploads of any pre existing files


    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
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
    session['paragraph'] = parrot.gen_paragraph() # lets use a session variable 
    render_template('text.html')