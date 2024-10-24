import matplotlib.pyplot as plt
import os
from collections import defaultdict

# Function to count false positives per contig from the merged regions
def count_false_positives_from_merged_regions(merged_regions):
    contig_false_positive_count = defaultdict(int)
    
    # Count the number of false positives per contig
    for contig, start, end, query_name, pred_value in merged_regions:
        contig_false_positive_count[contig] += 1  # Increment for each false positive region
    
    return contig_false_positive_count

# Function to plot the bar chart
def plot_false_positives(contig_false_positive_count, output_dir):
    contigs = list(contig_false_positive_count.keys())
    counts = list(contig_false_positive_count.values())
    total_false_positives = sum(counts)  # Calculate total false positives
    
    plt.figure(figsize=(12, 7))
    bars = plt.bar(contigs, counts, color='skyblue')

    # Add labels and title
    plt.xlabel('Contigs')
    plt.ylabel('Number of False Positives')
    plt.title(f'False Positives per Contig (Total False Positives: {total_false_positives})')

    # Rotate x-ticks labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Add numbers on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

    plt.tight_layout()

    # Save the plot to the output directory
    plot_file = os.path.join(output_dir, "false_positives_bar_chart.png")
    plt.savefig(plot_file)
    plt.close()
    
    print(f"Bar chart saved to: {plot_file}")
