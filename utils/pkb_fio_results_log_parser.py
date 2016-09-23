import csv
import fnmatch
import subprocess
import os
import pathlib


def find_pkb_logs():

    # finds all the pkb log files in all subsequent directories
    # and returns these logs as a list
    list_of_files = []
    for dirpath, dirs, files in os.walk(os.getcwd()):
        for filename in fnmatch.filter(files, '*.log'):
            list_of_files.append(dirpath + "/" + filename)
    return list_of_files


def consolidated_log(log_file):

    # summarizes individual log file by only extracting relevant section
    # and returns said relevant section
    consolidated_log = subprocess.Popen(
                     ['sed',
                      '/PerfKitBenchmarker Complete Results/,/p99.99/!d;//d',
                      log_file],
                     stdout=subprocess.PIPE).communicate()[0].decode('ascii')
    return consolidated_log


def find_param_value(variable, log_file):

    # parses summarized log file in order to find specific value, e.g. 'io'
    # and returns value of passed in variable/parameter
    brief_log = consolidated_log(log_file)
    brief_log_no_spaces = brief_log.split()
    brief_log_no_commas = ([s.replace(',', '') for s in brief_log_no_spaces])
    brief_log_no_colons = ([s.replace(':', '') for s in brief_log_no_commas])
    brief_log_no_quotes = ([s.replace("'", '') for s in brief_log_no_colons])

    position_of_variable = 1 + brief_log_no_quotes.index(variable)
    variable_value = brief_log_no_quotes[position_of_variable]
    return variable_value


def parse_pkb_log(log_file):

    # parse individual pkb log file for values
    # and returns a dictionary with these values
    report_dict = {}

    report_dict['io'] = find_param_value('iodepth', log_file)
    report_dict['rwmixwrite'] = find_param_value('rwmixwrite', log_file)
    report_dict['mean_bandwidth'] = find_param_value('bw_mean', log_file)
    report_dict['mean_latency'] = find_param_value('mean', log_file)
    report_dict['median_latency'] = find_param_value('p50', log_file)
    report_dict['99th_p_latency'] = find_param_value('p99', log_file)
    return report_dict


def write_to_csv():

    # writes data from log files into csv with appropriate header names
    full_path = pathlib.Path(os.getcwd())
    parent_directory = os.path.join(*full_path.parts[-1:])
    with open(parent_directory+'.csv', 'w') as csvfile:
        fieldnames = ['io', 'rwmixwrite', 'mean_bandwidth', 'mean_latency',
                      'median_latency', '99th_p_latency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        list_of_log_files = find_pkb_logs()
        for log_file in list_of_log_files:
            report_dict = parse_pkb_log(log_file)
            writer.writerow(report_dict)

if __name__ == '__main__':
    write_to_csv()
