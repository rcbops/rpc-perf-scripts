#!/bin/bash -e

VMS="$1"
OUT_DIRECTORY="$2"
CONFIG_FILE="$3"
DEFAULT_PKB_PATH="/opt/PerfKitBenchmarker/"

PKB_PATH="${PKB_PATH:-$DEFAULT_PKB_PATH}"

function run_pkb_provision() {
    local file="$1"
    local unique_run_id="$2"
    python "$PKB_PATH"/pkb.py --benchmarks=fio --run_uri="$unique_run_id" \
      --num_vms=1 --benchmark_config_file=pkb_fio_flags.yaml \
      --fio_jobfile="$file" --run_stage=provision,prepare
}

function run_pkb_benchmark() {
    local file="$1"
    local unique_run_id="$2"
    python "$PKB_PATH"/pkb.py --benchmarks=fio --run_uri="$unique_run_id" \
      --num_vms=1 --benchmark_config_file=pkb_fio_flags.yaml \
      --fio_jobfile="$file" --run_stage=run,cleanup,teardown
    cp -r /tmp/perfkitbenchmarker/runs/"$unique_run_id" "$OUT_DIRECTORY"
}


if [ $# -lt 3 ]; then
  echo "Too few arguments supplied, should be in format [vms, output directory, config file]"
  exit -1
fi

if [[ ! -d "$OUT_DIRECTORY" ]]; then
    mkdir -p "$OUT_DIRECTORY"
fi


python fio_job_file_generator.py "$CONFIG_FILE"
for file in generated_fio_files/*; do
  run_ids=
  for vm in $(seq 1 "$VMS"); do
      run_ids[$vm]="$(cat /dev/urandom | env LC_CTYPE=C tr -cd 'a-f0-9' | head -c 8)"
      run_pkb_provision "$file" "${run_ids[$vm]}" &
      sleep $[ ( $RANDOM % 5 ) + 1 ]s  # Sleep between 1 to 5 seconds
  done
  wait
  for vm in $(seq 1 "$VMS"); do
      run_pkb_benchmark "$file" "${run_ids[$vm]}" &
      sleep $[ ( $RANDOM % 5 ) + 1 ]s  # Sleep between 1 to 5 seconds
  done
  wait
done
