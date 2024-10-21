import os
import time
import argparse
from hmmer_runner import run_hmmer
from hmmer_results_parser import parse_hmmer_results
from hmmer_analysis import analyze_hmmer_results

def main():
    # Set up argument parser to allow user input for input/output files
    parser = argparse.ArgumentParser(description="Run HMMER analysis pipeline.")
    
    parser.add_argument('--input', type=str, required=True, help="Path to the input protein sequences FASTA file.")
    parser.add_argument('--output_dir', type=str, required=True, help="Directory to save the HMMER results and reports.")
    
    args = parser.parse_args()
    
    # Paths to the input and output files
    protein_sequences = args.input  # Input protein sequences file (from user)
    output_dir = args.output_dir    # Output directory (from user)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Output files    hmmer_output_file = os.path.join(output_dir, "hmmer_results.txt")         # Output of hmmer_runner
    parsed_hmmer_file = os.path.join(output_dir, "parsed_hmmer_results.txt")  # Output of hmmer_results_parser
    analysis_report_file = os.path.join(output_dir, "hmmer_analysis_report.txt")  # Final analysis report

    # Step 2: Run HMMER analysis
    print(f"Running HMMER scan on {protein_sequences}...")
    start_time = time.time()
    run_hmmer(protein_sequences, hmmer_output_file)
    print("HMMER scan completed.")

    # Step 3: Parse HMMER results
    print(f"Parsing HMMER results from {hmmer_output_file}...")
    parse_hmmer_results(hmmer_output_file, parsed_hmmer_file)
    print(f"Parsing completed. Parsed results saved to {parsed_hmmer_file}.")

    # Step 4: Analyze parsed results
    print(f"Analyzing parsed HMMER results from {parsed_hmmer_file}...")
    analyze_hmmer_results(parsed_hmmer_file, analysis_report_file)
    print(f"Analysis completed. Report saved to {analysis_report_file}.")

    # Calculate and print the total time taken
    total_time = time.time() - start_time
    hours, rem = divmod(total_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f"Total time taken: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds.")

if __name__ == "__main__":
    main()
