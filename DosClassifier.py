import collections
import datetime
import pprint

SrcIpToDestinationPort = collections.namedtuple("src_ip_to_destination_port_frequency",
                                                ["src_ip", "destination_port", "time"])


class DosClassifier:
    ip_to_port_requests = {}
    final_requests_per_hour = {}
    total_duration = 0.0
    average_duration = 0.0
    request_count = 0.0
    threshold = 5
    current_time = None

    # Used for Metric Data
    values_for_requests_per_hour = []
    average_requests_per_hour = 0

    ''' Pretty prints the interval_frequency dictionary
    To be used internally.
    '''

    def print_interval_frequencies(frequencies):
        pprint.pprint(DosClassifier.ip_to_port_requests)

    ''' Gathers the time of each log and calculates the frequency for each interval.
    It will also classify the current log as a DOS attack or not. The classification
    will be more reliable after analyzing previous data stored in ip_to_port_requests.
    '''

    def classify(server_log_tuple):
        overall_score = 0
        DosClassifier.request_count += 1.0

        current_duration = server_log_tuple.duration
        current_duration_in_seconds = datetime.timedelta(hours=current_duration.hour, minutes=current_duration.minute,
                                                         seconds=current_duration.second).total_seconds()
        DosClassifier.total_duration += current_duration_in_seconds
        DosClassifier.average_duration = DosClassifier.total_duration / DosClassifier.request_count

        time = server_log_tuple.time
        hour = time.hour

        if hour not in DosClassifier.final_requests_per_hour:
            DosClassifier.final_requests_per_hour[hour] = 1
        else:
            DosClassifier.final_requests_per_hour[hour] += 1

        destination_port = server_log_tuple.destination_port
        src_ip = server_log_tuple.src_ip

        current_request = SrcIpToDestinationPort(src_ip, destination_port, time)

        if DosClassifier.current_time != time:
            DosClassifier.current_time = time
            DosClassifier.ip_to_port_requests.clear()

        # If the current request information is not in the dictionary, add it.
        if current_request not in DosClassifier.ip_to_port_requests:
            DosClassifier.ip_to_port_requests[current_request] = 1
        else:
            DosClassifier.ip_to_port_requests[current_request] += 1

        if current_duration_in_seconds < DosClassifier.average_duration:
            overall_score += 2

        '''If the amount of current requests from the same dest_port and src_ip is greater
            than the threshold, then this current log is considered a DOS.
        '''
        if DosClassifier.ip_to_port_requests[current_request] >= DosClassifier.threshold:
            return True
        else:
            return False

    # number of requests per hour over 24 hours - done
    # average of requests per hour
    def calculate_final_score():
        sum_of_requests = 0
        for val in DosClassifier.final_requests_per_hour.values():
            sum_of_requests += val
        DosClassifier.average_requests_per_hour = sum_of_requests / 24 # 1927 for now




