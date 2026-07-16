# MD Universal Frame & Trajectory Extractor

This Python script uses `MDAnalysis` and `ParmEd` to replicate the functionality of the `autoimage` command and frame/trajectory extraction from `cpptraj` (AMBER). It centers the solute, wraps the solvent to prevent molecules from breaking across periodic boundaries (PBC), and extracts the desired frame or range.

## Features
* **Dynamic behavior**: Automatically decides whether to extract a full trajectory or a single frame by reading the output file extension.
* **cpptraj indices**: You can input frame numbers starting from 1 (just like cpptraj does), and the script automatically handles the translation to Python's 0-based indexing.
* **Supported formats**: Exports trajectories to `.dcd`, `.nc`, etc., and individual frames to `.rst`, `.rst7`, `.pdb`, etc.

## Usage
Open the frame_extractor.py file with your favorite text editor and modify only the USER SETTINGS block found at the top of the file:

TOPOLOGY_FILE = 'USER_TOPOLOGY.prmtop'
INPUT_TRAJECTORY = 'USER_TRAJECTORY.dcd'
OUTPUT_FILE = 'USER_OUTPUT.EXTENSION' 
    # The script automatically detects what to do based on the output extension:
    # - Trajectories (.dcd, .nc, .coord, .xtc, .trr): Extracts a range of frames.
    # - Single frames (.rst, .rst7, .pdb, .inpcrd): Extracts ONLY the START_FRAME.

    # Frames setup (1-based indexing, exactly like cpptraj)
# NOTE: If exporting a single frame, ONLY 'START_FRAME' is used as the target.
START_FRAME = INITIAL_FRAME 
END_FRAME = LAST_FRAME
STEP = 1

## Prerequisites

To install the required dependencies, run:
```bash
pip install -r requirements.txt