import argparse
import time
from hmmer_runner import run_hmmer
from hmmer_results_parser import parse_hmmer_results
from hmmer_analysis import main as analyze_hmmer

def format_time(seconds):
    """
    Formats the elapsed time as hours, minutes, and seconds.
    
    Parameters:
    - seconds (int): The total number of elapsed seconds.

    Returns:
    - str: The formatted time in 'xx hours, xx minutes, xx seconds' format.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours} hours, {minutes} minutes, {seconds} seconds"

def main():
    """
    Main function to run the FPIdentifier pipeline, including HMMER execution, parsing, and analysis.
    """

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the FPIdentifier pipeline for TE protein identification.")
    parser.add_argument('--input', required=True, help="Path to the input protein FASTA file.")
    parser.add_argument('--output', required=True, help="Path to the output directory for results.")
    parser.add_argument('--evalue', type=float, default=1e-5, help="E-value threshold for filtering.")
    parser.add_argument('--score', type=float, default=50, help="Score threshold for filtering.")
    
    args = parser.parse_args()

    # Define file paths
    hmmer_output_file = f"{args.output}/hmmer_results.txt"
    parsed_output_file = f"{args.output}/parsed_hmmer_results.txt"
    report_file = f"{args.output}/hmmer_analysis_report.txt"

    # Start timing
    start_time = time.time()

    # Step 1: Run HMMER
    print("Running HMMER...")
    run_hmmer(args.input, hmmer_output_file)

    # Step 2: Parse and filter HMMER results
    print("Parsing and filtering HMMER results...")
    parse_hmmer_results(hmmer_output_file, parsed_output_file, e_value_threshold=args.evalue, score_threshold=args.score)

    # Step 3: Analyze the parsed results
    print("Analyzing HMMER results...")
    analyze_hmmer(parsed_output_file, report_file)

    # End timing and calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    formatted_time = format_time(int(elapsed_time))

    # Print the total time taken
    print(f"Pipeline completed. Total time taken: {formatted_time}")

if __name__ == "__main__":
    main()
