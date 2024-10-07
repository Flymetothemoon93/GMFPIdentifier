import os

def parse_hmmer_results(hmmer_results_file, output_file, e_value_threshold=1e-5):
    """
    Parses HMMER output file and filters based on E-value.

    Parameters:
    - hmmer_results_file (str): Path to the HMMER output file.
    - output_file (str): Path to the filtered output file.
    - e_value_threshold (float): E-value threshold for filtering. Default is 1e-5.

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
                
                # Extract the E-value from the 7th column (index 6, as index starts at 0)
                try:
                    e_value = float(fields[6])
                except ValueError:
                    # If the E-value cannot be converted to float, skip this line
                    continue
                
                # Keep only the results with E-value <= e_value_threshold
                if e_value <= e_value_threshold:
                    outfile.write(line)  # Write the filtered line to the output file

        print(f"Filtered results saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {hmmer_results_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Define the input and output file paths
    hmmer_results_file = "hmmer_results.txt"  # Input file path from HMMER
    output_file = "parsed_hmmer_results.txt"  # Output file for filtered results

    # Call the function to parse and filter the HMMER results
    parse_hmmer_results(hmmer_results_file, output_file)

if __name__ == "__main__":
    main()
