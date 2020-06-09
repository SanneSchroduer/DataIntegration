import os

from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename


from flask import Flask
app = Flask(__name__, template_folder='../templates')
app.config['UPLOAD_FOLDER'] = '../inbox'
from util import is_allowed, get_db_result, write_output

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


@app.route('/result/<filename>')
def result(filename):
    output_data, filepath = get_db_result(filename)
    out_file = write_output(output_data, filename)
    return render_template('result.html', result=output_data, file=out_file)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')