# GROMACS Running Instructions for NVIDIA RTX 5070 Ti

To run the simulation using your NVIDIA RTX 5070 Ti, use the following command line flags to offload calculations to the GPU.

## The "Antigravity" Command

```bash
gmx mdrun -v -deffnm nvt \
  -nb gpu \
  -pme gpu \
  -bonded gpu \
  -update gpu \
  -ntmpi 1 \
  -ntomp 12
```

### Explanation of Flags
- `-nb gpu`, `-pme gpu`, `-bonded gpu`: Offloads the non-bonded, electrostatics, and bond-force math to your CUDA cores.
- `-update gpu`: Keeps the coordinates on the GPU memory as much as possible, preventing "lag" from sending data back to the CPU.
- `-ntmpi 1 -ntomp 12`: Uses 1 MPI rank and 12 AMD CPU cores to handle coordination (optimized for single GPU).

> **Pro-Tip for the 5070 Ti:**
> If you notice the simulation is "stuttering," it might be because the system is too small for the GPU to stay efficient. In that case, you can remove `-update gpu` to let the CPU handle the position updates while the GPU handles the heavy force math.
