import os

def check_file_exists(file_path):
    """
    Checks if a file exists and returns its status and size.
    
    Parameters:
    - file_path (str): Path to the file to check.
    
    Returns:
    - dict: A dictionary with 'exists' (True/False) and 'size' (in bytes).
    """
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        return {'exists': True, 'size': size}
    else:
        return {'exists': False, 'size': 0}


def count_lines_in_file(file_path):
    """
    Counts the number of lines in a file.
    
    Parameters:
    - file_path (str): Path to the file.
    
    Returns:
    - int: The number of lines in the file, or 0 if the file does not exist.
    """
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r') as file:
        return sum(1 for line in file)


def validate_output_files(output_dir):
    """
    Validates the presence and integrity of output files.
    
    Parameters:
    - output_dir (str): The directory containing output files.
    
    Returns:
    - dict: A summary dictionary of file statuses and statistics.
    """
    summary = {}

    # Define the expected files
    files_to_check = [
        "hmmer_results.txt",
        "parsed_hmmer_results.txt",
        "hmmer_results.bed",
        "te_gene_overlaps.bed"
    ]
    
    # Check each file's existence and size
    for file_name in files_to_check:
        file_path = os.path.join(output_dir, file_name)
        file_status = check_file_exists(file_path)
        line_count = count_lines_in_file(file_path)
        
        summary[file_name] = {
            'exists': file_status['exists'],
            'size': file_status['size'],
            'line_count': line_count
        }

    return summary


def generate_report_and_statistics(output_dir, report_file, statistics_file):
    """
    Generates a report and a statistics file based on the output files' validation.
    
    Parameters:
    - output_dir (str): The directory containing the output files.
    - report_file (str): Path to save the report as xxxx.report.txt.
    - statistics_file (str): Path to save the statistics as xxxx.statistics.txt.
    
    Returns:
    - None
    """
    summary = validate_output_files(output_dir)
    
    # Generate report
    with open(report_file, 'w') as report:
        report.write("FPIdentifier Report\n")
        report.write("=" * 40 + "\n\n")

        for file_name, stats in summary.items():
            report.write(f"File: {file_name}\n")
            if stats['exists']:
                report.write(f"  Status: Exists\n")
                report.write(f"  Size: {stats['size']} bytes\n")
                report.write(f"  Line Count: {stats['line_count']} lines\n")
            else:
                report.write(f"  Status: Missing\n")
            report.write("\n")
    
    print(f"Report generated: {report_file}")
    
    # Generate statistics file
    with open(statistics_file, 'w') as stats_file:
        stats_file.write("FPIdentifier Output Files Statistics\n")
        stats_file.write("=" * 40 + "\n\n")
        
        for file_name, stats in summary.items():
            if stats['exists']:
                stats_file.write(f"{file_name}:\n")
                stats_file.write(f"  Size: {stats['size']} bytes\n")
                stats_file.write(f"  Line Count: {stats['line_count']} lines\n\n")
    
    print(f"Statistics file generated: {statistics_file}")
