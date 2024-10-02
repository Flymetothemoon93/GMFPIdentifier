import subprocess
import os

def run_hmmer(protein_sequences, output_dir):
    # 指定 GyDB HMM 模型目录
    hmm_model_dir = 'database/GyDB'
    output_file = f'{output_dir}/hmmer_results.txt'

    # 构建 HMMER 命令，扫描目录中的所有 HMM 文件
    cmd = f"hmmscan --domtblout {output_file} {hmm_model_dir}/*.hmm {protein_sequences}"

    # 执行 HMMER 并捕获潜在的错误
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"HMMER run successfully, results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"HMMER failed with error: {e}")
