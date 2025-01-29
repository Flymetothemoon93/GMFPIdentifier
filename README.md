# FPIdentifier

GMFPIdentifier (Gene Model False Positives Identifier) is a bioinformatics tool designed to identify transposable elements (TEs) that may be misidentified as genes in genomic annotations. The tool utilizes HMMER to scan protein sequences against the GyDB database, detecting potential transposon-related domains. InterProScan is then used to validate these results, ensuring that the proteins identified by HMMER as TEs are indeed transposon-related, thereby reducing false positives. The tool ultimately generates a detailed report summarizing the identified transposon-related proteins, along with a TSV file containing their InterProScan-based functional annotations.

## Features

- Identify transposable element proteins from protein sequences using HMMER and GyDB profiles.
- Filter and extract high-confidence TE protein sequences.
- Validate HMMER results with InterProScan to eliminate false positives.
- Generate a detailed report summarizing identified transposon-related proteins and a TSV file containing their functional annotations.

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
   - Download the latest HMMER version:
     ```bash
     wget http://eddylab.org/software/hmmer/hmmer.tar.gz
     ```
   - Extract and compile:
     ```bash
     tar -xvzf hmmer.tar.gz
     cd hmmer-<version>
     ./configure
     make
     sudo make install
     ```
   - Add HMMER to your PATH:
     ```bash
     export PATH=$(pwd)/src:$PATH
     ```
   - For permanent addition, include this line in ~/.bashrc or ~/.zshrc.
      ```bash
     echo 'export PATH=$(pwd)/src:$PATH' >> ~/.bashrc
     source ~/.bashrc
     ```

   - Verify installation:
     ```bash
     hmmscan -h
     ```

4. **Download and Install InterProScan**
   - Download InterProScan from the official site. You can use the following command to download version 5.70-102.0:
     ```bash
     wget https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.70-102.0/interproscan-5.70-102.0-64-bit.tar.gz
     ```
   - Alternatively, use `curl`:
     ```bash
     curl -O https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.70-102.0/interproscan-5.70-102.0-64-bit.tar.gz
     ```
   - After downloading, extract the file in your chosen directory:
     ```bash
     tar -zxvf interproscan-5.70-102.0-64-bit.tar.gz
     ```

5. **Set the InterProScan Path**
   - Set the `INTERPROSCAN_PATH` environment variable to point to your InterProScan installation path. Replace `/path/to` with the directory where you extracted InterProScan:
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
python src/main.py --input testdata/Athaliana_with_Gypsy.fa --output testoutput/Athaliana_with_Gypsy
```

This command will:
1. Run HMMER to identify transposable element-related proteins.
2. Filter the HMMER results to retain high-confidence TE protein predictions.
3. Extract relevant protein sequences for further analysis.
4. Run InterProScan to confirm that the filtered sequences are true transposon-related proteins, removing false positives.
5. Generate a detailed report summarizing the analysis, including the runtime, detected transposon-related proteins, and their descriptions.

## Troubleshooting

- **InterProScan Not Found**: Ensure that the `INTERPROSCAN_PATH` environment variable is correctly set to the full path of your InterProScan installation. You can check if the variable is set by running:
  ```bash
  echo $INTERPROSCAN_PATH
  ```

- **Permissions**: If you encounter permissions issues, ensure that you have execution permissions for the `interproscan.sh` script.

## License

This project is open-source and licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
