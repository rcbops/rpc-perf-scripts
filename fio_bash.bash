for i in 1 2
    do
    for j in 1 2
        do
        ./pkb.py --benchmarks=fio \
        --num_vms=${i} \
        --benchmark_config_file=fio.yaml \
        --fio_jobfile=/home/fiofile${j}.fio
    done
done