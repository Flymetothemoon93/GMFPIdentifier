import pandas as pd

def analyze_hmmer_results(parsed_results_file, output_report_file):
    """
    Analyzes parsed HMMER results to identify detailed information for transposable elements (TEs).
    
    Parameters:
    - parsed_results_file (str): Path to the parsed HMMER results file.
    - output_report_file (str): Path to save the detailed analysis report.
    
    Returns:
    - None
    """
    te_details = []
    unique_hits = set()
    
    try:
        # Read the parsed HMMER results file
        with open(parsed_results_file, 'r') as infile:
            for line in infile:
                if line.startswith('#'):  # Skip comment lines
                    continue
                
                fields = line.strip().split()
                if len(fields) < 19:
                    continue  # Ensure we have enough fields to parse
                
                te_name = fields[0]    # TE name (first column)
                query_name = fields[3] # Query protein name (fourth column)
                start = fields[17]     # Start position (ali coord start, 18th column)
                end = fields[18]       # End position (ali coord end, 19th column)
                e_value = fields[6]    # E-value (seventh column)
                score = fields[7]      # Score (eighth column)

                # Generate a unique identifier for this TE hit
                hit_key = (te_name, query_name, start, end)

                # Ensure only unique TEs per position are counted
                if hit_key not in unique_hits:
                    unique_hits.add(hit_key)
                    te_details.append({
                        "TE Name": te_name,
                        "Query Name": query_name,
                        "Start": start,
                        "End": end,
                        "E-value": e_value,
                        "Score": score
                    })

        # Write the analysis report
        with open(output_report_file, 'w') as report:
            # Report header
            report.write("HMMER Detailed Analysis Report\n")
            report.write("================================\n")
            report.write(f"Total unique TEs identified: {len(te_details)}\n\n")
            
            # Detailed list of TEs
            report.write("List of unique TEs with detailed information:\n")
            report.write("------------------------------------------------\n")
            report.write("TE Name\tQuery Name\tStart\tEnd\tE-value\tScore\n")
            
            for te in te_details:
                report.write(f"{te['TE Name']}\t{te['Query Name']}\t{te['Start']}\t"
                             f"{te['End']}\t{te['E-value']}\t{te['Score']}\n")

        print(f"Analysis completed. Report saved to {output_report_file}")

    except FileNotFoundError:
        print(f"Error: The file {parsed_results_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
