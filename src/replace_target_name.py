import re

def replace_target_with_contig(hmmer_results_file, output_file, gff_file):
    """
    Replaces the target name in the parsed HMMER results file with the corresponding contig name from the GFF file.

    Parameters:
    - hmmer_results_file (str): Path to the filtered HMMER results file.
    - output_file (str): Path to save the modified results.
    - gff_file (str): Path to the input GFF file containing contig information.

    Returns:
    - None
    """
    # Step 1: Create a dictionary to map protein sequences to contig names from the GFF file
    query_to_contig = {}
    with open(gff_file, 'r') as gff:
        for line in gff:
            if not line.startswith('#'):  # Skip comment lines
                fields = line.strip().split('\t')
                if len(fields) > 8:  # Ensure the line has enough columns
                    contig_name = fields[0]  # The contig/scaffold/Chr name is in the first column
                    attributes = fields[8]  # The attributes field contains information about the protein sequences
                    # Try to extract from ID, Parent, or Name fields, ignoring spaces and case sensitivity
                    match = re.search(r'ID\s*=\s*([^;\s]+)|Parent\s*=\s*([^;\s]+)|Name\s*=\s*([^;\s]+)', attributes, re.IGNORECASE)
                    if match:
                        query_name = match.group(1) or match.group(2) or match.group(3)
                        query_to_contig[query_name] = contig_name  # Map the protein sequence to the contig name

    # Step 2: Process the parsed HMMER results and replace the target name with contig/scaffold/Chr name
    with open(hmmer_results_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('#'):
                outfile.write(line)
            else:
                fields = line.strip().split()
                if len(fields) > 3:
                    query_name = fields[3]  # Protein sequence name is in the 4th column
                    if query_name in query_to_contig:
                        contig_name = query_to_contig[query_name]
                        fields[0] = contig_name  # Replace the first column with contig/scaffold/Chr name
                    else:
                        # If no match is found, handle the error gracefully
                        print(f"Warning: Query name {query_name} not found in the GFF file.")
                    outfile.write("\t".join(fields) + "\n")
                else:
                    outfile.write(line)

    print(f"Results saved to {output_file}")
