import pandas as pd

def analyze_hmmer_results(parsed_results_file, output_report_file):
    """
    Analyzes parsed HMMER results to identify unique transposable elements (TEs).
    
    Parameters:
    - parsed_results_file (str): Path to the parsed HMMER results file.
    - output_report_file (str): Path to save the analysis report.
    
    Returns:
    - None
    """
    te_counter = {}
    unique_hits = set()
    
    try:
        # Read the parsed HMMER results file
        with open(parsed_results_file, 'r') as infile:
            for line in infile:
                if line.startswith('#'):  # Skip comment lines
                    continue
                
                fields = line.strip().split()
                if len(fields) < 17:
                    continue  # Ensure we have enough fields to parse
                
                te_name = fields[0]   # TE name (first column)
                contig = fields[2]    # Contig name
                start = fields[15]    # Start position
                end = fields[16]      # End position

                # Generate a unique identifier for this TE hit on this contig and position
                hit_key = (te_name, contig, start, end)

                # Ensure only unique TEs per position are counted
                if hit_key not in unique_hits:
                    unique_hits.add(hit_key)
                    if te_name not in te_counter:
                        te_counter[te_name] = 0
                    te_counter[te_name] += 1

        # Write the analysis report
        with open(output_report_file, 'w') as report:
            report.write("HMMER Analysis Report\n")
            report.write("======================\n")
            report.write(f"Total unique TEs identified: {len(te_counter)}\n\n")
            report.write("List of unique TEs and their counts:\n")
            report.write("-------------------------------------\n")
            for te_name, count in te_counter.items():
                report.write(f"{te_name}: {count} occurrence(s)\n")

        print(f"Analysis completed. Report saved to {output_report_file}")

    except FileNotFoundError:
        print(f"Error: The file {parsed_results_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
