WORKLOAD_DIRECTORIES="$(find -name '*workloads')"
for workload in $WORKLOAD_DIRECTORIES; do
       	cd $workload;
       	python ../pkb_fio_results_log_parser.py;
       	cd ..
done