import os
import time  # Import time module for runtime calculation
from hmmer_runner import run_hmmer
from hmmer_filter import filter_hmmer_results
from extract_fasta_sequences import extract_sequences
from interproscan_runner import run_interproscan
from generate_report import generate_report

def main(input_fasta, output_dir, threads, json_path=None):
    """
    Main function to run the GMFPIdentifier pipeline.
    """
    # Start timing the pipeline
    start_time = time.time()
    
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Determine the path for the transposon InterPro JSON file
    if json_path:
        transposon_json = json_path
    else:
        # Use the default JSON file based on the environment
        docker_json_path = "/app/database/transposon_interpro.json"  # For Docker
        local_json_path = os.path.abspath(os.path.join(current_dir, "../database/transposon_interpro.json"))

        # Prioritize the local JSON file if it exists; otherwise, use the Docker path
        transposon_json = local_json_path if os.path.exists(local_json_path) else docker_json_path

    # Verify that the JSON file exists
    if not os.path.exists(transposon_json):
        raise FileNotFoundError(f"Transposon JSON file not found: {transposon_json}")

    # Ensure INTERPROSCAN_PATH is set
    interproscan_path = os.environ.get("INTERPROSCAN_PATH")
    if not interproscan_path:
        raise EnvironmentError("Please set the INTERPROSCAN_PATH environment variable to the InterProScan installation path.")

    try:
        # Step 1: Run HMMER analysis
        hmmer_output = os.path.join(output_dir, "hmmer_results.txt")
        print("Step 1: Running HMMER analysis...", flush=True)
        run_hmmer(input_fasta, hmmer_output, threads)
        print(f"HMMER results saved to: {hmmer_output}", flush=True)

        # Step 2: Filter HMMER results
        filtered_hmmer_output = os.path.join(output_dir, "filtered_hmmer_results.txt")
        print("\nStep 2: Filtering HMMER results...", flush=True)
        filter_hmmer_results(hmmer_output, filtered_hmmer_output)
        print(f"Filtered HMMER results saved to: {filtered_hmmer_output}", flush=True)

        # Step 3: Extract protein sequences for InterProScan
        filtered_fasta_output = os.path.join(output_dir, "filtered_sequences.fasta")
        print("\nStep 3: Extracting protein sequences...", flush=True)
        extract_sequences(filtered_hmmer_output, input_fasta, filtered_fasta_output)
        print(f"Extracted sequences saved to: {filtered_fasta_output}", flush=True)

        # Step 4: Run InterProScan
        interproscan_output = os.path.join(output_dir, "interproscan_results.tsv")
        print("\nStep 4: Running InterProScan...", flush=True)
        run_interproscan(filtered_fasta_output, interproscan_output, threads)
        print(f"InterProScan results saved to: {interproscan_output}", flush=True)

        # Step 5: Generate final report and filtered TSV
        report_output = os.path.join(output_dir, "GMFPIdentifier_report.txt")
        tsv_output = os.path.join(output_dir, "GMFPIdentifier_results.tsv")
        print("\nStep 5: Generating final report and TSV...", flush=True)
        print(f"Using transposon JSON file: {transposon_json}", flush=True)
        # Calculate runtime and pass it to the report generation function
        end_time = time.time()
        runtime_seconds = end_time - start_time

        generate_report(interproscan_output, report_output, tsv_output, transposon_json, runtime_seconds)
        print(f"Final report saved to: {report_output}", flush=True)
        print(f"Filtered TSV saved to: {tsv_output}", flush=True)

        print("\nPipeline completed successfully. Results are saved in the specified output directory.", flush=True)

    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Automate transposon protein prediction and annotation pipeline.")
    parser.add_argument("--input", required=True, help="Path to the input protein sequences in FASTA format.")
    parser.add_argument("--output", required=True, help="Path to the output directory.")
    parser.add_argument("--threads", type=int, default=1, help="Number of CPU threads to use (default: 1).")
    parser.add_argument("--json", required=False, help="Path to a custom transposon JSON file (optional).")
    args = parser.parse_args()

    # Ensure the output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    main(args.input, args.output, args.threads, args.json)
