import fileinput
import shutil
import sys

import flask

import ServerLogConverter

LOG_PATH = "logs/"
MARKED = "marked_"

app = flask.Flask(__name__)


def markLogFile(classifiedLine, marked_file):
    opened_marked_log_file = fileinput.input(marked_file, inplace=True)

    for line, classifier in zip(opened_marked_log_file, classifiedLine):
        sys.stdout.write(classifier + line)

    opened_marked_log_file.close()


def classifyLogFile(log_file):
    classifiedLine = []

    opened_log_file = fileinput.input(log_file)
    for line in opened_log_file:
        server_log_tuple = ServerLogConverter.convert_line_to_server_log_tuple(line)

        # classify and add value to classifiedLine d = ddos, r = r2l...
        classifiedLine.append("d ")

    # close original file
    opened_log_file.close()

    return classifiedLine


@app.route('/')
def main():
    file = str("serverlogs.txt")
    log_file = LOG_PATH + file

    # copy marked file for classification
    marked_file = LOG_PATH + MARKED + file
    shutil.copyfile(log_file, marked_file)

    # classify each line
    classifiedLines = classifyLogFile(log_file)

    # mark log file with classifies
    markLogFile(classifiedLines, marked_file)

    return "Hello"


if __name__ == '__main__':
    app.run()
