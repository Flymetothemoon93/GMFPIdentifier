# GMFPIdentifier

GMFPIdentifier (Gene Model False Positives Identifier) is a bioinformatics tool designed to identify transposable elements (TEs) that may be misidentified as genes in genome annotations. The tool utilizes HMMER to scan protein sequences against the GyDB database, detecting potential transposon-related domains. InterProScan is then used to validate these results, ensuring that the proteins identified by HMMER as TEs are indeed transposon-related, thereby reducing false positives. The tool ultimately generates a detailed report summarizing the identified transposon-related proteins, along with a TSV file containing their functional annotations.

---

## How to Use

You can easily run GMFPIdentifier using Docker **without manually installing dependencies**.

### 1. Pull the Docker Image

```bash
docker pull flymetothemoon93/gmfpid:v1.3
```

### 2. Run the Container

To run GMFPIdentifier, use the following command:

```bash
docker run \
-v $(pwd)/your_input_folder:/app/input_data \
-v $(pwd)/your_output_folder:/app/output_data \
flymetothemoon93/gmfpid:v1.3 \
--input /app/input_data/your_input.fasta \
--output /app/output_data/results
```

### Explanation:

| Parameter | Description |
|-----------|------------|
| `-v $(pwd)/your_input_folder:/app/input_data` | Mounts your **local input data folder** to the container. |
| `-v $(pwd)/your_output_folder:/app/output_data` | Mounts your **output folder** to retrieve results. |
| `--input /app/input_data/your_input.fasta` | Specifies the **input PROTEIN FASTA** file. |
| `--output /app/output_data/results` | Defines the **directory** where results will be saved. |
| `--threads 4 (optional)` | Number of CPU threads to use. Default is 1 **(fastest)**. |
| `--json /app/database/custom_transposon_interpro.json (optional)` | Use a **custom transposon database JSON file** instead of the default. |

### Example Usage

If you have an input FASTA file called `Athaliana_with_Gypsy.fa` stored in your `testdata` directory, you can run:

```bash
docker run \
-v $(pwd)/testdata:/app/input_data \
-v $(pwd)/testoutput:/app/output_data \
flymetothemoon93/gmfpid:v1.3 \
--input /app/input_data/Athaliana_with_Gypsy.fa \
--output /app/output_data/Athaliana_results
```

After the process completes, results will be stored in `testoutput/Athaliana_results`. 🎯

---

### About `--threads`
You can **optionally specify `--threads`** to set the number of CPU threads.
**Example** (using 4 threads):
```bash
docker run \
-v $(pwd)/testdata:/app/input_data \
-v $(pwd)/testoutput:/app/output_data \
flymetothemoon93/gmfpid:v1.3 \
--input /app/input_data/Athaliana_with_Gypsy.fa \
--output /app/output_data/Athaliana_results \
--threads 4
  ```
⚠️ **Recommendation:**  
  **By default (without `--threads`), the program runs with `--threads 1`, which is the fastest option**.  
  Using multiple threads may not improve performance due to HMMER's I/O and CPU constraints.

---

### Customizing the Transposon Database (`transposon_interpro.json`)
By default, GMFPIdentifier uses **`/app/database/transposon_interpro.json`**, which includes known transposon-related proteins.

If you want to **modify or extend the database**, you can provide your own JSON file.

**How to Use a Custom JSON File in Docker**:
```bash
docker run \
-v $(pwd)/your_input_folder:/app/input_data \
-v $(pwd)/your_output_folder:/app/output_data \
-v $(pwd)/your_custom_json:/app/database \
flymetothemoon93/gmfpid:v1.3 \
--input /app/input_data/your_input.fasta \
--output /app/output_data/results \
--json /app/database/custom_transposon_interpro.json
```

This will **replace the default JSON** with your **custom** transposon detection database.

---

## Features
- Identify transposable element proteins from protein sequences using HMMER and GyDB profiles.
- Filter and extract high-confidence TE protein sequences.
- Validate HMMER results with InterProScan to eliminate false positives.
- Generate a detailed report and a TSV file summarizing identified transposon-related proteins.

---

## Prerequisites (For Manual Installation)
If you prefer to run GMFPIdentifier **without Docker**, you'll need:

- Python (3.6 or later, with required packages in `requirements.txt`)
- HMMER (must be installed and accessible in your system path)
- InterProScan (installation instructions below) for verification of TE proteins.

---

## Installation (Manual)

### 1. Clone the Repository

```bash
git clone https://github.com/Flymetothemoon93/GMFPIdentifier.git
cd GMFPIdentifier
```

### 2. Install Required Python Packages

```bash
pip install -r requirements.txt
```

### 3. Install HMMER

Download the latest HMMER version:

```bash
wget http://eddylab.org/software/hmmer/hmmer.tar.gz
```

Extract and compile:

```bash
tar -xvzf hmmer.tar.gz
cd hmmer-<version>
./configure
make
sudo make install
```

Add HMMER to your PATH:

```bash
export PATH=$(pwd)/src:$PATH
```

For permanent addition, include this line in `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export PATH=$(pwd)/src:$PATH' >> ~/.bashrc
source ~/.bashrc
```

Verify installation:

```bash
hmmscan -h
```

### 4. Download and Install InterProScan

Download InterProScan from the official site. You can use the following command to download version 5.70-102.0:

```bash
wget https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.70-102.0/interproscan-5.70-102.0-64-bit.tar.gz
```

Alternatively, use `curl`:

```bash
curl -O https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.70-102.0/interproscan-5.70-102.0-64-bit.tar.gz
```

Extract the file:

```bash
tar -zxvf interproscan-5.70-102.0-64-bit.tar.gz
```

Set the **InterProScan Path**:

```bash
export INTERPROSCAN_PATH=/path/to/interproscan-5.70-102.0
```

To make this setting persistent:

```bash
echo "export INTERPROSCAN_PATH=/path/to/interproscan-5.70-102.0" >> ~/.bashrc
source ~/.bashrc
```

---

## How to Use (Manual Execution)

Run GMFPIdentifier with your input files:

```bash
python src/main.py --input your_protein_sequences.fasta --output results
```

### Example Usage

```bash
python src/main.py --input testdata/Athaliana_with_Gypsy.fa --output testoutput/Athaliana_with_Gypsy
```

This command will:
- Run HMMER to identify transposable element-related proteins.
- Filter the HMMER results to retain high-confidence TE protein predictions.
- Extract relevant protein sequences for further analysis.
- Run InterProScan to confirm that the filtered sequences are true transposon-related proteins, removing false positives.
- Generate a detailed report summarizing the analysis, including runtime, detected transposon-related proteins, and their descriptions.
- Output an InterProScan TSV file containing domain annotations for all detected transposable element proteins.

### **Optional Arguments**
| Parameter            | Description |
|----------------------|-------------|
| `--json` *(optional)* | Path to a **custom transposon database JSON file**. If not provided, the default `/database/transposon_interpro.json` will be used. |
| `--threads` *(optional)* | Number of CPU threads to use. **Default: 1 (recommended for fastest execution)**. Multi-threading can be enabled, but due to HMMER & InterProScan constraints, **using the default (without --threads) is the fastest option.** |

---

## Troubleshooting

### InterProScan Not Found
Ensure that the `INTERPROSCAN_PATH` environment variable is correctly set to the full path of your InterProScan installation:

```bash
echo $INTERPROSCAN_PATH
```

### Permissions
If you encounter **permissions issues**, ensure that you have execution permissions for the `interproscan.sh` script.

---

## License
This project is open-source and licensed under the **MIT License**. See the `LICENSE` file for details.
