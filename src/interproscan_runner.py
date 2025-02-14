import subprocess
import os
from Bio import SeqIO

def truncate_fasta_ids(input_fasta, truncated_fasta):
    """
    Truncate sequence IDs in a FASTA file to ensure compatibility with InterProScan.
    """
    id_mapping = {}
    original_ids = set()
    with open(input_fasta, 'r') as input_handle, open(truncated_fasta, 'w') as output_handle:
        for i, record in enumerate(SeqIO.parse(input_handle, "fasta")):
            truncated_id = f"seq{i}"
            original_ids.add(record.id)  # Keep track of original IDs
            id_mapping[truncated_id] = record.id  # Store mapping
            record.id = truncated_id
            record.description = ""
            SeqIO.write(record, output_handle, "fasta")
    return id_mapping, original_ids

def restore_fasta_ids(output_tsv, id_mapping, original_ids, restored_tsv):
    """
    Restore original sequence IDs in the InterProScan results, ensuring only valid sequences are mapped back.
    """
    with open(output_tsv, 'r') as input_handle, open(restored_tsv, 'w') as output_handle:
        for line in input_handle:
            columns = line.strip().split("\t")
            if len(columns) > 0:
                seq_id = columns[0]
                if seq_id in id_mapping:  # Only replace valid truncated IDs
                    original_id = id_mapping[seq_id]
                    if original_id in original_ids:  # Ensure it's an input sequence, not a database match
                        columns[0] = original_id
                output_handle.write("\t".join(columns) + "\n")

def run_interproscan(input_fasta, output_file, threads=1):
    """
    Runs InterProScan on a given FASTA file and saves the results to an output file.
    """
    try:
        print(f"Running InterProScan with ID truncation using {threads} threads...", flush=True)

        # Temporary file paths
        truncated_fasta = input_fasta + ".truncated"
        temp_output = output_file + ".temp"

        # Step 1: Truncate IDs
        id_mapping, original_ids = truncate_fasta_ids(input_fasta, truncated_fasta)

        # Step 2: Retrieve InterProScan path
        interproscan_path = os.environ.get("INTERPROSCAN_PATH")
        if not interproscan_path:
            raise EnvironmentError("Please set the INTERPROSCAN_PATH environment variable.")

        # Step 3: Construct the InterProScan command with user-specified threads
        cmd = [
            os.path.join(interproscan_path, "interproscan.sh"),
            "-i", truncated_fasta,
            "-o", temp_output,
            "-f", "tsv",
            "-goterms",
            "-iprlookup",
            "--cpu", str(threads)
        ]

        # Step 4: Run InterProScan
        subprocess.run(cmd, check=True)
        print("InterProScan completed.", flush=True)

        # Step 5: Restore original IDs
        restore_fasta_ids(temp_output, id_mapping, original_ids, output_file)
        # print(f"Results saved to {output_file}", flush=True)

        # Cleanup
        os.remove(truncated_fasta)
        os.remove(temp_output)

    except subprocess.CalledProcessError as e:
        print(f"InterProScan failed with error: {e}", flush=True)
    except Exception as e:
        print(f"An error occurred: {e}", flush=True)
