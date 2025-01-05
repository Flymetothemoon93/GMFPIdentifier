import os
import subprocess
import pandas as pd

def run_hmmsearch(hmm_file, protein_db, output_dir, error_log):
    """
    Use HMMER to scan the protein database and output results to a file with 24 threads.
    Logs errors to a specific file.
    """
    output_file = os.path.join(output_dir, os.path.basename(hmm_file).replace(".hmm", "_results.tbl"))
    cmd = f"hmmsearch --tblout {output_file} --cpu 24 {hmm_file} {protein_db}"
    try:
        subprocess.run(cmd, shell=True, check=True, stderr=open(error_log, "a"))
        print(f"HMMER search completed: {output_file}")
    except subprocess.CalledProcessError as e:
        with open(error_log, "a") as log_file:
            log_file.write(f"Error running HMMER for {hmm_file}: {e}\n")
    return output_file

def map_to_interpro(hmm_results, protein2ipr, output_file, error_log):
    """
    Extract matched protein IDs from HMMER results and map them to InterPro IDs.
    Logs errors to a specific file.
    """
    try:
        # Parse HMMER results and extract protein IDs
        proteins = []
        with open(hmm_results, 'r') as file:
            for line in file:
                if not line.startswith("#") and line.strip():
                    proteins.append(line.split()[0])  # Extract matched protein ID

        if not proteins:
            with open(error_log, "a") as log_file:
                log_file.write(f"No protein matches found in {hmm_results}\n")
            return None

        # Load InterPro mapping file
        ipr_data = pd.read_csv(protein2ipr, sep="\t", header=None, names=["UniProt_ID", "InterPro_ID"])
        matched_ipr = ipr_data[ipr_data["UniProt_ID"].isin(proteins)]

        if matched_ipr.empty:
            with open(error_log, "a") as log_file:
                log_file.write(f"No InterPro IDs mapped for proteins in {hmm_results}\n")
            return None

        # Save results
        matched_ipr.to_csv(output_file, sep="\t", index=False, mode="a", header=not os.path.exists(output_file))
        print(f"InterPro ID mapping results saved to {output_file}")
        return matched_ipr
    except Exception as e:
        with open(error_log, "a") as log_file:
            log_file.write(f"Error processing HMM results in {hmm_results}: {e}\n")
        return None

def main():
    # Configure paths
    hmm_dir = "database/GyDB"               # Directory containing HMM files
    protein_db = "database/uniprot_sprot.fasta"   # Path to protein database
    output_dir = "results/hmmsearch"        # Directory for HMMER output
    protein2ipr = "database/protein2ipr.dat" # InterPro mapping file
    final_output = "results/interpro_ids.tsv"
    error_log = "results/error.log"         # Log file for errors

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Clear previous error log
    if os.path.exists(error_log):
        os.remove(error_log)

    # Initialize final output
    if os.path.exists(final_output):
        os.remove(final_output)

    # Run HMMER and map to InterPro IDs for each HMM file
    hmm_files = [os.path.join(hmm_dir, f) for f in os.listdir(hmm_dir) if f.endswith(".hmm")]
    print(f"Found {len(hmm_files)} HMM files to process.")

    for hmm_file in hmm_files:
        print(f"Processing HMM file: {os.path.basename(hmm_file)}")
        hmm_results = run_hmmsearch(hmm_file, protein_db, output_dir, error_log)
        if hmm_results:
            map_to_interpro(hmm_results, protein2ipr, final_output, error_log)

if __name__ == "__main__":
    main()
