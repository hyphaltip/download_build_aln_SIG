#!/bin/bash -l
conda activate phylogenetics

iqtree3 -s combined_aligned.fa -p combined_aligned.fa.part.aic -nt AUTO -B 1000
