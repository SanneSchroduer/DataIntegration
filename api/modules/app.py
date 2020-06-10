import os

from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename


from flask import Flask
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['UPLOAD_FOLDER'] = '../inbox'
from util import is_allowed, get_db_result, write_output

files = []
results = {}


@app.route('/', methods=['POST', 'GET'])
def home():
    """
    App route that handles a POST request, checks for the existence of the 'file' parameter.
    If a filename is provided, the file extension is checked with the is_allowed function.
    :return: renders template and provides file parameter
    """
    if request.method == 'POST':
        # checking if the post request contains a file
        if 'file' not in request.files:
            flash('The POST request doesn\'t contain a file')
            return redirect(request.url)
        file = request.files['file']
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
    """
    App route that handles
    :param filename: the name of the input file (string)
    :return: renders template for the result page, provides output_data (list) and out_file (name of the output file)
    """
    output_data, filepath = get_db_result(filename)
    out_file = write_output(output_data, filename)
    return render_template('result.html', result=output_data, file=out_file)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')