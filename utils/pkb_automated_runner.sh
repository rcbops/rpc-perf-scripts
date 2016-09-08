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
	    for vm in $(seq 1 $vms)
	    	do
		    pkb --benchmarks=fio \
		    --num_vms=$vm \
		    --benchmark_config_file=fio.yaml \
		    --fio_jobfile=generated_fio_files/"$file".fio
		    if [ -d "$DIRECTORY" ]; then
		    	mv tbd_path $OUT_DIRECTORY/
		    else
		    	mkdir $OUT_DIRECTORY
		    	mv tbd_path $OUT_DIRECTORY/
		    fi
		done
	done
fi