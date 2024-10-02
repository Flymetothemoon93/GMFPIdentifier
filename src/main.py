import argparse
import os
from data_loader import load_protein_sequences, save_sequences_to_fasta
from hmmer_runner import run_hmmer
from utils import check_file_exists, create_output_directory, print_status, validate_fasta_format

def main():
    """
    Main function to run the FPIdentifier pipeline using command-line arguments.
    """

    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run FPIdentifier to scan protein sequences using HMMER and GyDB.")
    parser.add_argument('--input', required=True, help="Path to the input FASTA file with protein sequences.")
    parser.add_argument('--output', required=True, help="Directory to save the output files.")
    
    # Parse arguments
    args = parser.parse_args()
    input_protein_file = args.input
    output_dir = args.output

    # Step 1: Check input file and validate
    try:
        print_status("Validating input file")
        check_file_exists(input_protein_file)
        validate_fasta_format(input_protein_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return
    
    # Step 2: Create output directory if not exists
    def create_output_directory(directory_path):
    """
    Creates the output directory if it doesn't exist. 
    If it already exists, this function does nothing.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Output directory created: {directory_path}")
    else:
        print(f"Output directory already exists: {directory_path}")

    # Step 3: Load the protein sequences
    print_status("Loading protein sequences")
    protein_sequences = load_protein_sequences(input_protein_file)
    print(f"Loaded {len(protein_sequences)} protein sequences.")
    
    # Step 4: Optionally save the loaded sequences for verification
    output_fasta = os.path.join(output_dir, "saved_input_sequences.fasta")
    save_sequences_to_fasta(protein_sequences, output_fasta)

    # Step 5: Run HMMER to scan the sequences against GyDB models
    print_status("Running HMMER")
    run_hmmer(input_protein_file, output_dir)
    
    # Final status update
    print_status("HMMER scan completed. Check the output directory for results.")

if __name__ == "__main__":
    main()
