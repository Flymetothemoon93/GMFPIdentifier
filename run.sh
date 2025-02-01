#!/bin/bash

# Check if input and output parameters are provided
if [ $# -lt 2 ]; then
    echo "Error: You must provide an input file and an output directory!"
    echo "Usage: ./run.sh your_input.fasta your_output_dir"
    exit 1
fi

# Read user input
INPUT_FILE="$(realpath "$1")"  # Convert to absolute path
OUTPUT_DIR="$(realpath "$2")"
USE_SINGULARITY=false

# Extract filename from the input path
INPUT_FILENAME=$(basename "$INPUT_FILE")

# Check if an optional third parameter (--use-singularity) is provided
if [ "$3" == "--use-singularity" ]; then
    USE_SINGULARITY=true
fi

# Validate that the input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found! Please check the path."
    exit 1
fi

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Run with Docker or Singularity
if [ "$USE_SINGULARITY" = true ]; then
    echo "Running with Singularity..."
    
    # Set Singularity image path inside the output directory
    SINGULARITY_IMAGE="$OUTPUT_DIR/gmfpid.sif"

    # Pull the Singularity image if not exists
    if [ ! -f "$SINGULARITY_IMAGE" ]; then
        echo "Downloading gmfpid.sif to $OUTPUT_DIR..."
        singularity pull "$SINGULARITY_IMAGE" docker://flymetothemoon93/gmfpid:v1.0
    fi
    
    # Run Singularity with proper bindings
    singularity run --bind "$OUTPUT_DIR:/app/output_data" "$SINGULARITY_IMAGE" \
        --input "$INPUT_FILE" \
        --output /app/output_data

else
    echo "Running with Docker..."
    docker run --rm \
        -v "$(dirname "$INPUT_FILE"):/app/input_data" \
        -v "$OUTPUT_DIR:/app/output_data" \
        flymetothemoon93/gmfpid:v1.0 \
        --input "/app/input_data/$INPUT_FILENAME" \
        --output "/app/output_data"
fi

echo "Process completed! Results are saved in '$OUTPUT_DIR'"
