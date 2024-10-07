import argparse
import os
from data_loader import load_protein_sequences, save_sequences_to_fasta
from hmmer_runner import run_hmmer
from utils import check_file_exists, create_output_directory, print_status, validate_fasta_format
from hmmer_results_parser import parse_hmmer_results

def main():
    """
    Main function to run the FPIdentifier pipeline and detect TE proteins.
    """

    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run FPIdentifier to scan protein sequences using HMMER and GyDB.")
    parser.add_argument('--input', required=True, help="Path to the input FASTA file with protein sequences.")
    parser.add_argument('--output', required=True, help="Directory to save the output results. The file will always be saved as hmmer_results.txt.")
    
    # Parse arguments
    args = parser.parse_args()
    input_protein_file = args.input  # Get the input protein sequences file path
    output_dir = args.output  # Get the user-specified output directory

    # Step 1: Check if the input file exists and validate the format
    try:
        print_status("Validating input file")  # Print status message
        check_file_exists(input_protein_file)  # Check if the input file exists
        validate_fasta_format(input_protein_file)  # Validate that the input file is in FASTA format
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")  # If there's an error, print the message
        return  # Stop execution
    
    # Step 2: Ensure the output path is always a directory, and set the output file to hmmer_results.txt
    output_file = os.path.join(output_dir, "hmmer_results.txt")  # Force output file to be hmmer_results.txt
    create_output_directory(output_dir)  # Ensure the output directory exists, create it if not

    # Step 3: Load the protein sequences
    print_status("Loading protein sequences")  # Print status message
    protein_sequences = load_protein_sequences(input_protein_file)  # Load the input protein sequences
    print(f"Loaded {len(protein_sequences)} protein sequences.")  # Print the number of loaded protein sequences
    
    # Step 4: Optionally save the loaded sequences for verification
    saved_fasta = os.path.join(output_dir, "saved_input_sequences.fasta")  # Define the path to save the loaded sequences
    save_sequences_to_fasta(protein_sequences, saved_fasta)  # Save the loaded sequences to a FASTA file

    # Step 5: Run HMMER to scan the protein sequences against GyDB models
    print_status("Running HMMER")  # Print status message
    run_hmmer(input_protein_file, output_file)  # Run HMMER and save results to the output file
    
    # Step 6: Parse and filter HMMER results based on E-value
    print_status("Parsing and filtering HMMER results")
    parse_hmmer_results(hmmer_output_file, filtered_output_file)
    
    # Final status update
    print_status(f"Pipeline completed. Filtered results saved to: {filtered_output_file}")


if __name__ == "__main__":
    main()
