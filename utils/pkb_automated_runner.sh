#!/bin/bash -e

VMS="$1"
OUT_DIRECTORY="$2"
CONFIG_FILE="$3"

if [ $# -lt 3 ]; then
  echo "Too few arguments supplied, should be in format [vms, output directory, config file]"
  exit -1
fi

if [[ ! -d "$OUT_DIRECTORY" ]]; then
    mkdir -p "$OUT_DIRECTORY"
fi

python fio_job_file_generator.py "$CONFIG_FILE"
for file in generated_fio_files/*; do
  for vm in $(seq 1 "$VMS"); do
    UNIQUE_RUN_ID="$(cat /dev/urandom | env LC_CTYPE=C tr -cd 'a-f0-9' | head -c 8)"
    python pkb.py --benchmarks=fio --run_uri="$UNIQUE_RUN_ID" \
      --num_vms="$vm" --benchmark_config_file=pkb_fio_flags.yaml \
      --fio_jobfile="$file"
    cp -r /tmp/perfkitbenchmarker/runs/"$UNIQUE_RUN_ID" "$OUT_DIRECTORY"
  done
done