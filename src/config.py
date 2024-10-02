# Configuration settings for FPIdentifier project

# Set the paths for input files and directories
INPUT_PROTEIN_FILE = "data/input_protein_sequences.fasta"  # Input FASTA file with protein sequences
OUTPUT_DIR = "output/"  # Directory for storing output files
HMM_MODEL_DIR = "database/Gydb/"  # Directory where the HMM profiles are stored

# Default parameters for the HMMER tool
HMMER_EXECUTABLE = "hmmscan"  # HMMER tool command for scanning protein sequences
HMMER_DOMTBL_OUTPUT = "hmmer_results.txt"  # Output file for domain table results

# Threshold settings for HMMER scan
E_VALUE_THRESHOLD = 1e-5  # E-value threshold for domain matches
