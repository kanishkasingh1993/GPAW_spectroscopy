# GPAW_spectroscopy
 Scripts for automating GPAW XAS calculations
 
The calculation works in three parts core, ground state and excited state. The routine works by ensuring all the three calculations can be run independently for each   molecule. For each method separate bash scripts are created for each molecule. As an example, for Ethane C 1s XAS spectra there will be 
a. Two core state calculations
b. One ground state calculation.
c. Two excited state calculations
The indices for each type of atom are calculated on the fly using ASE
In depth details for each type
 1. **Core state** : Calculates unoccupied states (Part 1 of XAS simulation) for each index of atom under investigation
 Scripts for this are generated using fin_scripts/make_scripts/core_scripts.py
 All the calculations are done for all input xyz files placed in the folder and all bash files for all the indexes are created simultaneously. 
 For sample scripts see the folder mol_scripts/core_scripts/*any molecule name_index*
 Each core state calculation is done with the help of the python scripts core_groundstate.py. This file uses the core_gs.py to get functions that actually perform core calculations with a GPAW calc object. The output for the script is a gpw file.
 For output files refer to output_files/*molecule name*/moleculename_index.gpw

  2. **Ground state** : Calculates ground state (Part 2 of XAS simulation) for each index of atom under investigation
 Scripts for this are generated using fin_scripts/make_scripts/gs_scripts.py
 All the calculations are done for all input xyz files placed in the folder and all bash files are created simultaneously. 
 For sample scripts see the folder mol_scripts/gs_scripts/*any molecule name*
 Each ground state calculation is done with the help of the python scripts groundstate.py. This file uses the gs.py to get functions that actually perform ground   calculations with a GPAW calc object. 
The output is stored in the output folder as a txt file. The ground state energy is stored as well as in an excel file under the name of the said molecule. For an example refer to  output_files/*molecule name*/moleculename.csv

 3. **Excited state** : Calculates unoccupied states (Part 3 of XAS simulation) for each index of atom under investigation
 Scripts for this are generated using fin_scripts/make_scripts/exc_scripts.py
 All the calculations are done for all input xyz files placed in the folder and all bash files for all the indexes are created simultaneously. 
 For sample scripts see the folder mol_scripts/exc_scripts/*any molecule name_index_name*
 Each excited state calculation is done with the help of the python scripts main.py. This file uses the exc.py to get functions that actually perform excited state calculations with a GPAW calc object for each index. The output for the script is a gpw file.
 For output files refer to output_files/*molecule name*/*molecule_name.xyz_exc_index*. In addition the csv file used from ground state calculations is modified and excited state energy is added to this.
 
 4. **Spectrum calculation** : Once all the above calculations are completed, the csv files are modified and spectra are plotted using matplotlib. The python files to be used are in the folder fin_scripts/spectra_scripts. The file spectra uses the functions within generate to perform this. This gives individual fingerprint spectra for each index as well as a complete spectrum after calculating the delta kohn sham energies from the csv file generated in the previous calculations. 
 

 
 
 
 
