import os

from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from parser import is_allowed

from flask import Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'inbox'
from parser import get_result, filter_malignant

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
    input_data, filepath = get_result(filename)
    output_data, out_file = filter_malignant(input_data, filename)
    return render_template('result.html', result=output_data, file=out_file)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')