from Bio import SeqIO

def load_sequences(file_path):
    try:
        # 加载并解析FASTA格式的蛋白质序列
        sequences = list(SeqIO.parse(file_path, "fasta"))
        if not sequences:
            raise ValueError(f"No sequences found in the provided file: {file_path}")
        return sequences
    except Exception as e:
        print(f"Error loading sequences from {file_path}: {e}")
        raise
