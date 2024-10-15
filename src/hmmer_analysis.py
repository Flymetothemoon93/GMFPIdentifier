import pandas as pd
from collections import defaultdict

def load_parsed_hmmer_results(parsed_file):
    """
    Loads the parsed HMMER results into a structured dictionary for analysis.

    Parameters:
    - parsed_file (str): Path to the parsed HMMER results file.

    Returns:
    - dict: A dictionary where keys are query names and values are lists of dicts with target, E-value, score, etc.
    """
    results = defaultdict(list)

    with open(parsed_file, 'r') as infile:
        for line in infile:
            fields = line.strip().split()
            if len(fields) < 8:
                continue
            
            # Extract relevant fields from the parsed HMMER results
            query_name = fields[3]  # Query name
            target_name = fields[0]  # Target name
            e_value = float(fields[6])  # E-value
            score = float(fields[7])  # Score
            
            # Store each entry as a dictionary in the results structure
            results[query_name].append({
                'target_name': target_name,
                'e_value': e_value,
                'score': score
            })
    
    return results

def analyze_hmmer_results(results, e_value_threshold=1e-5, score_threshold=50):
    """
    Analyzes HMMER results to identify False Positives and summary statistics.

    Parameters:
    - results (dict): Dictionary of parsed HMMER results loaded from load_parsed_hmmer_results.
    - e_value_threshold (float): Threshold for filtering E-values. Default is 1e-5.
    - score_threshold (float): Threshold for filtering scores. Default is 50.

    Returns:
    - dict: A summary dictionary containing the analysis results, including counts and potential False Positives.
    """
    summary = {
        'total_queries': 0,
        'total_hits': 0,
        'high_score_hits': 0,
        'potential_false_positives': []
    }

    for query, hits in results.items():
        summary['total_queries'] += 1
        
        for hit in hits:
            summary['total_hits'] += 1
            
            # Check if the hit passes the score threshold but fails the E-value threshold (potential false positive)
            if hit['score'] >= score_threshold and hit['e_value'] > e_value_threshold:
                summary['potential_false_positives'].append({
                    'query_name': query,
                    'target_name': hit['target_name'],
                    'e_value': hit['e_value'],
                    'score': hit['score']
                })

            # Check for high-score hits
            if hit['score'] >= score_threshold:
                summary['high_score_hits'] += 1
    
    return summary

def generate_report(summary, output_report):
    """
    Generates a text report summarizing the analysis of HMMER results.

    Parameters:
    - summary (dict): Summary dictionary containing analysis results.
    - output_report (str): Path to the output report file.

    Returns:
    - None: Saves the report to the specified file.
    """
    with open(output_report, 'w') as report:
        report.write("HMMER Analysis Report\n")
        report.write("======================\n")
        report.write(f"Total Queries Analyzed: {summary['total_queries']}\n")
        report.write(f"Total Hits Analyzed: {summary['total_hits']}\n")
        report.write(f"High Score Hits (score >= 50): {summary['high_score_hits']}\n")
        report.write(f"Potential False Positives: {len(summary['potential_false_positives'])}\n\n")
        
        report.write("List of Potential False Positives:\n")
        report.write("Query Name\tTarget Name\tE-value\tScore\n")
        for fp in summary['potential_false_positives']:
            report.write(f"{fp['query_name']}\t{fp['target_name']}\t{fp['e_value']}\t{fp['score']}\n")

    print(f"Report saved to {output_report}")

def main(parsed_hmmer_file, report_file):
    """
    Main function to load parsed HMMER results, analyze them, and generate a report.

    Parameters:
    - parsed_hmmer_file (str): Path to the parsed HMMER results file.
    - report_file (str): Path to the output report file.

    Returns:
    - None: Saves the analysis results and report to the specified file.
    """
    print("Loading parsed HMMER results...")
    results = load_parsed_hmmer_results(parsed_hmmer_file)
    
    print("Analyzing HMMER results...")
    summary = analyze_hmmer_results(results)

    print("Generating report...")
    generate_report(summary, report_file)

    print("Analysis completed.")

