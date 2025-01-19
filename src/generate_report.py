import csv
import json

def generate_report(input_file, output_file, transposon_json):
    """
    Generate a report identifying transposable proteins in input sequences.

    Parameters:
        input_file (str): Path to the input TSV file.
        output_file (str): Path to the output report file.
        transposon_json (str): Path to the JSON file containing transposon InterPro IDs and descriptions.
    """

    # Load transposon InterPro IDs from JSON
    try:
        with open(transposon_json, 'r') as json_file:
            transposon_interpro_ids = json.load(json_file)
    except Exception as e:
        print(f"Error loading transposon JSON file: {e}")
        return

    # Initialize counters and results list
    total_proteins = 0
    matched_proteins = []

    # Process the input file
    try:
        with open(input_file, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                total_proteins += 1
                protein_name = row.get('Protein') 
                interpro_id = row.get('InterPro ID') 
                
                if interpro_id in transposon_interpro_ids:
                    matched_proteins.append({
                        "protein": protein_name,
                        "interpro_id": interpro_id,
                        "description": transposon_interpro_ids[interpro_id]
                    })
    except Exception as e:
        print(f"Error processing input file: {e}")
        return

    # Write the report
    try:
        with open(output_file, 'w') as report:
            report.write("FPIdentifier Report\n")
            report.write("===================\n")
            report.write("Purpose:\n")
            report.write("FPIdentifier detects transposable proteins (False Positives) in the input protein sequences.\n\n")
            report.write(f"Input File: {input_file}\n")
            report.write(f"Total Proteins Analyzed: {total_proteins}\n\n")
            report.write("Results:\n")
            
            if matched_proteins:
                report.write("The following proteins were identified as transposable proteins:\n\n")
                for i, protein in enumerate(matched_proteins, 1):
                    report.write(f"{i}. Protein: {protein['protein']}\n")
                    report.write(f"   InterPro ID: {protein['interpro_id']}\n")
                    report.write(f"   Description: {protein['description']}\n\n")
                report.write("Summary:\n")
                report.write(f"A total of {len(matched_proteins)} transposable proteins were detected.\n")
            else:
                report.write("No transposable proteins were detected in the input data.\n\n")
                report.write("Summary:\n")
                report.write("The analysis did not find any transposable proteins in the provided sequences.\n")
                report.write("This indicates that your annotated proteins are likely accurate.\n")
        print(f"Report generated successfully: {output_file}")
    except Exception as e:
        print(f"Error writing report: {e}")
