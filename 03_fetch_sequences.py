#!/usr/bin/env python3
import argparse
import csv
import os
import json
from Bio import Entrez

Entrez.email = "research@example.com"

CACHE_FILE = "sequence_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def fetch_sequence(accession, cache):
    if accession in cache:
        print(f"  Cache hit: {accession}")
        return cache[accession]
    
    print(f"  Fetching: {accession}")
    try:
        handle = Entrez.efetch(db="nucleotide", id=accession, rettype="fasta", retmode="text")
        seq = handle.read()
        handle.close()
        cache[accession] = seq
        return seq
    except Exception as e:
        print(f"  Error fetching {accession}: {e}")
        cache[accession] = None
        return None

def main():
    parser = argparse.ArgumentParser(description='Fetch sequences from NCBI Entrez')
    parser.add_argument('--input', default='table1_filled.csv', help='Input CSV file')
    parser.add_argument('--outdir', default='sequences', help='Output directory for fasta files')
    parser.add_argument('--cache_checkpoint', default=10, type=int, help='How frequent to checkpoint cache')
    args = parser.parse_args()
    
    os.makedirs(args.outdir, exist_ok=True)
    
    cache = load_cache()
    sequences = {"ITS": [], "TEF": [], "ACT": [], "CAL": [], "HIS": []}
    
    with open(args.input, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            print(f"Row {row_num}: {row.get('Species', 'Unknown')}")
            for seq_type in ["ITS", "TEF", "ACT", "CAL", "HIS"]:
                accession = row.get(seq_type, '').strip()
                if accession:
                    seq = fetch_sequence(accession, cache)
                    if seq:
                        sequences[seq_type].append(seq)
            
            if row_num % args.cache_checkpoint == 0:
                save_cache(cache)
                print(f"  Checkpoint saved at row {row_num}")
    
    save_cache(cache)
    print("\nWriting sequence files...")
    
    for seq_type, seqs in sequences.items():
        if seqs:
            filename = os.path.join(args.outdir, f"{seq_type}.fasta")
            with open(filename, 'w') as f:
                f.write(''.join(seqs))
            print(f"  Wrote {len(seqs)} sequences to {filename}")
    
    print("Done!")

if __name__ == "__main__":
    main()
