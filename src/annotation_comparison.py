import subprocess
import os

def convert_to_bed(hmmer_results_file, bed_output_file):
    """
    Converts parsed and modified HMMER results to BED format.
    
    Parameters:
    - hmmer_results_file (str): Path to the HMMER results file where target names have been replaced by contig names.
    - bed_output_file (str): Path to the output BED file.
    
    Returns:
    - None
    """
    with open(hmmer_results_file, 'r') as infile, open(bed_output_file, 'w') as outfile:
        for line in infile:
            # Skip comment lines or empty lines
            if line.startswith('#') or not line.strip():
                continue
            
            fields = line.strip().split()
            
            # Extract the relevant fields
            chromosome = fields[0]  # Contig name (which was originally the target name)
            start = fields[15]  # HMM alignment start (hm coord 'from')
            end = fields[16]    # HMM alignment end (hm coord 'to')
            name = fields[3]    # Query name (e.g., protein or TE name)
            score = fields[6]   # E-value (or another score)

            # Write to BED format (chromosome, start, end, name, score)
            bed_line = f"{chromosome}\t{start}\t{end}\t{name}\t{score}\n"
            outfile.write(bed_line)
    
    print(f"Converted HMMER results to BED format: {bed_output_file}")


def compare_with_annotations(hmmer_bed_file, annotation_file, output_dir):
    """
    Uses Bedtools to compare the HMMER results (in BED format) with gene annotations (GFF format).
    
    Parameters:
    - hmmer_bed_file (str): Path to the HMMER results in BED format.
    - annotation_file (str): Path to the gene annotation file in GFF format.
    - output_dir (str): Directory where te_gene_overlaps.bed should be saved.
    
    Returns:
    - None
    """
    output_file = os.path.join(output_dir, "te_gene_overlaps.bed")  # Ensure the result is saved as te_gene_overlaps.bed
    
    # Construct the Bedtools intersect command
    cmd = f"bedtools intersect -a {hmmer_bed_file} -b {annotation_file} -wa -wb > {output_file}"
    
    try:
        # Run the Bedtools command
        subprocess.run(cmd, shell=True, check=True)
        print(f"Comparison completed. Overlapping regions saved to {output_file}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Bedtools comparison failed: {e}")
