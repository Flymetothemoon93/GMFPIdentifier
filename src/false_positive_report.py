import csv
from collections import defaultdict

# Function to parse the bed file and generate the report with false positives
def generate_false_positive_report(input_file, output_report):
    false_positives = []
    contig_false_positive_count = defaultdict(int)
    
    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        
        for row in reader:
            contig = row[0]
            start = row[1]
            end = row[2]
            query_name = row[3] 
            annotation_info = row[-1] 
            
            prediction_value = None
            for entry in annotation_info.split(';'):
                if "prediction=" in entry:
                    prediction_value = int(entry.split('=')[1]) 
                    break

            if prediction_value is not None and prediction_value != 0:
                contig_false_positive_count[contig] += 1
                false_positives.append((contig, start, end, query_name, prediction_value))
    
    total_false_positives = len(false_positives)
    
    with open(output_report, 'w') as report_file:
        report_file.write("PFIdentifier Report\n")
        report_file.write("===========================\n")
        report_file.write(f"Total False Positives identified: {total_false_positives}\n\n")
        report_file.write("Detailed False Positive List:\n")
        report_file.write("Contig\tStart\tEnd\tQuery Name\tPrediction\n")
        
        for fp in false_positives:
            report_file.write(f"{fp[0]}\t{fp[1]}\t{fp[2]}\t{fp[3]}\t{fp[4]}\n")
    
    print(f"False positive report generated at {output_report}")
