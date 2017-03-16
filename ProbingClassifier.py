import collections
import csv

ProbingAttackFinalScore = collections.namedtuple('probing_attack_final_score', ["src_ip", "time", "score"])


class ProbingClassifier:
    def __init__(self):
        # Initialize counters at 0 and current_time to 0
        self.current_time = None
        self.src_ip_score = {}
        self.current_probing_attacks = {}
        self.final_time_score = []

    def classify(self, server_log_tuple):
        probing_score = 0
        if self.current_time != server_log_tuple.time:
            self.calculate_final_score()
            self.current_time = server_log_tuple.time
            self.src_ip_score.clear()
            self.current_probing_attacks.clear()

        __src_ip = server_log_tuple.src_ip

        if __src_ip not in self.src_ip_score:
            self.src_ip_score[__src_ip] = 0

        if server_log_tuple.destination_port == '-':
            return probing_score

        destination_port = int(server_log_tuple.destination_port)
        self.src_ip_score[__src_ip] += self.__apply_points(destination_port)

        if self.src_ip_score[__src_ip] >= 21:
            if __src_ip not in self.current_probing_attacks:
                self.current_probing_attacks[__src_ip] = 1
                probing_score = 1

        return probing_score

    def calculate_final_score(self):
        for src_ip in self.current_probing_attacks:
            probing_attack_final_score = ProbingAttackFinalScore(src_ip, self.current_time, self.src_ip_score[src_ip])
            self.final_time_score.append(probing_attack_final_score)

    def convert_to_csv(self, file_name):
        headers = ['src_ip', 'time', 'score']

        csv_file_name = "csv/" + file_name + "_probing_classifer.csv"
        with open(csv_file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(headers)
            for i in self.final_time_score:
                csv_writer.writerow(i)

    def __apply_points(self, destination_port):
        """
        Based on the destination port, this method will apply points to the points dictionary
        as follows:
            Destination port less than 1024: 3 points
            Destination port greater or equal to 1024: 1 point
            Destination ports 11, 12, 13, 2000: 10 points
        """
        if destination_port in (11, 12, 13, 2000):
            return 10
        if destination_port < 1024:
            return 3
        if destination_port >= 1024:
            return 1
