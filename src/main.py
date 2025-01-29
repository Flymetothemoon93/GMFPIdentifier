import os
import time  # Import time module for runtime calculation
from hmmer_runner import run_hmmer
from hmmer_filter import filter_hmmer_results
from extract_fasta_sequences import extract_sequences
from interproscan_runner import run_interproscan
from generate_report import generate_report

def main(input_fasta, output_dir):
    """
    Main function to run the pipeline.

    Parameters:
        input_fasta (str): Path to the input FASTA file containing protein sequences.
        output_dir (str): Path to the output directory to save results.
    """
    # Start timing the pipeline
    start_time = time.time()

    # Get the current directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define fixed path for the transposon InterPro JSON file
    transposon_json = os.path.join(current_dir, "../database/transposon_interpro.json")

    # Check if JSON file exists
    if not os.path.exists(transposon_json):
        raise FileNotFoundError(f"Transposon JSON file not found: {transposon_json}")

    # Check if INTERPROSCAN_PATH environment variable is set
    interproscan_path = os.environ.get("INTERPROSCAN_PATH")
    if not interproscan_path:
        raise EnvironmentError("Please set the INTERPROSCAN_PATH environment variable to the InterProScan installation path.")
    
    try:
        # Step 1: Run HMMER analysis
        hmmer_output = os.path.join(output_dir, "hmmer_results.txt")
        print("[Step 1] Running HMMER analysis...")
        run_hmmer(input_fasta, hmmer_output)
        print(f"HMMER results saved to: {hmmer_output}")

        # Step 2: Filter HMMER results
        filtered_hmmer_output = os.path.join(output_dir, "filtered_hmmer_results.txt")
        print("\n[Step 2] Filtering HMMER results...")
        filter_hmmer_results(hmmer_output, filtered_hmmer_output)
        print(f"Filtered HMMER results saved to: {filtered_hmmer_output}")

        # Step 3: Extract protein sequences for InterProScan
        filtered_fasta_output = os.path.join(output_dir, "filtered_sequences.fasta")
        print("\n[Step 3] Extracting protein sequences...")
        extract_sequences(filtered_hmmer_output, input_fasta, filtered_fasta_output)
        print(f"Filtered sequences saved to: {filtered_fasta_output}")

        # Step 4: Run InterProScan
        interproscan_output = os.path.join(output_dir, "interproscan_results.tsv")
        print("\n[Step 4] Running InterProScan...")
        run_interproscan(filtered_fasta_output, interproscan_output)
        print(f"InterProScan results saved to: {interproscan_output}")

        # Step 5: Generate final report and filtered TSV
        report_output = os.path.join(output_dir, "GMFPIdentifier_report.txt")
        tsv_output = os.path.join(output_dir, "GMFPIdentifier_results.tsv")
        print("\n[Step 5] Generating final report and TSV...")

        # Calculate runtime and pass it to the report generation function
        end_time = time.time()
        runtime_seconds = end_time - start_time

        generate_report(interproscan_output, report_output, tsv_output, transposon_json, runtime_seconds)
        print(f"Final report saved to: {report_output}")
        print(f"Filtered TSV saved to: {tsv_output}")

        print("\nPipeline completed successfully. Results are saved in the specified output directory.")
    
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Automate transposon protein prediction and annotation pipeline.")
    parser.add_argument("--input", required=True, help="Path to the input protein sequences in FASTA format.")
    parser.add_argument("--output", required=True, help="Path to the output directory.")
    args = parser.parse_args()

    # Ensure the output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    main(args.input, args.output)
