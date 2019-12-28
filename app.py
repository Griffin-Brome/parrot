import parrot
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './var/www/uploads'
ALLOWED_EXTENSIONS = {'txt'} # I might try to implement other filetypes in the future

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/index')
def index():
    return render_template('index.html')

# Flask boilerplate
# http://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/#uploading-files

@app.route('/upload-file', methods=['GET', 'POST']) 
def upload_file(): 
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            return redirect(url_for('text_output', filename=path))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/text')
def text_output(filename):
    #I'm abusing the dynamic typing a bit here, 
    #this could be one line, but that would be cumbersome
    words = parrot.read_file(filename)
    words = parrot.text_to_dict(words)
    parrot.save_to_json(words)

    paragraph = parrot.gen_paragraph()
    return render_template('text.html', paragraph=paragraph)