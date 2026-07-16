import os
import MDAnalysis as mda
from MDAnalysis import transformations
import parmed as pmd

# =============================================================================
# USER SETTINGS (Modify these values)
# =============================================================================
TOPOLOGY_FILE = 'mutated_ok.prmtop'
INPUT_TRAJECTORY = 'METAD-pos-1.dcd'

# The script automatically detects what to do based on the output extension:
# - Trajectories (.dcd, .nc, .coord, .xtc, .trr): Extracts a range of frames.
# - Single frames (.rst, .rst7, .pdb, .inpcrd): Extracts ONLY the START_FRAME.
OUTPUT_FILE = 'mutated.rst'

# Frames setup (1-based indexing, exactly like cpptraj)
# NOTE: If exporting a single frame, ONLY 'START_FRAME' is used as the target.
START_FRAME = 30
END_FRAME = 5270
STEP = 1

# Selection string for centering
SOLUTE_SELECTION = 'protein'
# =============================================================================

# =============================================================================
# LOGIC & EXECUTION (Do not modify below this line)
# =============================================================================
# 1. Determine output format and mode based on file extension
_, ext = os.path.splitext(OUTPUT_FILE)
ext = ext.lower()

traj_extensions = ['.dcd', '.nc', '.coord', '.netcdf', '.trr', '.xtc']
frame_extensions = ['.rst', '.rst7', '.pdb', '.inpcrd', '.gro']

if ext not in traj_extensions and ext not in frame_extensions:
    raise ValueError(f"Extension '{ext}' not recognized. Please use a valid extension.")

# 2. Load and transform Universe
print(f"Loading {TOPOLOGY_FILE} and {INPUT_TRAJECTORY}...")
u = mda.Universe(TOPOLOGY_FILE, INPUT_TRAJECTORY)

solute = u.select_atoms(SOLUTE_SELECTION)
all_atoms = u.atoms

transform_center = transformations.center_in_box(solute, center='geometry')
transform_wrap = transformations.wrap(all_atoms, compound='fragments')
u.trajectory.add_transformations(transform_center, transform_wrap)

# 3. Execute Trajectory Mode
if ext in traj_extensions:
    print(f"Mode: TRAJECTORY. Extracting frames {START_FRAME} to {END_FRAME}...")
    start_idx = START_FRAME - 1
    end_idx = END_FRAME
    
    with mda.Writer(OUTPUT_FILE, all_atoms.n_atoms) as W:
        for ts in u.trajectory[start_idx : end_idx : STEP]:
            W.write(all_atoms)
            
    print(f"Success! Trajectory saved in {OUTPUT_FILE}")

# 4. Execute Single Frame Mode
elif ext in frame_extensions:
    print(f"Mode: SINGLE FRAME. Extracting frame {START_FRAME}...")
    target_idx = START_FRAME - 1
    
    # Move the universe state to the target frame
    u.trajectory[target_idx]
    
    print("Formatting and saving via ParmEd...")
    parmed_structure = all_atoms.convert_to('PARMED')
    
    # Force AMBER restart format if the classic '.rst' extension is used
    if ext == '.rst':
        parmed_structure.save(OUTPUT_FILE, format='rst7', overwrite=True)
    else:
        # ParmEd automatically detects .pdb, .rst7, .inpcrd, etc.
        parmed_structure.save(OUTPUT_FILE, overwrite=True)
        
    print(f"Success! Frame {START_FRAME} saved in {OUTPUT_FILE}")
    