import fileinput
import shutil
import sys

import ServerLogConverter

LOG_PATH = "logs/"
MARKED = "marked_"


def main():
    file = str(sys.argv[1])
    log_file = LOG_PATH + file

    # create marked file
    marked_file = LOG_PATH + MARKED + file
    shutil.copyfile(log_file, marked_file)

    for line in fileinput.input(log_file):
        server_log_tuple = ServerLogConverter.convert_line_to_server_log_tuple(line)

    fileinput.close()


if __name__ == '__main__':
    main()
