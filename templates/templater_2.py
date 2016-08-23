import jinja2
import time
import datetime


JOB_FILE_TEMPLATE = """
[global]
ioengine=libaio
direct=1
random_distribution=pareto:0.9
size={{size}}
time_based
runtime={{runtime}}
filename={{filename}}
[blocksize-{{blocksize}}]
rwkind={{rwkind}}
rwmixwrite={{rwmixwrite}}
blocksize={{blocksize}}
iodepth={{iodepth}}
"""

##BES TODO PUT IN INPUTS for bs iodepth and rw inputs, and error message or default [i.e. defaults to being filled in using map] if no input
##Bes sanitize input for RAM and others

def randwrite_temps(blocksizes, iodepths, rwmixwrites):
	job_file_template = jinja2.Template(JOB_FILE_TEMPLATE)
	try:
		ram_size=int(input("Enter the amount of RAM you are using : "))
		size=''.join((str(10*ram_size), 'g'))
	except ValueError:
		size="250g"
	for blocksize in blocksizes:
		for iodepth in iodepths:
			for rwmixwrite in rwmixwrites:
				filename = 'myfile%s%s%s.txt' % (blocksize, iodepth, rwmixwrite)
				file = open(filename, 'w+')
				string = str(job_file_template.render(
				  runtime="5m",
				  filename=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S'),
				  blocksize=blocksize,
				  size=size,
				  rwkind="randwrite",
				  rwmixwrite=rwmixwrite,
				  iodepth=iodepth))
				file.write(string+ "\n")
		
		#print(string)

randwrite_temps(["4k", "128k", "1M"], [1, 32], [100, 80, 60])
