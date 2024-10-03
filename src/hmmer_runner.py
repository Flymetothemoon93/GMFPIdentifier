import subprocess
import os

def run_hmmer(protein_sequences, output_dir):
    """
    Runs the HMMER tool to scan the provided protein sequences using HMM models from GyDB.

    Parameters:
    - protein_sequences (str): Path to the input protein sequences in FASTA format.
    - output_dir (str): Directory where the results should be saved.

    Returns:
    - None: Outputs the results to a file in the output directory.
    """

    # Define the HMM model directory
    hmm_model_dir = 'database/GyDB'
    output_file = os.path.join(output_dir, 'hmmer_results.txt')

    # Ensure HMM model directory and protein sequences file exist
    if not os.path.exists(hmm_model_dir):
        raise FileNotFoundError(f"HMM model directory not found: {hmm_model_dir}")
    if not os.path.isfile(protein_sequences):
        raise FileNotFoundError(f"Protein sequences file not found: {protein_sequences}")

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Open the output file for appending the results
    with open(output_file, 'w') as f_out:
        # Iterate through all .hmm files in the GyDB directory
        for hmm_file in os.listdir(hmm_model_dir):
            if hmm_file.endswith('.hmm'):
                hmm_file_path = os.path.join(hmm_model_dir, hmm_file)
                print(f"Processing HMM file: {hmm_file_path}")

                # Construct the HMMER command for each HMM file
                cmd = f"hmmscan --domtblout /dev/stdout {hmm_file_path} {protein_sequences}"
                
                try:
                    # Run HMMER and append the results to the output file
                    subprocess.run(cmd, shell=True, check=True, stdout=f_out)
                    print(f"Completed HMM file: {hmm_file_path}")
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(f"HMMER failed with error: {e}")

    print(f"HMMER process for {protein_sequences} finished. Results saved to {output_file}")
