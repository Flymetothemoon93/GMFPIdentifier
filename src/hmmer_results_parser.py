def parse_hmmer_results(hmmer_results_file, output_file, e_value_threshold=1e-5, score_threshold=50, min_coverage=0.5, min_length=50, max_bias=1.0, min_bit_score=100):
    """
    Parses HMMER output file and filters based on multiple criteria including E-value, score, coverage, length, bias, and bit score.

    Parameters:
    - hmmer_results_file (str): Path to the HMMER output file.
    - output_file (str): Path to the filtered output file.
    - e_value_threshold (float): E-value threshold for filtering. Default is 1e-5.
    - score_threshold (float): Score threshold for filtering. Default is 50.
    - min_coverage (float): Minimum coverage threshold for filtering. Default is 0.5 (50%).
    - min_length (int): Minimum alignment length for filtering. Default is 50.
    - max_bias (float): Maximum bias threshold for filtering. Default is 1.0.
    - min_bit_score (float): Minimum bit score threshold for filtering. Default is 100.

    Returns:
    - None
    """
    try:
        with open(hmmer_results_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                if line.startswith('#'):  # Skip comment lines
                    continue
                
                # Split the line into columns based on whitespace or tab
                fields = line.strip().split()
                
                # Extract relevant fields (index values are based on the format of --domtblout)
                try:
                    e_value = float(fields[6])  # E-value
                    score = float(fields[7])  # Score
                    bias = float(fields[8])  # Bias
                    bit_score = float(fields[5])  # Bit Score
                    qlen = int(fields[5])  # Query length
                    ali_from = int(fields[17])  # Alignment start position
                    ali_to = int(fields[18])  # Alignment end position
                except (ValueError, IndexError):
                    # If any field is missing or cannot be converted, skip this line
                    continue
                
                # Calculate alignment length and coverage
                alignment_length = ali_to - ali_from + 1
                coverage = alignment_length / qlen

                # Apply all filters (E-value, score, coverage, length, bias, bit score)
                if (e_value <= e_value_threshold and
                    score >= score_threshold and
                    coverage >= min_coverage and
                    alignment_length >= min_length and
                    bias <= max_bias and
                    bit_score >= min_bit_score):
                    outfile.write(line)  # Write the filtered line to the output file

        print(f"Filtered results saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {hmmer_results_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
