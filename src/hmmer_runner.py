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

    # Ensure that hmmpress has been applied to the HMM files
    for hmm_file in os.listdir(hmm_model_dir):
        if hmm_file.endswith(".hmm"):
            hmm_file_path = os.path.join(hmm_model_dir, hmm_file)
            try:
                print(f"Running hmmpress on {hmm_file_path}")
                subprocess.run(f"hmmpress {hmm_file_path}", shell=True, check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"hmmpress failed on {hmm_file_path} with error: {e}")

    # Construct the HMMER command
    cmd = f"hmmscan --domtblout {output_file} {hmm_model_dir}/*.hmm {protein_sequences}"

    # Information prompt: Start running HMMER
    print(f"Running HMMER on {protein_sequences} using models from {hmm_model_dir}...")
    
    try:
        # Check if the output directory exists; if not, create it
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        # Execute the HMMER command
        subprocess.run(cmd, shell=True, check=True)
        print(f"HMMER run completed successfully. Results saved to {output_file}")
    
    except subprocess.CalledProcessError as e:
        # Capture command execution errors
        raise RuntimeError(f"HMMER failed with error: {e}")
    
    except FileNotFoundError:
        # Handle missing files (input or model)
        raise FileNotFoundError("Protein sequences or HMM model files not found. Please check the paths.")
    
    except PermissionError:
        # Handle permission errors if directories or files cannot be accessed
        raise PermissionError("Permission denied. Unable to write to the output directory or read input files.")
    
    except Exception as e:
        # Catch-all for any other unexpected errors
        raise RuntimeError(f"An unexpected error occurred: {e}")

    # Information prompt: Finished running
    print(f"HMMER process for {protein_sequences} finished.")

    # Add more debug output
    for hmm_file in os.listdir(hmm_model_dir):
        if hmm_file.endswith('.hmm'):
            current_hmm_path = os.path.join(hmm_model_dir, hmm_file)
            print(f"Processing HMM file: {current_hmm_path}")
            cmd = f"hmmscan --domtblout {output_file} {current_hmm_path} {protein_sequences}"
            try:
                subprocess.run(cmd, shell=True, check=True)
                print(f"Completed HMM file: {current_hmm_path}")
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"HMMER failed with error: {e}")

# Example of how to run the function
if __name__ == "__main__":
    # Set test input and output for demonstration purposes
    protein_sequences = "data/test_protein_sequences.fasta"
    output_dir = "output/hmmer_results"
    
    # Run the HMMER function
    run_hmmer(protein_sequences, output_dir)

