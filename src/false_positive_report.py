import csv
from collections import defaultdict

# Function to parse the bed file and generate the report with false positives
def generate_false_positive_report(input_file, output_report):
    false_positives = []
    contig_false_positive_count = defaultdict(int)
    
    # This dictionary will store contig and their associated start, end, and query info
    contig_regions = defaultdict(list)
    
    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        
        for row in reader:
            contig = row[0]
            start = int(row[1])
            end = int(row[2])
            query_name = row[3] 
            annotation_info = row[-1] 
            
            prediction_value = None
            for entry in annotation_info.split(';'):
                if "prediction=" in entry:
                    prediction_value = int(entry.split('=')[1]) 
                    break

            if prediction_value is not None and prediction_value != 0:
                # Instead of directly appending, store by contig for later processing
                contig_regions[contig].append((start, end, query_name, prediction_value))
    
    # Process contig regions to merge overlapping/adjacent regions
    for contig, regions in contig_regions.items():
        # Sort by start position to process the regions in order
        regions.sort(key=lambda x: x[0])
        
        merged_regions = []
        current_start, current_end, current_query, current_pred = regions[0]
        
        for start, end, query_name, pred_value in regions[1:]:
            if start <= current_end + 10:  # If regions are adjacent or overlap (gap of 10 or less)
                current_end = max(current_end, end)  # Merge the region
            else:
                # Add the previous region to the merged list
                merged_regions.append((current_start, current_end, current_query, current_pred))
                # Start a new region
                current_start, current_end, current_query, current_pred = start, end, query_name, pred_value
        
        # Don't forget to add the last region
        merged_regions.append((current_start, current_end, current_query, current_pred))
        
        # Add merged regions to the false positives list
        false_positives.extend([(contig, start, end, query_name, pred_value) for start, end, query_name, pred_value in merged_regions])
    
    total_false_positives = len(false_positives)
    
    # Write the report
    with open(output_report, 'w') as report_file:
        report_file.write("PFIdentifier Report\n")
        report_file.write("===========================\n")
        report_file.write(f"Total False Positives identified: {total_false_positives}\n\n")
        report_file.write("Detailed False Positive List:\n")
        report_file.write("Contig\tStart\tEnd\tQuery Name\tPrediction\n")
        
        for fp in false_positives:
            report_file.write(f"{fp[0]}\t{fp[1]}\t{fp[2]}\t{fp[3]}\t{fp[4]}\n")
    
    print(f"False positive report generated at {output_report}")

