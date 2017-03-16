import fileinput
import sys

import ServerLogConverter

LOG_PATH = "logs/"


def main():
    file = str(sys.argv[1])
    log_file = LOG_PATH + file

    for line in fileinput.input(log_file):
        server_log_tuple = ServerLogConverter.convert_line_to_server_log_tuple(line)
        print(server_log_tuple)
        break

    fileinput.close()


if __name__ == '__main__':
    main()
