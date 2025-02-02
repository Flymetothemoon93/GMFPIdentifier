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
if [[ "$1" != -* ]]; then
    INPUT_FILE="$(realpath "$1" 2>/dev/null || echo "$1")"
else
    echo "Error: First argument should be the input file, but got '$1'."
    exit 1
fi

if [[ "$2" != -* ]]; then
    OUTPUT_DIR="$(realpath "$2" 2>/dev/null || echo "$2")"
else
    echo "Error: Second argument should be the output directory, but got '$2'."
    exit 1
fi

echo "DEBUG: Resolved input file path: $INPUT_FILE"
echo "DEBUG: Resolved output directory path: $OUTPUT_DIR"

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
    singularity run --bind "$(dirname "$INPUT_FILE"):/testdata" --bind "$OUTPUT_DIR:/testoutput" "$SINGULARITY_IMAGE" \
        /app/run.sh "/testdata/$INPUT_FILENAME" "/testoutput"

else
    echo "Running with Docker..."
    docker run --rm \
        -v "$(dirname "$INPUT_FILE"):/testdata" \
        -v "$OUTPUT_DIR:/testoutput" \
        flymetothemoon93/gmfpid:v1.0 \
        /bin/bash -c "/app/run.sh /testdata/$INPUT_FILENAME /testoutput"
fi

echo "Process completed! Results are saved in '$OUTPUT_DIR'"
