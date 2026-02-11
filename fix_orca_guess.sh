#!/bin/bash
ORCA_DIR=~/orca/orca_6_1_0_linux_x86-64_shared_openmpi418_avx2
cd "$ORCA_DIR" || exit 1

# Remove the symlink we created
if [ -L orca_guess_mpi ]; then
    rm orca_guess_mpi
fi

# Create the wrapper script
cat << 'EOF' > orca_guess_mpi
#!/bin/bash
# Wrapper to run serial orca_guess only on Rank 0 to avoid race conditions
# Check OpenMPI rank variable (OMPI_COMM_WORLD_RANK)
if [ "$OMPI_COMM_WORLD_RANK" = "0" ] || [ -z "$OMPI_COMM_WORLD_RANK" ]; then
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    if [ -f "$DIR/orca_guess" ]; then
        "$DIR/orca_guess" "$@"
    else
        echo "Error: orca_guess not found in $DIR"
        exit 1
    fi
else
    # Non-zero ranks exit successfully to satisfy mpirun
    exit 0
fi
EOF

chmod +x orca_guess_mpi
echo "Replaced orca_guess_mpi with Rank 0 wrapper."
