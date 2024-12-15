import subprocess
import os
from Bio import SeqIO

def truncate_fasta_ids(input_fasta, truncated_fasta):
    """
    Truncate sequence IDs in a FASTA file to ensure compatibility with InterProScan.

    Parameters:
    - input_fasta (str): Path to the input FASTA file.
    - truncated_fasta (str): Path to save the truncated FASTA file.

    Returns:
    - dict: Mapping of original IDs to truncated IDs.
    """
    id_mapping = {}
    with open(input_fasta, 'r') as input_handle, open(truncated_fasta, 'w') as output_handle:
        for i, record in enumerate(SeqIO.parse(input_handle, "fasta")):
            truncated_id = f"seq{i}"
            id_mapping[truncated_id] = record.id
            record.id = truncated_id
            record.description = ""
            SeqIO.write(record, output_handle, "fasta")
    return id_mapping

def restore_fasta_ids(output_tsv, id_mapping, restored_tsv):
    """
    Restore original sequence IDs in the InterProScan results.

    Parameters:
    - output_tsv (str): Path to the InterProScan results with truncated IDs.
    - id_mapping (dict): Mapping of truncated IDs to original IDs.
    - restored_tsv (str): Path to save the results with restored IDs.
    """
    with open(output_tsv, 'r') as input_handle, open(restored_tsv, 'w') as output_handle:
        for line in input_handle:
            for truncated_id, original_id in id_mapping.items():
                if truncated_id in line:
                    line = line.replace(truncated_id, original_id)
            output_handle.write(line)

def run_interproscan(input_fasta, output_file):
    """
    Runs InterProScan on a given FASTA file and saves the results to an output file.

    Parameters:
    - input_fasta (str): Path to the input FASTA file containing sequences for InterProScan.
    - output_file (str): Path where the InterProScan results should be saved.

    Returns:
    - None
    """
    try:
        print("Running InterProScan with ID truncation...")

        # Temporary file paths
        truncated_fasta = input_fasta + ".truncated"
        temp_output = output_file + ".temp"

        # Step 1: Truncate IDs
        id_mapping = truncate_fasta_ids(input_fasta, truncated_fasta)

        # Step 2: Retrieve InterProScan path
        interproscan_path = os.environ.get("INTERPROSCAN_PATH")
        if not interproscan_path:
            raise EnvironmentError("Please set the INTERPROSCAN_PATH environment variable.")

        # Step 3: Construct the InterProScan command
        cmd = [
            os.path.join(interproscan_path, "interproscan.sh"),
            "-i", truncated_fasta,
            "-o", temp_output,
            "-f", "tsv",
            "-goterms",
            "-iprlookup",
            "--cpu", "4"
        ]

        # Step 4: Run InterProScan
        subprocess.run(cmd, check=True)
        print("InterProScan completed.")

        # Step 5: Restore original IDs
        restore_fasta_ids(temp_output, id_mapping, output_file)
        print(f"Results saved to {output_file}")

        # Cleanup
        os.remove(truncated_fasta)
        os.remove(temp_output)

    except subprocess.CalledProcessError as e:
        print(f"InterProScan failed with error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
