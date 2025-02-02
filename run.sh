#!/bin/bash

# Check if input and output parameters are provided
if [ $# -lt 2 ]; then
    echo "Error: You must provide an input file and an output directory!"
    echo "Usage: ./run.sh your_input.fasta your_output_dir"
    exit 1
fi

# Read user input
echo "DEBUG: Raw input file argument: $1"
echo "DEBUG: Raw output directory argument: $2"

# Convert to absolute path safely
INPUT_FILE="$(realpath "$1" 2>/dev/null || echo "$1")"
OUTPUT_DIR="$(realpath "$2" 2>/dev/null || echo "$2")"

echo "DEBUG: Resolved input file path: $INPUT_FILE"
echo "DEBUG: Resolved output directory path: $OUTPUT_DIR"

USE_SINGULARITY=false

# Validate that the input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found! Please check the path."
    exit 1
fi

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Debugging: Check if input directory exists
echo "DEBUG: Checking if input directory exists: $(dirname "$INPUT_FILE")"
ls -l "$(dirname "$INPUT_FILE")"

# Run with Docker
echo "Running with Docker..."
docker run --rm -it \
    -v "$(dirname "$INPUT_FILE"):/app/input_data" \
    -v "$OUTPUT_DIR:/app/output_data" \
    flymetothemoon93/gmfpid:v1.0 \
    bash -c "ls -l /app/input_data && ls -l /app/output_data && python3 /app/src/main.py --input /app/input_data/$(basename "$INPUT_FILE") --output /app/output_data"

echo "Process completed! Results are saved in '$OUTPUT_DIR'"
