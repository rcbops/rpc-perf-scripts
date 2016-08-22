import jinja2
import time


SCENARIOS = {
    'random_write_100': {
        'name': 'random_write',
        'rwkind': 'randwrite',
        'rwmixwrite': '100'
    },
    'random_write_80': {
        'name': 'random_write',
        'rwkind': 'randwrite',
        'rwmixwrite': '80'
    },
    'random_write_60': {
        'name': 'random_write',
        'rwkind': 'randwrite',
        'rwmixwrite': '60'
    },
    'random_read_100': {
        'name': 'random_read',
        'rwkind': 'randread',
        'rwmixread': '100'
    },
    'random_read_80': {
        'name': 'random_read',
        'rwkind': 'randread',
        'rwmixread': '80'
    },
    'random_read_60': {
        'name': 'random_read',
        'rwkind': 'randread',
        'rwmixread': '60'
    }
}

JOB_FILE_TEMPLATE = """
[global]
ioengine=libaio
direct=1
random_distribution=pareto:0.9
size=250g
time_based
runtime={{runtime}}
filename={{filename}}
{%- for scenario in scenarios %}
{%- for blocksize in blocksizes %}
{%- for iodepth in iodepths %}
[{{scenario['name']}}-blocksize-{{blocksize}}]
rw={{scenario['rwkind']}}
rwmixwrite={{scenario['rwmixwrite']}}
rwmixread={{scenario['rwmixread']}}
blocksize={{blocksize}}
iodepth={{iodepth}}
{%- endfor %}
{%- endfor %}
{%- endfor %}
"""

  job_file_template = Template(JOB_FILE_TEMPLATE)

  job_file_template.render(
      runtime=5m,
      filename=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),
      blocksizes=[4k, 128k, 1M]
      scenarios=SCENARIOS
      iodepths=[1, 32]))

