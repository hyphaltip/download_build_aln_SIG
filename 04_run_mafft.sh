#!/bin/bash

for file in sequences/*.fasta; do
    if [ -f "$file" ]; then
        basename=$(basename "$file" .fasta)
        echo "Running mafft on $file -> sequences/${basename}.mfa"
        mafft "$file" > "sequences/${basename}.mfa"
    fi
done

echo "Done!"
