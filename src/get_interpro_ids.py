import os
import subprocess
import pandas as pd

def run_hmmsearch(hmm_file, protein_db, output_dir):
    """
    使用 HMMER 扫描蛋白数据库，输出结果文件。
    """
    output_file = os.path.join(output_dir, os.path.basename(hmm_file).replace(".hmm", "_results.tbl"))
    cmd = f"hmmsearch --tblout {output_file} {hmm_file} {protein_db}"
    subprocess.run(cmd, shell=True, check=True)
    return output_file

def map_to_interpro(hmm_results, protein2ipr, output_file):
    """
    从 HMMER 结果中提取匹配的蛋白 ID，并映射到 InterPro ID。
    """
    # 解析 HMMER 结果，提取蛋白 ID
    proteins = []
    with open(hmm_results, 'r') as file:
        for line in file:
            if not line.startswith("#") and line.strip():
                proteins.append(line.split()[0].split("|")[1])  # 提取 UniProt ID

    # 加载 InterPro 映射文件
    ipr_data = pd.read_csv(protein2ipr, sep="\t", header=None, names=["UniProt_ID", "InterPro_ID"])
    matched_ipr = ipr_data[ipr_data["UniProt_ID"].isin(proteins)]

    # 保存结果
    matched_ipr.to_csv(output_file, sep="\t", index=False)
    print(f"InterPro ID 映射结果已保存到 {output_file}")

def main():
    # 配置路径
    hmm_dir = "database/GyDB"               # HMM 文件目录
    protein_db = "database/uniprot.fasta"   # 蛋白数据库路径
    output_dir = "results/hmmsearch"        # HMMER 输出目录
    protein2ipr = "database/protein2ipr.dat" # InterPro 映射文件
    final_output = "results/interpro_ids.tsv"

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 批量运行 HMMER 和映射
    for hmm_file in os.listdir(hmm_dir):
        if hmm_file.endswith(".hmm"):
            hmm_path = os.path.join(hmm_dir, hmm_file)
            hmm_results = run_hmmsearch(hmm_path, protein_db, output_dir)
            map_to_interpro(hmm_results, protein2ipr, final_output)

if __name__ == "__main__":
    main()
