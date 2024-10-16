import matplotlib.pyplot as plt
from collections import defaultdict
import os

# Function to parse the bed file and count false positives per contig
def parse_bed_file_with_flexible_prediction(file_path):
    contig_false_positive_count = defaultdict(int)
    
    with open(file_path, 'r') as file:
        for line in file:
            cols = line.split()
            contig = cols[0]
            additional_info = cols[-1] 
            
            prediction_value = None  # Initialize prediction_value
            
            # Search for the "prediction=" field in the annotation info
            for entry in additional_info.split(';'):
                if "prediction=" in entry:
                    prediction_value = int(entry.split('=')[1])  # Extract the prediction value
                    break

            # Count false positives (prediction != 0) if prediction_value was found
            if prediction_value is not None and prediction_value != 0:
                contig_false_positive_count[contig] += 1
    
    return contig_false_positive_count

# Function to plot the bar chart
def plot_false_positives(contig_false_positive_count, output_dir):
    contigs = list(contig_false_positive_count.keys())
    counts = list(contig_false_positive_count.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(contigs, counts, color='skyblue')
    plt.xlabel('Contigs')
    plt.ylabel('Number of False Positives')
    plt.title('False Positives per Contig')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the plot to the output directory
    plot_file = os.path.join(output_dir, "false_positives_bar_chart.png")
    plt.savefig(plot_file)
    plt.close()
    
    print(f"Bar chart saved to: {plot_file}")
