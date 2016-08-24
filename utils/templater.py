import jinja2
import time
import datetime
import json
from pprint import pprint


JOB_FILE_TEMPLATE = """
[global]
ioengine=libaio
direct=1
random_distribution=pareto:0.9
size={{size}}
time_based
runtime={{runtime}}
filename={{filename}}

[rw-{{rwkind}}-iodepth-{{iodepth}}-blocksize-{{blocksize}}]
rw={{rwkind}}
rwmixwrite={{rwmixwrite}}
blocksize={{blocksize}}
iodepth={{iodepth}}
"""

def config_file_parser(config_file_name):
    with open(config_file_name) as data_file:
        data = json.load(data_file)
        return(data)


def render_function(filename, job_file_template, config_file_params,
                    blocksize, size, rwmix, iodepth):
    with open(filename, 'wt') as f:
                    string = str(job_file_template.render(
                      runtime='5m',
                      filename=datetime.datetime
                              .fromtimestamp(time.time())
                              .strftime('%Y-%m-%d_%H:%M:%S'),
                      blocksize=blocksize,
                      size=size,
                      rwkind=config_file_params['rwkind'],
                      rwmixwrite=rwmix,
                      iodepth=iodepth))
                    f.write(string + "\n")


def template_creator(config_file=None):
    if config_file is None:
        config_file = 'default_config_file.json'
    job_file_template = jinja2.Template(JOB_FILE_TEMPLATE)
    config_file_params = config_file_parser(config_file)
    size = ''.join((str(10*config_file_params['ram']), 'g'))
    for blocksize in config_file_params['blocksizes']:
        for iodepth in config_file_params['iodepths']:
            for rwmix in config_file_params['rwmixs']:
                filename = '%s_%s_%s_%s.fio' % (config_file_params['filename'],
                                                blocksize, iodepth, rwmix)
                render_function(filename, job_file_template,
                                config_file_params, blocksize,
                                size, rwmix, iodepth)
