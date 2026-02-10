# Setting up WSL (Windows Subsystem for Linux)

To run the `run_antigravity.sh` script and execute computational chemistry workflows on Windows, you need the Windows Subsystem for Linux (WSL).

## Installation

1. **Open PowerShell as Administrator**
    * Right-click the **Start** button.
    * Select **Windows PowerShell (Admin)** or **Terminal (Admin)**.

2. **Run the Install Command**
    Type the following command and press Enter:

    ```powershell
    wsl --install
    ```

    This command will enable the necessary features and download the latest Ubuntu distribution.

3. **Restart Your Computer**
    * You will see a prompt to restart your machine. **Please restart now.**

4. **Finish Configuration**
    * After rebooting, a terminal window will open automatically.
    * It will ask you to create a **username** and **password** for your new Linux environment.
    * *Note: These credentials are specific to Linux and do not need to match your Windows login.*

## Troubleshooting: "WSL2 is not supported..."

If you see an error about virtualization being disabled, you need to enable two things:

1. **BIOS Setting**: Restart your computer and enter BIOS (usually F2 or Del). Look for **"Virtualization Technology"** (Intel VT-x) or **"SVM Mode"** (AMD) and **Enable** it.
2. **Windows Feature**: Search for "Turn Windows features on or off", check **"Virtual Machine Platform"**, and click OK.

## GPU Configuration for GROMACS

To ensure your RTX 5070 Ti is fully utilized:

1. **Switch to Discrete GPU Mode**: Open **Lenovo Vantage** (or your BIOS) and switch the GPU Working Mode to **dGPU Mode** (sometimes called "Discrete Graphics"). This disables the integrated graphics and gives the RTX 5070 Ti full control, which is highly recommended for compute tasks to avoid latency or driver conflicts.
2. **Driver**: Ensure you have the latest **NVIDIA Game Ready Driver** or **Studio Driver** installed on Windows. WSL2 will automatically use this driver.

## Verification

Once installed, verify it by opening a standard PowerShell window and running:

```powershell
wsl --status
```

You should see: `Default Distribution: Ubuntu`

## Running the Project

Navigate to your project folder in WSL:

```bash
cd /mnt/c/Users/Don/experiment6/diatomic-vibrations-computational-study
./run_antigravity.sh
```
