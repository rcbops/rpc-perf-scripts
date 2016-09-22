# RPC PKB Fio Job Automation

## Purpose

In order to ease running the Perfkit Benchmarker Fio Benchmark on Openstack, we decided to automate the process and use simple config files to pass in desired parameters for the runs. Below we explain what parameters the config file takes in, as well as how to run the automation.

## Quick Start

In order to quickly run the automation sutie (with the default fio config parameters) all you need to do is issue the following command:

```sh
pkb_automated_runner.sh <desired_num_vms> <desired_output_directory> [json_config_file]
```

* desired_num_vms is an integer representing the number of VMs to concurrently execute the workload on.
* desired_output_directory is a string representing the relative path where the fio job will output the results and logs.
* json_config_file is a string representing the filename of the json file used to describe the desired fio jobs you wish to create.


This will run the fio benchmark with the default fio parameters, located in the default_config.json file.

## Breakdown of files

There are four main types of files contained in the rpc-perf-scripts repo:

* Default config files (default_config.json):
    * Example of json config file:

```json
{
    "ram": 4,
    "blocksizes": ["4k"],
    "iodepths": [1, 32],
    "rwmixs": [100],
    "rwkind": "write",
    "rwmix_type": "rwmixwrite",
    "filename": "default"
}

```
	*This is an example of the json file that contains the parameters and variables for the desired fio job you wish to create. This file is passed into the fio job generator program (referenced below).
	* Parameters that config takes in are as follows: 

		|             | Example      | Type            | Required |
		|-------------|--------------|-----------------|----------|
		| RAM         | 4            | Int             | X        |
		| Blocksizes  | ["4k"]       | List of Strings | X        |
		| IO depths   | [1, 32]      | List of Ints    | X        |
		| RW mixs     | [100]        | List of Ints    | X        |
		| RW kind     | "write"      | String          | X        |
		| RW mix type | "rwmixwrite" | String          | X        |
		| Filename    | "default"    | String          | X        |
		
	* Refer to fio man pages for more information on possible inputs for these parameters.
* Fio job generator (fio_job_file_generator.py):
	* This is a python script that takes in a JSON config file (if no config file passed in, it uses the default config file). Then it generates fio job files based on the passed in config file. It then puts all of these fio files in a folder called generated_fio_jobs. This folder is deleted at the start of every run.
* PKB Fio Flags (pkb_fio_flags.yaml):
	* This is a simple way of specifying the flags that PKB requires to run a fio job on an Openstack infrastructure, e.g. image ID for the desired server, volume size, etc.
* Perfkit Benchamarker runner (pkb_automated_runner.sh):
	* This is the **main** file that is run when wanting to run PKB for fio in an automated way. This file runs all the above files. 
	* Takes in the number of vms, desired output directory for the fio results, JSON config, and (this is optional) path to pkb.py. It then generates all the config files by calling the Perfkit Benchamarker runner with the PKB fio flags file and the passed in config file. It then runs all the fio jobs that were generated with the number of vms specified. 
