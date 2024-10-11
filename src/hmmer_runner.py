import subprocess
import os
import re

def extract_contig_name(fasta_file):
    """
    Extracts the contig or chromosome name from the input FASTA file by parsing the 'chr=' field in the header.
    
    Parameters:
    - fasta_file (str): Path to the input FASTA file.
    
    Returns:
    - str: Contig or chromosome name extracted from the first sequence header.
    """
    with open(fasta_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                # Use regex to find the 'chr=' field and extract its value
                match = re.search(r'chr=(\S+)', line)
                if match:
                    contig_name = match.group(1)
                    return contig_name
    return None

def run_hmmer(protein_sequences, output_file):
    """
    Runs the HMMER tool to scan the provided protein sequences using HMM models from GyDB.
    
    Parameters:
    - protein_sequences (str): Path to the input protein sequences in FASTA format.
    - output_file (str): Path where the hmmer_results.txt should be saved.
    
    Returns:
    - None: Outputs the results to a file in the specified output path.
    """
    # Extract contig or chromosome name from the protein sequences file
    contig_name = extract_contig_name(protein_sequences)
    if contig_name is None:
        raise ValueError(f"Unable to extract contig name from {protein_sequences}")
    
    # Define the HMM model directory
    hmm_model_dir = 'database/GyDB'

    # Ensure the output directory exists (from the file path)
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the output file for writing results
    with open(output_file, 'w') as f_out:
        # Iterate through all .hmm files to run hmmscan
        for hmm_file in os.listdir(hmm_model_dir):
            if hmm_file.endswith('.hmm'):
                hmm_file_path = os.path.join(hmm_model_dir, hmm_file)
                print(f"Processing HMM file: {hmm_file_path}")
                
                # Construct the HMMER command for each HMM file
                cmd = f"hmmscan --domtblout /dev/stdout {hmm_file_path} {protein_sequences}"
                try:
                    # Run HMMER and capture the results
                    result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                    for line in result.stdout.splitlines():
                        # Filter the actual data lines, skipping comments
                        if not line.startswith('#'):
                            fields = line.strip().split()
                            if len(fields) >= 7:  # Ensure there are enough fields in the result
                                # Replace the first column (target name) with the extracted contig name
                                fields[0] = contig_name
                                # Write the modified result to the output file
                                f_out.write("\t".join(fields) + "\n")
                    print(f"Completed HMM file: {hmm_file_path}")
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(f"HMMER failed with error: {e}")
    
    print(f"HMMER process for {protein_sequences} finished. Results saved to {output_file}")

def clean_and_format_hmmer_results(input_file, output_file):
    """
    Cleans and formats the HMMER results file for better readability.

    Parameters:
    - input_file (str): Path to the raw HMMER results file.
    - output_file (str): Path to the formatted results file.
    
    Returns:
    - None
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Skip unnecessary lines
            if line.startswith('#') or "statistics summary" in line:
                continue
            
            # Split columns based on whitespace and format them
            fields = line.strip().split()
            
            # Ensure the number of fields is consistent and valid
            if len(fields) >= 7:  # Adjust based on your needs
                formatted_line = "\t".join(fields)
                outfile.write(formatted_line + "\n")

    print(f"Formatted results saved to {output_file}")
