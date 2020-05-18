import os

from flask import render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from util import is_allowed

from . import app    # For application discovery by the 'flask' command.
from parser import get_result

files = []
results = {}


@app.route('/', methods=['POST', 'GET'])
def home():
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
        if file and is_allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            files.append(filename)
    return render_template('index.html', files=files)


    #return redirect(url_for('bla', filename=filename))


@app.route('/result/<filename>')
def result(filename):
    result = get_result(filename)
    return render_template('result.html', result=result)


# Also, if you want to run the development server on a different IP address or port,
# use the host and port command-line arguments, as with --host=0.0.0.0 --port=80.

"""
How to:
Implement an API endpoint that returns a static file.
      In the static folder, create a JSON data file named data.json
      For this purpose, the Flask object contains a built-in method, send_static_file,
      which generates a response with a static file contained within the app's static folder.

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

"""