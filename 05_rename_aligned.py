#!/usr/bin/env python3
import argparse
import csv
import os
import re
from Bio import Entrez, SeqIO

def main():
    parser = argparse.ArgumentParser(description='Rename aligned sequences MAFFT')
    parser.add_argument('--input', default='table1_filled.csv', help='Input CSV file')
    parser.add_argument('--outdir', default='aligned_renamed', help='Output directory for renamed_aligned files')
    parser.add_argument('--aln_ext', default='mfa', help='Extension for input and output aligned files')
    parser.add_argument('--aligned', default='sequences', help='Input directory for aligned files')
    args = parser.parse_args()
    
    os.makedirs(args.outdir, exist_ok=True)
    
    sequences = {}
    
    for filename in os.listdir(args.aligned):
        print(f"Processing file: {filename}")
        if filename.endswith(args.aln_ext):
            print(f"Loading alignment for {filename}")
            marker_name = os.path.splitext(filename)[0]
            filepath = os.path.join(args.aligned, filename)
            sequences[marker_name] = {}
            
            for record in SeqIO.parse(filepath, 'fasta'):
                sequences[marker_name][record.id] = record
    
    print(f"Loaded {len(sequences)} marker alignments")
    for marker, seqs in sequences.items():
        print(f"  {marker}: {len(seqs)} sequences")
    update_sequences = {}
    with open(args.input, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            print(f"Row {row_num}: {row.get('Species', 'Unknown')}")
            species = re.sub(r'\s+','_',row.get('Species'))
            strain = re.sub(r'\s+','_',row.get('Culture accession number(s)').split(';')[0])
            strain = re.sub(r'\(TYPE\)','__TYPE',strain)
            print(f'species is {species} strain is {strain}') 
            for seq_type in ["ITS", "TEF", "ACT", "CAL", "HIS"]:
                accession = row.get(seq_type, '').strip()
                if accession:
                    print(f'looking for {accession} for {seq_type} for {species}') 
                    if seq_type in sequences:
                        if accession in sequences[seq_type]:
                            record = sequences[seq_type][accession]
                        elif accession + ".1" in sequences[seq_type]:
                            record = sequences[seq_type][accession + ".1"]
                        else:
                            print(f"Accession {accession} not found in {seq_type} for {species}")
                            continue
        
                        seq_id = record.id
                        new_id = f"{species}_{strain}"
                        print(f"Renaming {seq_id} to {new_id}")
                        record.id = new_id
                        record.description = ''
                        if seq_type not in update_sequences:
                                update_sequences[seq_type] = []
                        update_sequences[seq_type].append(record)
    
    for seq_type, records in update_sequences.items():
        output_file = os.path.join(args.outdir, f"{seq_type}.{args.aln_ext}")
        SeqIO.write(records, output_file, 'fasta')
    print("Done!")

if __name__ == "__main__":
    main()
