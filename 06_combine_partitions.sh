#!/bin/bash -l

# use 8 threads, more if you have a more beefy computer
CPU=8
conda activate phylogenetics
# will create a partition file and combined multi-fasta alignment then run modeltest to determine per-alignment model test
pushd aligned_renamed
ls *.mfa > matrix.txt
phykit cc -a matrix.txt -p combined_aligned
perl -i -p -e 's/^AUTO/DNA/; s/\.mfa//' combined_aligned.partition
modeltest-ng -i combined_aligned.fa -q combined_aligned.partition -T raxml -p $CPU
# just using this, could use *.aicc or *.bic if you prefer
cp *.aic *.fa ..
popd
