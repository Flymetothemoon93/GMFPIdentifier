def parse_hmmer_results(hmmer_results_file, output_file, e_value_threshold=1e-5, score_threshold=50):
    """
    Parses HMMER output file and filters based on both E-value and score.

    Parameters:
    - hmmer_results_file (str): Path to the HMMER output file.
    - output_file (str): Path to the filtered output file.
    - e_value_threshold (float): E-value threshold for filtering. Default is 1e-5.
    - score_threshold (float): Score threshold for filtering. Default is 50.

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
                
                # Extract the E-value from the 7th column (index 6) and score from the 8th column (index 7)
                try:
                    e_value = float(fields[6])
                    score = float(fields[7])
                except (ValueError, IndexError):
                    # If E-value or score cannot be converted to float, or columns are missing, skip this line
                    continue
                
                # Apply both the E-value and score filters
                if e_value <= e_value_threshold and score >= score_threshold:
                    outfile.write(line)  # Write the filtered line to the output file

        print(f"Filtered results saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {hmmer_results_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
