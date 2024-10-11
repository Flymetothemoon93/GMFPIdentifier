import subprocess
import os
import re

def extract_contig_mapping(fasta_file):
    """
    Extracts a mapping between query names (protein IDs) and contig/chromosome names
    from the input FASTA file by parsing 'chr=' field in the header.
    
    Parameters:
    - fasta_file (str): Path to the input FASTA file.
    
    Returns:
    - dict: A dictionary mapping query names to contig/chromosome names.
    """
    contig_mapping = {}
    with open(fasta_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                # Extract the query name (protein ID)
                query_name = line.split()[0][1:]  # Remove '>' and take the first part as query name
                # Use regex to find the 'chr=' field and extract its value
                match = re.search(r'chr=(\S+)', line)
                if match:
                    contig_name = match.group(1)
                    contig_mapping[query_name] = contig_name
    return contig_mapping

def run_hmmer(protein_sequences, output_file):
    """
    Runs the HMMER tool to scan the provided protein sequences using HMM models from GyDB,
    and replaces target names with corresponding contig names based on the input FASTA file.
    
    Parameters:
    - protein_sequences (str): Path to the input protein sequences in FASTA format.
    - output_file (str): Path where the hmmer_results.txt should be saved.
    
    Returns:
    - None: Outputs the results to a file in the specified output path.
    """
    # Extract contig mapping from the protein sequences file
    contig_mapping = extract_contig_mapping(protein_sequences)
    if not contig_mapping:
        raise ValueError(f"Unable to extract contig mappings from {protein_sequences}")
    
    # Define the HMM model directory
    hmm_model_dir = 'database/GyDB'

    # Ensure the output directory exists (from the file path)
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the output file for writing results
    with open(output_file, 'w') as f_out:
        # Iterate through all .hmm files again to run hmmscan
        for hmm_file in os.listdir(hmm_model_dir):
            if hmm_file.endswith('.hmm'):
                hmm_file_path = os.path.join(hmm_model_dir, hmm_file)
                
                # Print both processing and completed status
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
                            if len(fields) > 3:
                                query_name = fields[3]  # The query name in the 4th column (index 3)
                                
                                # Check if the query name is in our contig mapping
                                if query_name in contig_mapping:
                                    # Replace the first column (target name) with the corresponding contig name
                                    fields[0] = contig_mapping[query_name]
                                
                                # Write the modified result to the output file
                                f_out.write("\t".join(fields) + "\n")
                    
                    # Print completion message
                    print(f"Completed HMM file: {hmm_file_path}")
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(f"HMMER failed with error: {e}")
    
    print(f"HMMER process for {protein_sequences} finished. Results saved to {output_file}")
