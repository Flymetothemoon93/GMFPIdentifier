import subprocess
import argparse
import os
from data_loader import load_protein_sequences, save_sequences_to_fasta
from hmmer_runner import run_hmmer
from utils import check_file_exists, create_output_directory, print_status, validate_fasta_format
from hmmer_results_parser import parse_hmmer_results
from annotation_comparison import convert_to_bed, compare_with_annotations
from validation_summary import generate_report_and_statistics

def main():
    """
    Main function to run the FPIdentifier pipeline, detect TE proteins, and compare with gene annotations.
    """

    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run FPIdentifier to scan protein sequences using HMMER and GyDB, and compare with gene annotations.")
    parser.add_argument('--input', required=True, help="Path to the input FASTA file with protein sequences.")
    parser.add_argument('--annotation', required=True, help="Path to the gene annotation file (GFF format).")
    parser.add_argument('--output', required=True, help="Directory to save the hmmer_results.txt and comparison results.")
    
    # Parse arguments
    args = parser.parse_args()
    input_protein_file = args.input
    annotation_file = args.annotation
    output_dir = args.output

    # Step 1: Check input files and validate
    try:
        print_status("Validating input files")
        check_file_exists(input_protein_file)
        check_file_exists(annotation_file)
        validate_fasta_format(input_protein_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return
    
    # Step 2: Ensure the output directory exists
    create_output_directory(output_dir)

    # Define the output file paths
    hmmer_output_file = os.path.join(output_dir, "hmmer_results.txt")  # Automatically generate hmmer_results.txt
    filtered_output_file = os.path.join(output_dir, "parsed_hmmer_results.txt")
    bed_output_file = os.path.join(output_dir, "hmmer_results.bed")  # Intermediate BED file for TE proteins

    # Step 3: Load the protein sequences
    print_status("Loading protein sequences")
    protein_sequences = load_protein_sequences(input_protein_file)
    print(f"Loaded {len(protein_sequences)} protein sequences.")
    
    # Step 4: Optionally save the loaded sequences for verification
    saved_fasta = os.path.join(output_dir, "saved_input_sequences.fasta")
    save_sequences_to_fasta(protein_sequences, saved_fasta)

    # Step 5: Run HMMER to scan the sequences against GyDB models
    print_status("Running HMMER")
    run_hmmer(input_protein_file, hmmer_output_file)
    
    # Step 6: Parse and filter HMMER results based on E-value
    print_status("Parsing and filtering HMMER results")
    parse_hmmer_results(hmmer_output_file, filtered_output_file)
    
    # Step 7: 替换 target name 为 contig name
    print_status("Replacing target name with contig name")
    subprocess.run(["python", "replace_target_name.py", hmmer_output_file, os.path.join(output_dir, "hmmer_results_modified.txt"), input_protein_file])
    
    # Step 8: Convert parsed results to BED format and compare with annotations
    print_status("Converting parsed results to BED format")
    convert_to_bed(filtered_output_file, bed_output_file)

    print_status("Comparing TE proteins with gene annotations")
    compare_with_annotations(bed_output_file, annotation_file, output_dir)
    
    # Step 9: Generate validation summary report and statistics
    print_status("Generating validation summary report and statistics")
    report_file = os.path.join(output_dir, "FPIdentifier.report.txt")
    statistics_file = os.path.join(output_dir, "FPIdentifier.statistics.txt")
    generate_report_and_statistics(output_dir, report_file, statistics_file)
    
    # Final status
    print_status(f"Pipeline completed. Gene overlap results saved to: {os.path.join(output_dir, 'te_gene_overlaps.bed')}")
    print_status(f"Validation summary report saved to: {report_file}")
    print_status(f"Statistics file saved to: {statistics_file}")


if __name__ == "__main__":
    main()
