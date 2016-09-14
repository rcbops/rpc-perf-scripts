There are four main types of files contained in the rpc-perf-scripts repo:

* Default config files (default_config.json):
	*This is an example of the json file that contains the parameters and variables for the desired fio job you wish to create. This file is passed into the fio job generator program (referenced below).
	* Parameters that config takes in are as follows: 
		* Ram: singular, e.g. 4
		* Blocksizes: can be singular or multiple, e.g. ["4k"]
		* iodepths: can be singular or multiple, e.g. [1, 32] 
		* Rwmixs: singular, e.g. [60]
		* Rwkind: singular, e.g. "write"
		* Rwmix_type: singular, e.g. "rwmixwrite"
		* Filename: singular , e.g. "helloworld"
	* Refer to fio man pages for more information on possible inputs for these parameters.
* Fio job generator (fio_job_file_generator.py):
	* This is a python script that takes in a JSON config file (if no config file passed in, it uses the default config file). Then it generates fio job files based on the passed in config file. It then puts all of these fio files in a folder called generated_fio_jobs. This folder is deleted at the start of every run.
* PKB Fio Flags (pkb_fio_flags.yaml):
	* This is a simple way of specifying the flags that PKB requires to run a fio job on an Openstack infrastructure, e.g. image ID for the desired server, volume size, etc.
* Perfkit Benchamarker runner (pkb_automated_runner.sh):
	* This is the **main** file that is run when wanting to run PKB for fio in an automated way. This file runs all the above files. 
	* Takes in the number of vms, desired output directory for the fio results,  JSON config, and (this is optional) path to pkb.py. It then generates all the config files by calling the Perfkit Benchamarker runner with the PKB fio flags file and the passed in config file. It then runs all the fio jobs that were generated with the number of vms specified. 