import os

from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from parser import is_allowed

from . import app
from parser import get_result

files = []
results = {}


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        # check if the post request contains a file
        if 'file' not in request.files:
            flash('The POST request doesn\'t contain a file')
            return redirect(request.url)
        file = request.files['file']
        # if the user submits without selecting a file, the browser also submits an empty part without filename
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