# FPIdentifier
This project focuses on identifying transposable elements (TEs) that are misidentified as genes in genomic annotations. The tool uses **HMMER** to compare protein sequences against the **GyDB** database and detects potential transposon-related domains.

## Features
- Identify TE proteins from protein sequences using HMMER with GyDB profiles.
- Compare identified TE proteins with gene annotations using Bedtools.
- Generate validation reports and detailed statistics on output files.

## How to Use
1. Clone the repository:
git clone https://github.com/Flymetothemoon93/FPIdentifier.git


2. Install required Python packages:
pip install -r requirements.txt


3. Install HMMER and Bedtools: Make sure hmmer and bedtools are installed and available in your system path.

4. Run the tool with your input files:
python src/main.py --input your_protein_sequences.fasta --annotation final_annotation.gff --output results
