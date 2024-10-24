import pandas as pd

def analyze_hmmer_results(parsed_results_file, output_report_file):
    """
    Analyzes parsed HMMER results to identify detailed information for transposable elements (TEs)
    and merge overlapping or adjacent regions within 10 base pairs.
    
    Parameters:
    - parsed_results_file (str): Path to the parsed HMMER results file.
    - output_report_file (str): Path to save the detailed analysis report.
    
    Returns:
    - None
    """
    te_details = []
    unique_hits = set()
    unique_proteins = set()  # Set to track unique protein names (query names)

    try:
        # Read the parsed HMMER results file
        with open(parsed_results_file, 'r') as infile:
            last_hit = None
            for line in infile:
                if line.startswith('#'):  # Skip comment lines
                    continue
                
                fields = line.strip().split()
                if len(fields) < 19:
                    continue  # Ensure we have enough fields to parse
                
                te_name = fields[0]    # TE name (first column)
                query_name = fields[3] # Query protein name (fourth column)
                start = int(fields[17]) # Start position (ali coord start, 18th column)
                end = int(fields[18])   # End position (ali coord end, 19th column)
                e_value = fields[6]    # E-value (seventh column)
                score = fields[7]      # Score (eighth column)

                # Merge overlapping or adjacent regions within 10 base pairs
                if last_hit and last_hit["TE Name"] == te_name and last_hit["Query Name"] == query_name:
                    if start <= last_hit["End"] + 10:  # Allow 10 base pair adjacency for merging
                        # Update the end position and possibly the E-value or score
                        last_hit["End"] = max(last_hit["End"], end)
                        last_hit["E-value"] = min(last_hit["E-value"], e_value)
                        last_hit["Score"] = max(last_hit["Score"], score)
                        continue
                
                # Add the last hit to the details list if it exists
                if last_hit:
                    te_details.append(last_hit)
                
                # Create a new hit
                last_hit = {
                    "TE Name": te_name,
                    "Query Name": query_name,
                    "Start": start,
                    "End": end,
                    "E-value": e_value,
                    "Score": score
                }

                # Add query_name to unique_proteins to ensure each protein is counted only once
                unique_proteins.add(query_name)

            # Add the final hit after the loop ends
            if last_hit:
                te_details.append(last_hit)

        # Write the analysis report
        with open(output_report_file, 'w') as report:
            # Report header
            report.write("HMMER Detailed Analysis Report\n")
            report.write("================================\n")
            # Output the count of unique proteins instead of total TE hits
            report.write(f"Total unique TEs identified (unique proteins): {len(unique_proteins)}\n\n")
            
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
