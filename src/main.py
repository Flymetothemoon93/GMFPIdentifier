import os
from hmmer_runner import run_hmmer
from hmmer_filter import filter_hmmer_results
from extract_fasta_sequences import extract_sequences
from interproscan_runner import run_interproscan
from generate_report import generate_report

def main(input_fasta, output_dir):
    # Check if INTERPROSCAN_PATH environment variable is set
    interproscan_path = os.environ.get("INTERPROSCAN_PATH")
    if not interproscan_path:
        raise EnvironmentError("Please set the INTERPROSCAN_PATH environment variable to the InterProScan installation path.")
    
    # Step 1: Run HMMER analysis
    hmmer_output = os.path.join(output_dir, "hmmer_results.txt")
    print("Step 1: Running HMMER analysis...")
    run_hmmer(input_fasta, hmmer_output)
    
    # Step 2: Filter HMMER results
    filtered_hmmer_output = os.path.join(output_dir, "filtered_hmmer_results.txt")
    print("Step 2: Filtering HMMER results...")
    filter_hmmer_results(hmmer_output, filtered_hmmer_output)

    # Step 3: Extract protein sequences for InterProScan
    filtered_fasta_output = os.path.join(output_dir, "filtered_sequences.fasta")
    print("Step 3: Extracting protein sequences...")
    extract_sequences(filtered_hmmer_output, input_fasta, filtered_fasta_output)

    # Step 4: Run InterProScan
    interproscan_output = os.path.join(output_dir, "interproscan_results.tsv")
    print("Step 4: Running InterProScan...")
    run_interproscan(filtered_fasta_output, interproscan_output)

    # Step 5: Generate final report
    report_output = os.path.join(output_dir, "FPIdentifier_report.txt")
    print("Step 5: Generating final report...")
    generate_report(interproscan_output, report_output)

    print("Pipeline completed successfully. Results are saved in the specified output directory.")

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
