VMS=$1
OUT_DIRECTORY=$2
CONFIG_FILE=$3

if [ $# -lt 3 ]
	then
		echo "Too few arguments supplied, should be in format [vms, output directory, config file]"
else
	python fio_job_file_generator.py CONFIG_FILE
	for file in generated_fio_files/*
	    do
	    for vm in $(seq 1 $VMS)
	    	do
            UNIQUE_RUN_ID=`cat /dev/urandom | env LC_CTYPE=C tr -cd 'a-f0-9' | head -c 8`
		    pkb --benchmarks=fio \
            --run_uri=$UNIQUE_RUN_ID
		    --num_vms=$vm \
		    --benchmark_config_file=pkb_fio_flags.yaml \
		    --fio_jobfile=generated_fio_files/"$file".fio
            mkdir $HOME/$OUT_DIRECTORY
		    cp -r $HOME/tmp/perfkitbenchmarker/runs/$UNIQUE_RUN_ID $HOME/$OUT_DIRECTORY
		done
	done
fi