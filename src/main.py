import subprocess
import argparse
import os
import time
from data_loader import load_protein_sequences, save_sequences_to_fasta
from hmmer_runner import run_hmmer
from utils import check_file_exists, create_output_directory, print_status, validate_fasta_format
from hmmer_results_parser import parse_hmmer_results
from replace_target_name import replace_target_with_contig
from annotation_comparison import convert_to_bed, compare_with_annotations
from false_positive_report import generate_false_positive_report

def format_time(seconds):
    """
    Format the elapsed time in seconds into hours, minutes, and seconds.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours} hours, {minutes} minutes, {seconds} seconds"

def main():
    """
    Main function to run the FPIdentifier pipeline, detect TE proteins, and compare with gene annotations.
    """
    
    # Record the start time
    start_time = time.time()
    
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
    modified_hmmer_file = os.path.join(output_dir, "hmmer_results_modified.txt")  # The file with replaced contig names

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
    
    # Step 7: Replace target name with contig name from the FASTA file
    print_status("Replacing target name with contig name")
    replace_target_with_contig(filtered_output_file, modified_hmmer_file, input_protein_file)
    
    # Step 8: Convert parsed results to BED format and compare with annotations
    print_status("Converting parsed results to BED format")
    convert_to_bed(modified_hmmer_file, bed_output_file)

    print_status("Comparing TE proteins with gene annotations")
    compare_with_annotations(bed_output_file, annotation_file, output_dir)
    
    # Step 9: Generate false positive report (replacing validation summary)
    print_status("Generating false positive report")
    false_positive_report_file = os.path.join(output_dir, "false_positives_report.txt")
    generate_false_positive_report(os.path.join(output_dir, 'te_gene_overlaps.bed'), false_positive_report_file)
    
    # Final status
    print_status(f"Pipeline completed. Gene overlap results saved to: {os.path.join(output_dir, 'te_gene_overlaps.bed')}")
    print_status(f"False positive report saved to: {false_positive_report_file}")
    
    # Record the end time
    end_time = time.time()
    
    elapsed_time = int(end_time - start_time)
    
    formatted_time = format_time(elapsed_time)
    print(f"Total elapsed time: {formatted_time}")

if __name__ == "__main__":
    main()
