import os
import time
from hmmer_runner import run_hmmer
from hmmer_results_parser import parse_hmmer_results
from hmmer_analysis import analyze_hmmer_results

def main():
    # Step 1: Set file paths
    protein_sequences = "input_protein_sequences.fasta"  # Input protein sequences in FASTA format
    hmmer_output_file = "hmmer_results.txt"              # Output of hmmer_runner
    parsed_hmmer_file = "parsed_hmmer_results.txt"       # Output of hmmer_results_parser
    analysis_report_file = "hmmer_analysis_report.txt"   # Final analysis report

    # Step 2: Run HMMER analysis
    print("Running HMMER scan...")
    start_time = time.time()
    run_hmmer(protein_sequences, hmmer_output_file)
    print("HMMER scan completed.")

    # Step 3: Parse HMMER results
    print("Parsing HMMER results...")
    parse_hmmer_results(hmmer_output_file, parsed_hmmer_file)
    print("Parsing completed.")

    # Step 4: Analyze parsed results
    print("Analyzing parsed HMMER results...")
    analyze_hmmer_results(parsed_hmmer_file, analysis_report_file)
    print("Analysis completed.")

    # Calculate and print the total time taken
    total_time = time.time() - start_time
    hours, rem = divmod(total_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f"Total time taken: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds.")

if __name__ == "__main__":
    main()
