#!/bin/bash -l
conda activate phylogenetics

raxml-ng --all --msa combined_aligned.fa --model combined_aligned.fa.part.aic --threads 5
