import jinja2
import time
import datetime
import json
import os
import shutil
import sys
from pprint import pprint


JOB_FILE_TEMPLATE = """
[global]
ioengine=libaio
direct=1
random_distribution=pareto:0.9
size={{size}}
time_based
runtime={{runtime}}

[rw-{{rwkind}}-iodepth-{{iodepth}}-blocksize-{{blocksize}}]
rw={{rwkind}}
rwmixwrite={{rwmixwrite}}
blocksize={{blocksize}}
iodepth={{iodepth}}
"""


def parse_config_file(config_file_name):
    with open(config_file_name) as data_file:
        data = json.load(data_file)
        return(data)


def render_fio_job(job_file_template, config_file_params,
                   blocksize, size, rwmix, iodepth):
    fio_job = str(job_file_template.render(
      runtime='5m',
      blocksize=blocksize,
      size=size,
      rwkind=config_file_params['rwkind'],
      rwmixwrite=rwmix,
      iodepth=iodepth))
    return fio_job


def write_fio_job(filename, fio_job, path):
    with open(os.path.join(path, filename), 'wt') as f:
        f.write(fio_job + "\n")


def create_fio_job_files(config_file=None):
    path = 'generated_fio_files'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)
    if config_file is None:
        config_file = 'config_file.json'
    job_file_template = jinja2.Template(JOB_FILE_TEMPLATE)
    config_file_params = parse_config_file(config_file)
    size = ''.join((str(10*config_file_params['ram']), 'g'))
    for blocksize in config_file_params['blocksizes']:
        for iodepth in config_file_params['iodepths']:
            for rwmix in config_file_params['rwmixs']:
                filename = '%s_%s_blocksize_%s_iodepth_%s_rwmix.fio' % (config_file_params['filename'],
                                                blocksize, iodepth, rwmix)
                fio_job = render_fio_job(job_file_template,
                                         config_file_params, blocksize,
                                         size, rwmix, iodepth)
                write_fio_job(filename, fio_job, path)

if __name__ == '__main__':
    create_fio_job_files(sys.argv[1])
