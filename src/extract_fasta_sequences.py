from Bio import SeqIO

def extract_sequences(filtered_results_file, protein_sequences_file, output_fasta):
    """
    Extracts protein sequences from the filtered HMMER results and creates a FASTA file.
    """
    try:
        # Load filtered sequence IDs from the third column in the results file
        filtered_ids = set()
        with open(filtered_results_file, 'r') as f:
            for line in f:
                fields = line.strip().split()
                if len(fields) > 3:
                    protein_id = fields[3]
                    filtered_ids.add(protein_id)

        # Print the filtered IDs
        print("Filtered IDs:", filtered_ids, flush=True)

        # Extract and write matching sequences to the output FASTA file
        with open(output_fasta, 'w') as output_handle:
            matched = False
            for record in SeqIO.parse(protein_sequences_file, "fasta"):
                if record.id in filtered_ids:
                    # Remove '*' characters from the sequence using replace
                    record.seq = record.seq.replace("*", "")
                    SeqIO.write(record, output_handle, "fasta")
                    matched = True
            
            if not matched:
                print("No matching sequences found in the original FASTA file.", flush=True)

        # print(f"Extracted sequences saved to {output_fasta}", flush=True)

    except FileNotFoundError:
        print(f"Error: The file {filtered_results_file} or {protein_sequences_file} was not found.", flush=True)
    except Exception as e:
        print(f"An error occurred: {e}", flush=True)
