import csv
import json
import fnmatch
import subprocess
import os
import pathlib


def find_pkb_json_logs():
    """Find all pkb json log files.

    Finds all the pkb log files in all subsequent directories
    and returns these logs as a list.

    """
    list_of_files = []
    for dirpath, dirs, files in os.walk(os.getcwd()):
        for filename in fnmatch.filter(files, '*.json'):
            list_of_files.append(dirpath + "/" + filename)
    return list_of_files


def json_file_consolidator(log_file):
    """Retrives first two lines of json file.

    Grabs first two lines of the json file,
    as these are the only lines that contain the data
    we care about. This function returns an array of the
    two json lines we care about.

    """
    data = []
    with open(log_file) as filename:
        lines_after_2 = filename.readlines()[:2]
        for line in lines_after_2:
            data.append(json.loads(line))
        return data


def parse_labels(labels):
    """Removes commas and seporators from labels value.

    Takes in string (the value to "labels" key)and removes
    commas and separators. Returns dictionary of parsed input string.
    
    This function was taken from https://goo.gl/rpSmtW.

    """
    result = {}
    for item in labels.strip('|').split('|,|'):
        key, value = item.split(':', 1)
        result[key] = value
    return result


def get_labels(consolidated_log_file):
    """Gets value associated with label key.

    Calls parse_labels function on each element of the
    array passed in and returns an array of the dictionary value
    pertaining to the key "labels" for each dictionary in
    the passed in array.

    """
    labels = []
    for dict_item in consolidated_log_file:
        parsed_labels_info = parse_labels(dict_item['labels'])
        labels.append(parsed_labels_info)
    return labels


def find_key(parsed_labels, key):
    """Find the value associated with the desired key.

    Goes through the passed in parsed_labels dictionaries,
    and for each dictionary in parsed_labels checks to see if
    the desired key is there, if it is, it grabs the value
    of the key and returns it.

    """
    for label_value in parsed_labels:
        try:
            value = label_value[key]
            return value
        except:
            pass


def report_dict_assign_values(log_file):
    """Assigns values to report dictionary keys.

    Parse individual pkb log file for values
    and returns a dictionary with these values.

    """
    report_dict = {}
    consolidated_log_file = json_file_consolidator(log_file)
    parsed_labels = get_labels(consolidated_log_file)

    report_dict['io'] = find_key(parsed_labels, 'iodepth')
    report_dict['rwmixwrite'] = find_key(parsed_labels, 'rwmixwrite')
    report_dict['mean_bandwidth'] = find_key(parsed_labels, 'bw_mean')
    report_dict['mean_latency'] = find_key(parsed_labels, 'mean')
    report_dict['median_latency'] = find_key(parsed_labels, 'p50')
    report_dict['99th_p_latency'] = find_key(parsed_labels, 'p99')
    return report_dict


def write_to_csv():

    """writes data from log files into csv with appropriate header names."""
    full_path = pathlib.Path(os.getcwd())
    parent_directory = os.path.join(*full_path.parts[-1:])
    with open(parent_directory+'.csv', 'w') as csvfile:
        fieldnames = ['io', 'rwmixwrite', 'mean_bandwidth', 'mean_latency',
                      'median_latency', '99th_p_latency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        list_of_log_files = find_pkb_json_logs()
        for log_file in list_of_log_files:
            report_dict = report_dict_assign_values(log_file)
            writer.writerow(report_dict)


if __name__ == '__main__':
    # This will only be executed when this module is run directly.
    write_to_csv()
