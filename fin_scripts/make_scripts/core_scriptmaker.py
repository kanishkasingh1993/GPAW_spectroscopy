from ase import Atom
from ase.build import molecule
from ase import io
import os
import sys
import argparse


#ARGS 
parser = argparse.ArgumentParser(description='For input files')
parser.add_argument('-inp', '--inpath', metavar='dir', type=str, nargs=1,
                        help='path where inp files are  (default ./)')
parser.add_argument('-sp','--scriptpath',metavar='dir',type=str,nargs=1,
			help='path where script will be saved')
parser.add_argument('-f','--inpfile',metavar='str',type=str,nargs=1,
			help='name of input xyz file')

#Declaring variables for ase calc

args = parser.parse_args()

ase_inp=args.inpath[0]
script_path=args.scriptpath[0]
input_file=args.inpfile[0]



#Declaring all variables for bash
python_path="/home/${USER}/fin_scripts"
#script_out="C:/Users/kanishk/Desktop/spectra/"
input_path="/home/${USER}/input_files/"
output_path="/home/${USER}/output_files/"
#script_path="/home/${USER}/input_files/input_scripts/"
#input_path="C:/Users/kanishk/Desktop/spectra/"
#output_path="C:/Users/kanishk/Desktop/spectra/"
#script_path="C:/Users/kanishk/Desktop/spectra/"
#input_file="acrolein.xyz"
name=input_file[:-4]
script_file=name+"_coregs.sh"
output_path=output_path+name+"/"
file_path=ase_inp+input_file

#Process molecule info

molecule=io.read(file_path)
atom_list=molecule.get_chemical_symbols()

#Get list of indexes for core-hole
x=[i for i, j in enumerate(atom_list) if j == 'C']
# Set number of resources for sarray
s_array=len(x)-1

#Sbatch string 
sbatch_string="""#!/bin/bash
#BATCH --job-name=test_GPAW_job                   # replace name
#SBATCH --mail-user=singhk93@zedat.fu-berlin.de  # replace email address
#SBATCH --mail-type=end
#SBATCH --ntasks=1                             # replace with value for your job
#SBATCH --mem-per-cpu=1024                      # replace with value for your job
#SBATCH --time=01:00:00                         # replace with value for your job
#SBATCH --qos=standard                          # replace with value for your job
#SBATCH --cpus-per-task=4
#SBATCH --array=0-"""+ str(s_array)

#modules PARAMS
mods="""module add GPAW"""
variables="""PYTHDIR="""+ python_path+"""
INPUTDIR="""+input_path+ """                        # replace with your directory
OUTPUTDIR="""+output_path+"""
INPUT_FILES="""+input_file+"""
FILE_PATH="""+file_path

c_dir="cd $PYTHDIR"
mk_dir="""if [ ! -d $OUTPUTDIR ]; then
  mkdir $OUTPUTDIR
fi"""

t="("
for i in range(len(x)):
    t=t+str(x[i])+" "
t=t[:-1]    
t=t+")"

#INDEX
index_string="""INDICES="""+ t + """
atom_index=${INDICES[${SLURM_ARRAY_TASK_ID}]} """
exec_string="""mpiexec	--oversubscribe -np 4  python3  core_groundstate.py -p $INPUTDIR -p2 $OUTPUTDIR -name ${INPUT_FILES[0]} -num ${SLURM_ARRAY_TASK_ID} -procs 4 -index ${atom_index} 
"""

with open(script_path+script_file, "a") as f:
    f.write(sbatch_string)
    f.write("\n\n")
    f.write(mods)
    f.write("\n\n")
    f.write(variables)
    f.write("\n")
    f.write(c_dir)
    f.write("\n")
    f.write(mk_dir)
    f.write("\n\n")
    f.write(index_string)
    f.write("\n\n")
    f.write(exec_string)
