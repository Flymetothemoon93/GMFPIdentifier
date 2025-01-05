import os
import subprocess
import pandas as pd

def run_hmmsearch(hmm_file, protein_db, output_dir):
    """
    Use HMMER to scan the protein database and output results to a temporary file with 24 threads.
    """
    temp_file = os.path.join(output_dir, os.path.basename(hmm_file).replace(".hmm", "_results.tbl"))
    cmd = f"hmmsearch --tblout {temp_file} --cpu 24 {hmm_file} {protein_db}"
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"HMMER search completed: {temp_file}")
        return temp_file
    except subprocess.CalledProcessError as e:
        print(f"Error running hmmsearch for {hmm_file}: {e}")
        return None

def map_to_interpro(hmm_results, protein2ipr, output_file):
    """
    Extract matched protein IDs from HMMER results and map them to InterPro IDs.
    """
    if not hmm_results:
        print("No HMM results to process.")
        return

    # Parse HMMER results and extract protein IDs
    proteins = []
    with open(hmm_results, 'r') as file:
        for line in file:
            if not line.startswith("#") and line.strip():
                proteins.append(line.split()[0])  # Extract matched protein ID

    # Load InterPro mapping file
    ipr_data = pd.read_csv(protein2ipr, sep="\t", header=None, names=["UniProt_ID", "InterPro_ID"])
    matched_ipr = ipr_data[ipr_data["UniProt_ID"].isin(proteins)]

    # Append results to the final output file
    with open(output_file, 'a') as out:
        matched_ipr.to_csv(out, sep="\t", index=False, header=False)
    print(f"InterPro ID mapping results appended to {output_file}")

def main():
    # Configure paths
    hmm_dir = "database/GyDB"               # Directory containing HMM files
    protein_db = "database/uniprot_sprot.fasta"   # Path to protein database
    output_dir = "results/hmmsearch"        # Directory for HMMER output
    protein2ipr = "database/protein2ipr.dat" # InterPro mapping file
    final_output = "results/interpro_ids.tsv"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Initialize final output file
    if os.path.exists(final_output):
        os.remove(final_output)

    # Run HMMER and map to InterPro IDs for each HMM file
    hmm_files = [os.path.join(hmm_dir, f) for f in os.listdir(hmm_dir) if f.endswith(".hmm")]
    print(f"Found {len(hmm_files)} HMM files to process.")

    for hmm_file in hmm_files:
        print(f"Processing HMM file: {os.path.basename(hmm_file)}")
        temp_result = run_hmmsearch(hmm_file, protein_db, output_dir)
        if temp_result:
            map_to_interpro(temp_result, protein2ipr, final_output)
            # Remove the temporary file after processing
            os.remove(temp_result)
            print(f"Temporary file deleted: {temp_result}")

if __name__ == "__main__":
    main()
