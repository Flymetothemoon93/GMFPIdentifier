import os
import csv
import json

def generate_report(input_file, output_report, output_tsv, transposon_json, runtime_seconds):
    """
    Generate a detailed report and filtered TSV file identifying transposable proteins.
    """
    # Convert runtime from seconds to readable format
    hours = int(runtime_seconds // 3600)
    minutes = int((runtime_seconds % 3600) // 60)
    seconds = int(runtime_seconds % 60)
    formatted_runtime = f"{hours} hours {minutes} minutes {seconds} seconds"

    # Convert transposon_json to absolute path
    transposon_json = os.path.abspath(transposon_json)

    # Load transposon InterPro IDs from JSON
    if not os.path.exists(transposon_json):
        raise FileNotFoundError(f"Error: Transposon JSON file not found at {transposon_json}")

    try:
        with open(transposon_json, 'r') as json_file:
            transposon_interpro_ids = json.load(json_file)
    except Exception as e:
        print(f"Error loading transposon JSON file: {e}", flush=True)
        return

    # Initialize counters and results dictionary
    total_proteins = 0
    protein_dict = {}  # Dictionary to store results per protein
    matched_rows = []  # List to store all matching rows for the TSV output

    # Process the input InterProScan TSV file
    try:
        with open(input_file, 'r') as file:
            reader = csv.reader(file, delimiter='\t')

            for row in reader:
                if len(row) < 12:  # Ensure the row has enough columns
                    continue

                total_proteins += 1
                protein_name = row[0]  # First column: Protein name
                interpro_id = row[11]  # 12th column: InterPro ID

                if interpro_id in transposon_interpro_ids:
                    description = transposon_interpro_ids[interpro_id]

                    if protein_name not in protein_dict:
                        protein_dict[protein_name] = []

                    # Only add if this InterPro ID is not already listed for this protein
                    if (interpro_id, description) not in protein_dict[protein_name]:
                        protein_dict[protein_name].append((interpro_id, description))

                    # Store the full row for TSV output
                    matched_rows.append(row)

    except Exception as e:
        print(f"Error processing input file: {e}", flush=True)
        return

    # Write the detailed report
    try:
        with open(output_report, 'w') as report:
            report.write("GMFPIdentifier Report\n")
            report.write("===================\n")
            report.write("Purpose:\n")
            report.write("GMFPIdentifier detects transposable proteins (False Positives) in the input protein sequences.\n\n")
            report.write(f"Pipeline Runtime: {formatted_runtime}\n\n")
            report.write("Results:\n")

            if protein_dict:
                report.write("The following proteins were identified as transposable proteins:\n\n")
                for i, (protein, domains) in enumerate(protein_dict.items(), 1):
                    report.write(f"{i}. Protein: {protein}\n")
                    for interpro_id, description in domains:
                        report.write(f"   - InterPro ID: {interpro_id}\n")
                        report.write(f"     Description: {description}\n")
                    report.write("\n")

                report.write("Summary:\n")
                report.write(f"A total of {len(protein_dict)} unique transposable proteins were detected.\n")
            else:
                report.write("No transposable proteins were detected in the input data.\n\n")
                report.write("Summary:\n")
                report.write("The analysis did not find any transposable proteins in the provided sequences.\n")
                report.write("This indicates that your annotated proteins are likely accurate.\n")

        print(f"Report generated successfully: {output_report}", flush=True)
    except Exception as e:
        print(f"Error writing report: {e}", flush=True)

    # Write the filtered TSV file
    try:
        with open(output_tsv, 'w', newline='') as tsv_file:
            writer = csv.writer(tsv_file, delimiter='\t')
            writer.writerows(matched_rows) 
        print(f"Filtered TSV file generated successfully: {output_tsv}", flush=True)
    except Exception as e:
        print(f"Error writing TSV file: {e}", flush=True)
