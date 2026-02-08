
# GROMACS Running Instructions for NVIDIA GPU

To run the simulation using your NVIDIA RTX 5070 Ti, use the following command line flags to offload calculations to the GPU.

```bash
gmx mdrun -v -deffnm nvt -nb gpu -pme gpu -bonded gpu -update gpu
```

- `-nb gpu`: Offload non-bonded interactions to GPU.
- `-pme gpu`: Offload PME electrostatics to GPU.
- `-bonded gpu`: Offload bonded interactions to GPU (requires GROMACS 2023+).
- `-update gpu`: Offload coordinate updates to GPU.
