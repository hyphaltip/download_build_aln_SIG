# Agent Instructions

## Task: Parse NCBI PMC Table to CSV

### Overview
Parse Table 1 from https://pmc.ncbi.nlm.nih.gov/articles/PMC3713887/table/T1/ and convert it to a CSV file.

### Table Description
- Table 1 contains "Collection details and GenBank accession numbers of isolates included in this study"
- Contains fungal species (Cercospora) with culture accession numbers, host information, and GenBank accessions
- Header spans 2 rows (first row has column groups, second row has individual column names)

### Output
- `table1.csv` with 361 data rows and 11 columns:
  - Species, Culture accession number(s), Host name or isolation source, Host Family, Country, Collector, ITS, TEF, ACT, CAL, HIS

### Notes
- Rows with empty Species values are continuations from the previous species (matching original table format)
- Some species have multiple isolates (multiple rows with same species name)

### Code Location
- Parser script: `parse_table.py`
- Output CSV: `table1.csv`

### How to Run
```bash
python3 parse_table.py
```

### Dependencies
- beautifulsoup4
- lxml

## Task: Fill Empty Species Values in CSV

### Overview
Parse `table1.csv` and fill empty Species values with the species from the previous row.

### Code Location
- Script: `fill_species.py`
- Input: `table1.csv`
- Output: `table1_filled.csv`

### How to Run
```bash
python3 fill_species.py
```

## Task: Fetch Sequences from NCBI

### Overview
Parse `table1_filled.csv`, fetch sequences from NCBI using Biopython Entrez for each accession in ITS, TEF, ACT, CAL, HIS columns. Cache lookups to allow restarts.

### Code Location
- Script: `fetch_sequences.py`
- Input: `table1_filled.csv`
- Output: `{ITS,TEF,ACT,CAL,HIS}.fasta` files
- Cache: `sequence_cache.json`

### How to Run
```bash
python3 fetch_sequences.py
```

### Dependencies
- biopython

## Task: Align Sequences with MAFFT

### Overview
Run mafft on each fasta file in the sequences folder.

### Code Location
- Script: `run_mafft.sh`
- Input: `sequences/*.fasta`
- Output: `sequences/*.mfa`

### How to Run
```bash
./run_mafft.sh
```

## Setup Environment

### Using environment
```bash
conda env create -f environment.yml
conda activate phylogenetics
```

### Or install dependencies directly
```bash
conda create -n phylogenetics mafft phykit modeltest-ng raxml-ng iqtree biopython beautifulsoup4 lxml -c conda-forge -c bioconda -y
```
