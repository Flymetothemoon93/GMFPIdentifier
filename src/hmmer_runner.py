import subprocess

def run_hmmer(protein_sequences, output_dir):
    hmm_model = 'database/rexdb/rexdb.hmm'  # 假设 HMM 模型路径
    output_file = f'{output_dir}/hmmer_results.txt'

    # 构建 HMMER 命令
    cmd = f"hmmscan --domtblout {output_file} {hmm_model} {protein_sequences}"
    
    # 执行 HMMER 并捕获潜在错误
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"HMMER run successfully, results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"HMMER failed with error: {e}")
