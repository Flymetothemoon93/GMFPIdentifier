#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Error: You must provide an input file and an output directory!"
    echo "Usage: ./run.sh your_input.fasta your_output_dir"
    exit 1
fi

INPUT_FILE=$(realpath "$1")
OUTPUT_DIR=$(realpath "$2")

mkdir -p "$OUTPUT_DIR"

docker run --rm \
    -v "$(dirname "$INPUT_FILE"):/app/input_data" \
    -v "$OUTPUT_DIR:/app/output_data" \
    flymetothemoon93/gmfpid:v1.0 \
    --input "/app/input_data/$(basename "$INPUT_FILE")" \
    --output "/app/output_data"

echo "Process completed! Results saved in $OUTPUT_DIR"
