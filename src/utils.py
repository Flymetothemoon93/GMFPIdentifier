import os

def check_file_exists(file_path):
    """
    Checks if a file exists at the given path.
    
    Parameters:
    - file_path (str): Path to the file to check.
    
    Returns:
    - bool: True if the file exists, False otherwise.
    
    Raises:
    - FileNotFoundError: If the file is not found.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    return True


def create_output_directory(directory_path):
    """
    Creates the output directory if it doesn't exist.
    
    Parameters:
    - directory_path (str): Path to the output directory.
    
    Returns:
    - None
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Output directory created: {directory_path}")
    else:
        print(f"Output directory already exists: {directory_path}")


def print_status(message):
    """
    Prints a status message to the console with formatting.
    
    Parameters:
    - message (str): The status message to print.
    
    Returns:
    - None
    """
    print(f"==== {message} ====")


def validate_fasta_format(file_path):
    """
    Validates whether a given file is in FASTA format by checking its extension.
    
    Parameters:
    - file_path (str): Path to the file to validate.
    
    Returns:
    - bool: True if the file is a FASTA file, False otherwise.
    """
    if not file_path.endswith(".fasta") and not file_path.endswith(".fa"):
        raise ValueError(f"Invalid file format: {file_path}. Expected a FASTA file.")
    return True
