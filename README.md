# Linked Marker Table Analysis

Scripts to parse NCBI PMC Table 1, fetch sequences, and perform phylogenetic analysis.

## Overview

This project parses Table 1 from a PMC article about Cercospora species, fetches corresponding sequences from NCBI, and prepares alignments for phylogenetic analysis.

## Setup

Create the conda environment:

```bash
conda env create -f environment.yml
conda activate phylogenetics
```

Or install dependencies directly:

```bash
conda create -n phylogenetics mafft phykit modeltest-ng raxml-ng iqtree biopython beautifulsoup4 lxml -c conda-forge -c bioconda -y
```

## Running the Pipeline

Run the scripts in numeric order (01, 02, 03, ...):

### 1. Parse Table from PMC

```bash
python3 01_parse_table.py
```

Downloads Table 1 from PMC and saves as `table1.csv` (361 rows, 11 columns).

### 2. Fill Empty Species Values

```bash
python3 02_fill_species.py
```

Parses `table1.csv` and fills empty Species values from previous row. Output: `table1_filled.csv`.

### 3. Fetch Sequences from NCBI

```bash
python3 03_fetch_sequences.py
```

Parses `table1_filled.csv`, fetches sequences from NCBI Entrez for ITS, TEF, ACT, CAL, HIS accessions. Caches lookups to `sequence_cache.json` for restarts.

Options:
- `--input FILE` - Input CSV file (default: `table1_filled.csv`)
- `--outdir DIR` - Output directory (default: `sequences`)
- `--checkpoint N` - Save cache every N rows (default: 10)

### 4. Align Sequences with MAFFT

```bash
./run_mafft.sh
```

Runs mafft on each `.fasta` file in `sequences/` and outputs `.mfa` alignment files.

## Output Files

- `table1.csv` - Raw table from PMC
- `table1_filled.csv` - Table with filled species values
- `sequence_cache.json` - Cached sequence lookups
- `sequences/` - Directory containing:
  - `{ITS,TEF,ACT,CAL,HIS}.fasta` - Raw sequences
  - `{ITS,TEF,ACT,CAL,HIS}.mfa` - Aligned sequences
