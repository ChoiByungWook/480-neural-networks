import fileinput
import os
import shutil
import sys

import flask
from flask import flash, request, url_for
from werkzeug.utils import redirect, secure_filename

import ServerLogConverter
from DosClassifier import DosClassifier
from ProbingClassifier import ProbingClassifier

__LOG_PATH = "logs/"
__MARKED = "marked_"

ALLOWED_EXTENSIONS = {'txt'}

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = __LOG_PATH

__pc = ProbingClassifier()


def __classifyLogFile(log_file):
    '''

    :param log_file:
    :return:
    '''
    classifiedLine = []

    opened_log_file = fileinput.input(log_file)
    for line in opened_log_file:
        server_log_tuple = ServerLogConverter.convert_line_to_server_log_tuple(line)
        probing_attack = __pc.classify(server_log_tuple)
        dos_attack = DosClassifier.classify(server_log_tuple)
        # classify and add value to classifiedLine d = ddos, r = r2l...
        classifierString = ""

        if probing_attack == 1:
            classifierString += "p"
        else:
            classifierString += "-"

        if dos_attack:
            classifierString += "d"
        else:
            classifierString += "-"

        classifierString += " "
        classifiedLine.append(classifierString)

    # close original file
    opened_log_file.close()

    return classifiedLine


def __markLogFile(classifiedLine, marked_file):
    '''

    :param classifiedLine:
    :param marked_file:
    :return:
    '''
    opened_marked_log_file = fileinput.input(marked_file, inplace=True)

    for line, classifier in zip(opened_marked_log_file, classifiedLine):
        sys.stdout.write(classifier + line)

    opened_marked_log_file.close()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def my_form():
    return flask.render_template("index.html")


@app.route('/', methods=['POST'])
def __main():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            log_file = __LOG_PATH + file.filename
            # copy marked file for classification
            marked_file = __LOG_PATH + __MARKED + file.filename
            shutil.copyfile(log_file, marked_file)

            # classify each line
            classifiedLines = __classifyLogFile(log_file)

            # mark log file with classifies
            __markLogFile(classifiedLines, marked_file)

            return "Successfully classified server log."

    return "Failed to classify log."


if __name__ == '__main__':
    app.run()
