import fileinput
import shutil
import sys

import flask

import ServerLogConverter

__LOG_PATH = "logs/"
__MARKED = "marked_"

app = flask.Flask(__name__)


def __classifyLogFile(log_file):
    '''

    :param log_file:
    :return:
    '''
    classifiedLine = []

    opened_log_file = fileinput.input(log_file)
    for line in opened_log_file:
        server_log_tuple = ServerLogConverter.convert_line_to_server_log_tuple(line)

        # classify and add value to classifiedLine d = ddos, r = r2l...
        classifiedLine.append("d ")

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


@app.route('/')
def __main():
    file = str("serverlogs.txt")
    log_file = __LOG_PATH + file

    # copy marked file for classification
    marked_file = __LOG_PATH + __MARKED + file
    shutil.copyfile(log_file, marked_file)

    # classify each line
    classifiedLines = __classifyLogFile(log_file)

    # mark log file with classifies
    __markLogFile(classifiedLines, marked_file)

    return "Hello"


if __name__ == '__main__':
    app.run()
