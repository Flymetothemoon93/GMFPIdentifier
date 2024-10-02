import argparse
import os
from hmmer_runner import run_hmmer
from data_loader import load_sequences
from utils import create_output_dir

def main():
    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(description="Run FPIdentifier Tool to detect transposons misidentified as genes.")
    parser.add_argument('--input', required=True, help="Path to input protein sequences in FASTA format")
    parser.add_argument('--output', required=True, help="Directory to store output results")
    args = parser.parse_args()

    # 检查输入文件是否存在
    if not os.path.isfile(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return

    # 创建或确认输出目录存在
    create_output_dir(args.output)

    # 加载蛋白质序列并捕获潜在的错误
    try:
        protein_sequences = load_sequences(args.input)
        print(f"Successfully loaded {len(protein_sequences)} sequences from {args.input}")
    except Exception as e:
        print(f"Error loading sequences: {e}")
        return

    # 运行 HMMER 进行比对
    try:
        run_hmmer(protein_sequences, args.output)
        print(f"Results saved to: {args.output}")
    except Exception as e:
        print(f"Error running HMMER: {e}")

if __name__ == "__main__":
    main()
