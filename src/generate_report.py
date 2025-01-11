import csv

def generate_report(input_file, output_file):
    # Define transposon protein InterPro IDs and descriptions
    transposon_interpro_ids = {
        "IPR000123": "RNA-directed DNA polymerase (reverse transcriptase), msDNA",
        "IPR000477": "Reverse transcriptase domain",
        "IPR000840": "Gamma-retroviral matrix protein",
        # Add all other IDs and descriptions here
    }

    # Initialize counters and results list
    total_proteins = 0
    matched_proteins = []

    # Process the input file
    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            total_proteins += 1
            protein_name = row[0]  # Protein name in the first column
            interpro_id = row[11]  # InterPro ID in the 12th column
            if interpro_id in transposon_interpro_ids:
                matched_proteins.append({
                    "protein": protein_name,
                    "interpro_id": interpro_id,
                    "description": transposon_interpro_ids[interpro_id]
                })

    # Write the report
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
            report.write("Please review the input file to ensure accuracy or consider using alternative datasets.\n")

    print(f"Report generated successfully: {output_file}")
