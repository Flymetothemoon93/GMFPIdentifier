def filter_hmmer_results(hmmer_results_file, output_file, e_value_threshold=1e-5, score_threshold=50, coverage_threshold=0.5):
    """
    Parses HMMER output file and filters based on e-value, score, and coverage relative to HMM model length.

    Parameters:
    - hmmer_results_file (str): Path to the HMMER output file.
    - output_file (str): Path to the filtered output file.
    - e_value_threshold (float): E-value threshold for filtering. Default is 1e-5.
    - score_threshold (float): Score threshold for filtering. Default is 50.
    - coverage_threshold (float): Coverage threshold for filtering, relative to HMM model length. Default is 0.5 (50%).

    Returns:
    - None: Saves the filtered results to output_file.
    """
    try:
        filtered_count = 0  # Counter for the number of filtered entries
        
        with open(hmmer_results_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                if line.startswith('#'):  # Skip comment lines
                    continue
                
                # Split the line into columns based on whitespace
                fields = line.strip().split()
                
                try:
                    # Extract relevant columns (assuming standard HMMER output format)
                    e_value = float(fields[6])
                    score = float(fields[7])
                    alignment_start = int(fields[17])  # Alignment start in target
                    alignment_end = int(fields[18])    # Alignment end in target
                    hmm_length = int(fields[2])  # The HMM model length is in column index 2
                    
                    # Calculate coverage relative to HMM model length
                    alignment_length = alignment_end - alignment_start + 1
                    coverage = alignment_length / hmm_length

                except (ValueError, IndexError):
                    # Skip lines with missing or non-numeric values
                    continue
                
                # Apply filters
                if (
                    e_value <= e_value_threshold and
                    score >= score_threshold and
                    coverage >= coverage_threshold
                ):
                    outfile.write(line)  # Write the filtered line to the output file
                    filtered_count += 1

        # print(f"Filtered HMMER results saved to {output_file}. Total filtered entries: {filtered_count}", flush=True)

    except FileNotFoundError:
        print(f"Error: The file {hmmer_results_file} was not found.", flush=True)
    except Exception as e:
        print(f"An error occurred: {e}", flush=True)
