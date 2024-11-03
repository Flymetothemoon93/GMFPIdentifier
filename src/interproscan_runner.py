import subprocess
import os

def run_interproscan(input_fasta, output_file):
    """
    Runs InterProScan on a given FASTA file and saves the results to an output file.

    Parameters:
    - input_fasta (str): Path to the input FASTA file containing sequences for InterProScan.
    - output_file (str): Path where the InterProScan results should be saved.

    Returns:
    - None: Outputs the results to the specified output file.
    """
    try:
        print("Running InterProScan...")

        # Retrieve InterProScan path from the environment variable
        interproscan_path = os.environ.get("INTERPROSCAN_PATH")
        if not interproscan_path:
            raise EnvironmentError("Please set the INTERPROSCAN_PATH environment variable to the InterProScan installation path.")

        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Construct the InterProScan command
        cmd = [
            os.path.join(interproscan_path, "interproscan.sh"),
            "-i", input_fasta,
            "-o", output_file,
            "-f", "tsv",  # Specify output format; can be changed based on requirements
            "-goterms",   # Include GO terms if relevant for functional annotation
            "-iprlookup", # Include InterPro annotations
            "--cpu", "4"  # Number of CPU cores to use
        ]
        
        # Run InterProScan
        subprocess.run(cmd, check=True)
        
        print(f"InterProScan completed. Results saved to {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"InterProScan failed with error: {e}")
    except FileNotFoundError:
        print(f"Error: The file {input_fasta} or the InterProScan executable was not found.")
    except EnvironmentError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
