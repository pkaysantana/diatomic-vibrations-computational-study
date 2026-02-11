#!/bin/bash
cd ~/orca/orca_6_1_0_linux_x86-64_shared_openmpi418_avx2 || exit 1
for f in *_mpi; do
    basename="${f%_mpi}"
    if [ ! -e "$basename" ]; then
        ln -s "$f" "$basename"
        echo "Linked $f -> $basename"
    fi
done

# Second pass: link non-mpi to _mpi if missing
for f in *; do
    if [[ "$f" != *"_mpi"* ]] && [[ -f "$f" ]] && [[ -x "$f" ]]; then
        mpiname="${f}_mpi"
        if [ ! -e "$mpiname" ]; then
            ln -s "$f" "$mpiname"
            echo "Linked $f -> $mpiname"
        fi
    fi
done
