# FPIdentifier

FPIdentifier is a bioinformatics tool designed to identify transposable elements (TEs) that may be misidentified as genes in genomic annotations. The tool utilizes HMMER to scan protein sequences against the GyDB database, detecting potential transposon-related domains. InterProScan is then used to validate these results, ensuring that the proteins identified by HMMER as TEs are indeed transposon-related, thus reducing false positives.

## Features

- Identify transposable element proteins from protein sequences using HMMER and GyDB profiles.
- Filter and extract high-confidence TE protein sequences.
- Validate HMMER results with InterProScan to eliminate false positives.

## Prerequisites

- **Python** (3.6 or later, with required packages in `requirements.txt`)
- **HMMER** (must be installed and accessible in your system path)
- **InterProScan** (installation instructions below) for verification of TE proteins.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Flymetothemoon93/FPIdentifier.git
   cd FPIdentifier
   ```

2. **Install Required Python Packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install HMMER**
   - Ensure that `hmmer` is installed and available in your system path.
   - On Ubuntu, you can install it using:
     ```bash
     sudo apt-get install hmmer
     ```
   - For other systems, refer to the [HMMER installation guide](http://hmmer.org/download.html).

4. **Download and Install InterProScan**
   - To validate HMMER’s results, download InterProScan from [InterProScan’s official website](https://www.ebi.ac.uk/interpro/interproscan.html).
   - Installation:
     1. Go to the [InterProScan download page](https://www.ebi.ac.uk/interpro/interproscan.html).
     2. Choose the appropriate version for your system (e.g., `Linux x64` for most servers).
     3. Download and extract the package in a directory of your choice:
        ```bash
        tar -zxvf interproscan-5.70-102.0-64-bit.tar.gz
        ```
     4. Move the extracted folder to your software directory (e.g., `~/99_software`).

5. **Set the InterProScan Path**
   - Set the `INTERPROSCAN_PATH` environment variable to point to your InterProScan installation path:
     ```bash
     export INTERPROSCAN_PATH=/path/to/interproscan-5.70-102.0
     ```
   - To make this setting persistent, add the line to your `~/.bashrc` or `~/.zshrc` file:
     ```bash
     echo "export INTERPROSCAN_PATH=/path/to/interproscan-5.70-102.0" >> ~/.bashrc
     source ~/.bashrc
     ```

## How to Use

Run FPIdentifier with your input files:

```bash
python src/main.py --input your_protein_sequences.fasta --output results
```

### Example Usage

```bash
python src/main.py --input test.athaliana.protein.fa --output test_output
```

This command will:
1. Run HMMER to identify transposable element-related proteins.
2. Filter the HMMER results to retain high-confidence TE protein predictions.
3. Extract relevant protein sequences for further analysis.
4. Run InterProScan to confirm that the filtered sequences are true transposon-related proteins, removing false positives.

## Troubleshooting

- **InterProScan Not Found**: Ensure that the `INTERPROSCAN_PATH` environment variable is correctly set to the full path of your InterProScan installation. You can check if the variable is set by running:
  ```bash
  echo $INTERPROSCAN_PATH
  ```

- **Permissions**: If you encounter permissions issues, ensure that you have execution permissions for the `interproscan.sh` script.

- **Execution Format Error**: If you encounter format errors, make sure you are running the script on the appropriate operating system and have all necessary dependencies installed.

## License

This project is open-source and licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
