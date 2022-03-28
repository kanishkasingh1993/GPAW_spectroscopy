# GPAW_spectroscopy
 Scripts for automating GPAW XAS calculations
 
The calculation works in three parts core, ground state and excited state. The routine works by ensuring all the three calculations can be run independently for each   molecule. For each method separate bash scripts are created for each molecule. As an example, for Ethane C 1s XAS spectra there will be 
a. Two core state calculations
b. One ground state calculation.
c. Two excited state calculations
The indices for each type of atom are calculated on the fly using ASE
In depth details for each type
 1. Core state : Calculates unoccupied states (Part 1 of XAS simulation) for each index of atom under investigation
 Scripts for this are generated using fin_scripts/make_scripts/core_scripts.py
 All the calculations are done for all input xyz files placed in the folder and all bash files for all the indexes are created simultaneously. 
 For sample scripts see the folder mol_scripts/core_scripts/*any molecule name*/
 Each core state calculation is done with the help of the python scripts core_groundstate.py. This file uses the core_gs.py to get functions that actually perform core calculations with a GPAW calc object. The output for the script is a gpw file.
 For output files refer to output_files/*molecule name*/moleculename_index.gpw

  2. Core state : Calculates unoccupied states (Part 1 of XAS simulation) for each index of atom under investigation
 Scripts for this are generated using fin_scripts/make_scripts/core_scripts.py
 All the calculations are done for all input xyz files placed in the folder and all bash files for all the indexes are created simultaneously. 
 For sample scripts see the folder mol_scripts/core_scripts/*any molecule name*/
 Each core state calculation is done with the help of the python scripts core_groundstate.py. This file uses the core_gs.py to get functions that actually perform core   calculations with a GPAW calc object.
 
 
 
