import argparse
import os
from data_loader import load_protein_sequences, save_sequences_to_fasta
from hmmer_runner import run_hmmer
from utils import check_file_exists, create_output_directory, print_status, validate_fasta_format
from hmmer_results_parser import parse_hmmer_results  # Importing the parse_hmmer_results function

def main():
    """
    Main function to run the FPIdentifier pipeline and detect TE proteins.
    """

    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run FPIdentifier to scan protein sequences using HMMER and GyDB.")
    parser.add_argument('--input', required=True, help="Path to the input FASTA file with protein sequences.")
    parser.add_argument('--output', required=True, help="Directory to save the hmmer_results.txt. The filtered result will also be saved to this directory.")
    
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
    
    # Step 2: Ensure the output directory exists
    create_output_directory(output_dir)

    # Define the output file paths
    hmmer_output_file = os.path.join(output_dir, "hmmer_results.txt")  # Automatically generate hmmer_results.txt
    filtered_output_file = os.path.join(output_dir, "parsed_hmmer_results.txt")

    # Step 3: Load the protein sequences
    print_status("Loading protein sequences")
    protein_sequences = load_protein_sequences(input_protein_file)
    print(f"Loaded {len(protein_sequences)} protein sequences.")
    
    # Step 4: Optionally save the loaded sequences for verification
    saved_fasta = os.path.join(output_dir, "saved_input_sequences.fasta")
    save_sequences_to_fasta(protein_sequences, saved_fasta)

    # Step 5: Run HMMER to scan the sequences against GyDB models
    print_status("Running HMMER")
    run_hmmer(input_protein_file, hmmer_output_file)  # Save hmmer_results.txt to the user-specified directory
    
    # Step 6: Parse and filter HMMER results based on E-value
    print_status("Parsing and filtering HMMER results")
    parse_hmmer_results(hmmer_output_file, filtered_output_file)
    
    # Final status update
    print_status(f"Pipeline completed. Filtered results saved to: {filtered_output_file}")


if __name__ == "__main__":
    main()
