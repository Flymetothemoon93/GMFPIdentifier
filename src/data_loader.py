from Bio import SeqIO

def load_protein_sequences(file_path):
    """
    Loads protein sequences from a FASTA file using SeqIO.
    
    Parameters:
    - file_path (str): Path to the input FASTA file.
    
    Returns:
    - dict: A dictionary where the keys are sequence headers and the values are protein sequences.
    """
    sequences = {}
    
    # Use SeqIO to read the FASTA file
    for record in SeqIO.parse(file_path, "fasta"):
        sequences[record.description] = str(record.seq)  # Use the full header, not just the ID
    
    # Check if no sequences were loaded
    if not sequences:
        raise ValueError("No sequences were found in the file. Please check if the file is in valid FASTA format.")
    
    return sequences

def save_sequences_to_fasta(sequences, output_file):
    """
    Saves a dictionary of protein sequences to a FASTA file using SeqIO.
    
    Parameters:
    - sequences (dict): A dictionary where the keys are sequence headers and the values are protein sequences.
    - output_file (str): The output file path for saving the sequences.
    
    Returns:
    - None
    """
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    
    # Create SeqRecord objects for each sequence
    records = [SeqRecord(Seq(seq), id=header.split()[0], description=header) for header, seq in sequences.items()]  # Keep full header
    
    # Write the SeqRecord objects to a FASTA file
    with open(output_file, 'w') as file:
        SeqIO.write(records, file, "fasta")
    
    print(f"Protein sequences successfully saved to {output_file}")
