import argparse
import os
from data_loader import load_protein_sequences, save_sequences_to_fasta
from hmmer_runner import run_hmmer
from utils import check_file_exists, create_output_directory, print_status, validate_fasta_format

def main():
    """
    Main function to run the FPIdentifier pipeline and detect TE proteins.
    """

    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run FPIdentifier to scan protein sequences using HMMER and GyDB.")
    parser.add_argument('--input', required=True, help="Path to the input FASTA file with protein sequences.")
    parser.add_argument('--output', required=True, help="Directory or file to save the output results.")
    
    # Parse arguments
    args = parser.parse_args()
    input_protein_file = args.input
    output_path = args.output

    # Step 1: Check input file and validate
    try:
        print_status("Validating input file")
        check_file_exists(input_protein_file)
        validate_fasta_format(input_protein_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return
    
    # Step 2: Handle output path (can be file or directory)
    if output_path.endswith('.txt'):
        output_file = output_path
        output_dir = os.path.dirname(output_file) or "."
    else:
        output_dir = output_path
        output_file = os.path.join(output_dir, "hmmer_results.txt")
    
    create_output_directory(output_dir)

    # Step 3: Load the protein sequences
    print_status("Loading protein sequences")
    protein_sequences = load_protein_sequences(input_protein_file)
    print(f"Loaded {len(protein_sequences)} protein sequences.")
    
    # Step 4: Optionally save the loaded sequences for verification
    saved_fasta = os.path.join(output_dir, "saved_input_sequences.fasta")
    save_sequences_to_fasta(protein_sequences, saved_fasta)

    # Step 5: Run HMMER to scan the sequences against GyDB models
    print_status("Running HMMER")
    run_hmmer(input_protein_file, output_file)
    
    # Final status update
    print_status(f"HMMER scan completed. Check the results in: {output_file}")
  
if __name__ == "__main__":
    main()
