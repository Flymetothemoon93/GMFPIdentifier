#!/bin/bash

# 确保至少两个参数（输入文件和输出目录）
if [ $# -lt 2 ]; then
    echo "Error: You must provide an input file and an output directory!"
    echo "Usage: ./run.sh your_input.fasta your_output_dir [--use-singularity]"
    exit 1
fi

# 解析参数
INPUT_ARG="$1"
OUTPUT_ARG="$2"
USE_SINGULARITY=false

if [ "$3" == "--use-singularity" ]; then
    USE_SINGULARITY=true
fi

echo "DEBUG: Raw input file argument: $INPUT_ARG"
echo "DEBUG: Raw output directory argument: $OUTPUT_ARG"

# 解析输入文件的绝对路径
if [[ "$INPUT_ARG" != -* ]]; then
    INPUT_FILE="$(realpath "$INPUT_ARG" 2>/dev/null || echo "$INPUT_ARG")"
else
    echo "Error: First argument should be the input file, but got '$INPUT_ARG'."
    exit 1
fi

# 解析输出目录的绝对路径
if [[ "$OUTPUT_ARG" != -* ]]; then
    OUTPUT_DIR="$(realpath "$OUTPUT_ARG" 2>/dev/null || echo "$OUTPUT_ARG")"
else
    echo "Error: Second argument should be the output directory, but got '$OUTPUT_ARG'."
    exit 1
fi

# 只提取输入文件名（避免路径解析错误）
INPUT_FILENAME=$(basename "$INPUT_FILE")

echo "DEBUG: Resolved input file path: $INPUT_FILE"
echo "DEBUG: Resolved output directory path: $OUTPUT_DIR"

# 确保输入文件存在
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found! Please check the path."
    exit 1
fi

# 确保输出目录存在
mkdir -p "$OUTPUT_DIR"

# 运行 Singularity 或 Docker
if [ "$USE_SINGULARITY" = true ]; then
    echo "Running with Singularity..."
    
    # 定义 Singularity 镜像路径
    SINGULARITY_IMAGE="$OUTPUT_DIR/gmfpid.sif"

    # 如果 Singularity 镜像不存在，则拉取
    if [ ! -f "$SINGULARITY_IMAGE" ]; then
        echo "Downloading gmfpid.sif to $OUTPUT_DIR..."
        singularity pull "$SINGULARITY_IMAGE" docker://flymetothemoon93/gmfpid:v1.0
    fi
    
    # 运行 Singularity
    singularity run --bind "$(dirname "$INPUT_FILE"):/app/input_data" --bind "$OUTPUT_DIR:/app/output_data" "$SINGULARITY_IMAGE" \
        --input "/app/input_data/$INPUT_FILENAME" \
        --output "/app/output_data"

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
