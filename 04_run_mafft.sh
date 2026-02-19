#!/bin/bash

# could replace mafft with muscle for probably better alignment
for file in sequences/*.fasta; do
    if [ -f "$file" ]; then
        basename=$(basename "$file" .fasta)
        echo "Running mafft on $file -> sequences/${basename}.mfa"
        mafft "$file" > "sequences/${basename}.mfa"
    fi
done

echo "Done!"
