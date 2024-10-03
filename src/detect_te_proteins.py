import os

# TE-related domains set
TE_DOMAINS = set()

def load_all_hmm_domains(hmm_dir):
    """
    Load all domain names from HMM files in GyDB.
    
    Args:
    - hmm_dir (str): Path to the directory containing HMM files.
    
    Returns:
    - None: Populates the global TE_DOMAINS set.
    """
    global TE_DOMAINS
    for hmm_file in os.listdir(hmm_dir):
        if hmm_file.endswith(".hmm"):
            domain_name = hmm_file.split('.')[0]  # Use filename as domain
            TE_DOMAINS.add(domain_name)

def parse_hmmer_results(hmmer_output, output_file, e_value_threshold=1e-5):
    """
    Parse HMMER results and extract TE-related hits based on E-value threshold.
    
    Args:
    - hmmer_output (str): Path to the HMMER results file.
    - output_file (str): Path to the output file for filtered results.
    - e_value_threshold (float): E-value threshold to filter significant hits.
    
    Returns:
    - None
    """
    with open(hmmer_output, 'r') as infile, open(output_file, 'w') as outfile:
        outfile.write("Protein ID\tDomain\tE-value\n")
        for line in infile:
            if line.startswith('#'):  # Skip comment lines
                continue

            fields = line.split()
            if len(fields) < 5:
                continue  # Ensure line has enough fields
            
            domain = fields[0]       # Domain from HMMER result
            e_value = float(fields[4])  # E-value from HMMER result
            protein_id = fields[3]   # Protein ID

            # Check if domain is in known TE domains and passes E-value threshold
            if domain in TE_DOMAINS and e_value <= e_value_threshold:
                outfile.write(f"{protein_id}\t{domain}\t{e_value}\n")
    
    print(f"Filtered results saved to {output_file}")

# Example usage:
hmm_dir = "database/GyDB"
hmmer_output = "hmmer_results.txt"  # Your HMMER output file
output_file = "filtered_te_results.txt"  # Output filtered results

# Load all HMM domain names from GyDB
load_all_hmm_domains(hmm_dir)

# Parse HMMER results
parse_hmmer_results(hmmer_output, output_file)
