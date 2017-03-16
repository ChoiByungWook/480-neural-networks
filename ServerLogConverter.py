import collections

import datetime

ServerLogTuple = collections.namedtuple('server_log_line', ['number', 'date', 'time', 'duration', 'protocol', 'src_port',
                                                     'destination_port', 'src_ip', 'destination_ip'])


def convert_line_to_server_log_tuple(line):
    ''' Converts line of text from a server log into a named tuple representation.

    :param line: Line of server log text
    :return: Named tuple representation of line
    '''
    split_line = line.rstrip().split(" ")

    number = split_line[0]

    dateMDY = split_line[1]
    date = datetime.datetime.strptime(dateMDY, "%m/%d/%Y").date()

    timeHMS = split_line[2]
    time = datetime.datetime.strptime(timeHMS, "%X").time()

    durationHMS = split_line[3]
    duration = datetime.datetime.strptime(durationHMS, "%X").time()

    protocol = split_line[4]
    src_port = split_line[5]
    destination_port = split_line[6]
    src_ip = split_line[7]
    destination_ip = split_line[8]

    server_log_tuple = ServerLogTuple(number, date, time, duration, protocol, src_port, destination_port, src_ip,
                                      destination_ip)

    return server_log_tuple