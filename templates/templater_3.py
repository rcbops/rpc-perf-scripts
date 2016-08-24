import jinja2
import time
import datetime


JOB_FILE_TEMPLATE_READ = """
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
rwmixread={{rwmixread}}
blocksize={{blocksize}}
iodepth={{iodepth}}
"""


JOB_FILE_TEMPLATE_WRITE = """
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


def templates(ram=25, blocksizes=['4k'], iodepths=[1], rwmixs=[100],
              rwkind='randread', rwmix_type='rwmixread', filename_input=None):
    if filename_input is None:
        filename_input = 'myfile'
    if rwmix_type == 'rwmixread':
        job_file_template = jinja2.Template(JOB_FILE_TEMPLATE_READ)
    else:
        job_file_template = jinja2.Template(JOB_FILE_TEMPLATE_WRITE)
    size = ''.join((str(10*ram), 'g'))
    for blocksize in blocksizes:
        for iodepth in iodepths:
            for rwmix in rwmixs:
                filename = '%s_%s_%s_%s.txt' % (filename_input,
                                                blocksize, iodepth, rwmix)
                with open(filename, 'wt') as f:
                    if rwmix_type == 'rwmixread':
                        string = str(job_file_template.render(
                          runtime='5m',
                          filename=datetime.datetime
                                  .fromtimestamp(time.time())
                                  .strftime('%Y-%m-%d_%H:%M:%S'),
                          blocksize=blocksize,
                          size=size,
                          rwkind=rwkind,
                          rwmixread=rwmix,
                          iodepth=iodepth))
                    else:
                        string = str(job_file_template.render(
                          runtime='5m',
                          filename=datetime.datetime
                                  .fromtimestamp(time.time())
                                  .strftime('%Y-%m-%d_%H:%M:%S'),
                          blocksize=blocksize,
                          size=size,
                          rwkind=rwkind,
                          rwmixwrite=rwmix,
                          iodepth=iodepth))
                    f.write(string + "\n")

#templates(25, ['4k', '128k', '1M'], [1, 32], [100, 80, 60], 'randwrite', 'rwmixwrite', 'hello')
templates()
