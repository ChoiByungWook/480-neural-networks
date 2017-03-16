import pprint

class DosClassifier:
    # Dictionary that keeps track of the frequency of the requests at hourly intervals.
    interval_frequency = {}

    '''Pretty prints the interval_frequency dictionary

        To be used internally.
    '''
    def print_interval_frequencies(frequencies):
        pprint.pprint(DosClassifier.interval_frequency)

    ''' Gathers the time of each log and calculates the frequency for each interval.
    It will also classify the current log as a DOS attack or not. The classification
    will be more reliable after analyzing previous data stored in interval_frequency.
    '''
    def classify(my_tuple):
        # This defines the weight of the features relative to the classifier.
        # weights_of_features = {my_tuple[0]: 0, my_tuple[1]: 0, my_tuple[2]: 0,
        #                        my_tuple[3]: 3, my_tuple[4]: 0, my_tuple[5]: 0,
        #                        my_tuple[6]: 0, my_tuple[7]: 0, my_tuple[8]: 0}

        # Check the time of the current log to add it to the corresponding key:value pair in interval_frequency
        if my_tuple.time.hour not in DosClassifier.interval_frequency:
            DosClassifier.interval_frequency[my_tuple.time.hour] = 0
        else:
            DosClassifier.interval_frequency[my_tuple.time.hour] += 1

        # list of the dictionary's values
        value_list = list(DosClassifier.interval_frequency.values())

        ''' Finding the average amount of requests during log analysis.
        This average serves as one of the criteria for determining whether
        the current log is a DOS attack.
        '''
        sum = 0
        for i in range(0, len(value_list)):
            sum += value_list[i]

        average = sum/len(value_list)

        print(average) #Right now this is ~1920

        ''' Criteria for determining a DOS attack:
            -If the duration of session is less than 1 second
            -If the time of request is less than the usual average of the log file
        '''
        if my_tuple.duration.second < 3 and DosClassifier.interval_frequency[my_tuple.time.hour] < average:
            return True
        else:
            return False






