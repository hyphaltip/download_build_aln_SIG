# Linked Marker Table Analysis

Scripts to parse NCBI PMC Table from Studies in Mycology paper, fetch sequences, and perform phylogenetic analysis.
Using https://pmc.ncbi.nlm.nih.gov/articles/PMC3713887/table/T1/ - but theoretically may work for any SIG paper with table format
but it has hard coded the column names which have the Strain Info and the columns which have the markers so you will need to adjust code
to accomodate that.

## Overview

This project parses [Table 1](Using https://pmc.ncbi.nlm.nih.gov/articles/PMC3713887/table/T1/) from a PMC article about Cercospora species, fetches corresponding sequences from NCBI, and prepares alignments for phylogenetic analysis.

This was initially generated with opencode AI Open Code Zen and then manually adjusted.

Use Conda to install the dependency tools for alignment, concatenation, and phylogenetics.

You could further trim the alignments with clipkit before doing concatenation if you want to tighten up the alignments ahead of the runs.
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

### 5. Rename Sequences in Alignments

```bash
python3 05_rename_aligned.py
```

Renames sequences in aligned FASTA files using species and strain names from the CSV table. Creates standardized sequence IDs in format `Species_Strain`.

Options:
- `--input FILE` - Input CSV file (default: `table1_filled.csv`)
- `--outdir DIR` - Output directory (default: `aligned_renamed`)
- `--aligned DIR` - Input directory for aligned files (default: `sequences`)

### 6. Combine Partitions and Find Best Models

```bash
./06_combine_partitions.sh
```

Uses phykit to concatenate multiple marker alignments into a single combined alignment (`combined_aligned.fa`). Creates a partition file specifying each gene region. Runs modeltest-ng to determine the best substitution model for each partition.

### 7. Run RAxML-NG Phylogenetic Analysis

```bash
./07_raxml.sh
```

Runs raxml-ng for maximum likelihood phylogenetic analysis on the combined alignment using the best-fit models from modeltest-ng.

### 8. Run IQ-TREE Phylogenetic Analysis

```bash
./08_iqtree.sh
```

Runs IQ-TREE for maximum likelihood phylogenetic analysis with ultrafast bootstrap (1000 replicates) on the combined alignment.

## Output Files

- `table1.csv` - Raw table from PMC
- `table1_filled.csv` - Table with filled species values
- `sequence_cache.json` - Cached sequence lookups
- `sequences/` - Directory containing:
  - `{ITS,TEF,ACT,CAL,HIS}.fasta` - Raw sequences
  - `{ITS,TEF,ACT,CAL,HIS}.mfa` - Aligned sequences
- `aligned_renamed/` - Renamed alignment files:
  - `{ITS,TEF,ACT,CAL,HIS}.mfa` - Renamed alignments
- `combined_aligned.fa` - Combined multi-locus alignment
- `combined_aligned.fa.part.aic` - Partition file with best-fit models (AIC)
- `combined_aligned.fa.part.aic.treefile` - RAxML-NG maximum likelihood tree
- `combined_aligned.fa.tree` - IQ-TREE maximum likelihood tree with bootstrap support
