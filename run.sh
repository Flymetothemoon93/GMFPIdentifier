#!/bin/bash

# Ensure at least two arguments (input file and output directory) are provided
if [ $# -lt 2 ]; then
    echo "Error: You must provide an input file and an output directory!"
    echo "Usage: ./run.sh your_input.fasta your_output_dir [--use-singularity]"
    exit 1
fi

# Capture arguments
INPUT_ARG="$1"
OUTPUT_ARG="$2"
USE_SINGULARITY=false

# Optional third argument to use Singularity
if [ "$3" == "--use-singularity" ]; then
    USE_SINGULARITY=true
fi

echo "DEBUG: Raw input file argument: $INPUT_ARG"
echo "DEBUG: Raw output directory argument: $OUTPUT_ARG"

# Convert input path to absolute
if [[ "$INPUT_ARG" != -* ]]; then
    INPUT_FILE="$(realpath "$INPUT_ARG" 2>/dev/null || echo "$INPUT_ARG")"
else
    echo "Error: First argument should be the input file, but got '$INPUT_ARG'."
    exit 1
fi

# Convert output path to absolute
if [[ "$OUTPUT_ARG" != -* ]]; then
    OUTPUT_DIR="$(realpath "$OUTPUT_ARG" 2>/dev/null || echo "$OUTPUT_ARG")"
else
    echo "Error: Second argument should be the output directory, but got '$OUTPUT_ARG'."
    exit 1
fi

# Extract filename from the input path
INPUT_FILENAME=$(basename "$INPUT_FILE")

echo "DEBUG: Resolved input file path: $INPUT_FILE"
echo "DEBUG: Resolved output directory path: $OUTPUT_DIR"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found! Please check the path."
    exit 1
fi

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Decide whether to use Singularity or Docker
if [ "$USE_SINGULARITY" = true ]; then
    echo "Running with Singularity..."
    
    # Define Singularity image path
    SINGULARITY_IMAGE="$OUTPUT_DIR/gmfpid.sif"

    # Pull Singularity image if not exists
    if [ ! -f "$SINGULARITY_IMAGE" ]; then
        echo "Downloading gmfpid.sif to $OUTPUT_DIR..."
        singularity pull "$SINGULARITY_IMAGE" docker://flymetothemoon93/gmfpid:latest
    fi
    
    # Run with Singularity
    singularity run --bind "$(dirname "$INPUT_FILE"):/app/input_data" --bind "$OUTPUT_DIR:/app/output_data" "$SINGULARITY_IMAGE" \
        --input "/app/input_data/$INPUT_FILENAME" \
        --output "/app/output_data"

else
    echo "Running with Docker..."
    docker run --rm \
        -v "$(dirname "$INPUT_FILE"):/app/input_data" \
        -v "$OUTPUT_DIR:/app/output_data" \
        flymetothemoon93/gmfpid:latest \
        --input "/app/input_data/$INPUT_FILENAME" \
        --output "/app/output_data"
fi

echo "Process completed! Results are saved in '$OUTPUT_DIR'"
